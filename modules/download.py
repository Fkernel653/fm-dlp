"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

import asyncio
import concurrent.futures
import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncGenerator, AsyncIterator

from yt_dlp import YoutubeDL

from modules.add_metadata import add_metadata
from modules.colors import BOLD, GREEN, RED, RESET, YELLOW


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    urls: str
    codec: str
    kbps: int
    quiet: bool
    max_concurrent: int
    cookies: str
    proxy: str

    config_file = Path(__file__).parent.parent / "config.json"

    def __post_init__(self):
        from shutil import which

        self.kbps = int(self.kbps)
        self.max_concurrent = int(self.max_concurrent)

        if which("ffmpeg") is None:
            exit(f"{RED}FFmpeg not found in PATH! Please install FFmpeg.{RESET}")
        if not self.config_file.exists():
            exit(
                f"{RED}\nConfig file not found!{RESET}\n{YELLOW}Run: fm-dlp config /path/to/downloads{RESET}\n"
            )

    def _get_download_path(self):
        from json import JSONDecodeError, loads

        try:
            data = loads(self.config_file.read_text(encoding="utf-8"))
            path = data.get("path")
            if not path or not Path(path).exists():
                exit(f"{RED}\nDownload path '{path}' does not exist.{RESET}\n")
            return path
        except (JSONDecodeError, UnicodeDecodeError) as e:
            exit(f"{RED}\nConfig file corrupted or has wrong encoding: {e}{RESET}\n")
        except Exception as e:
            exit(f"{RED}\nError reading config file: {e}{RESET}\n")

    def _create_base_opts(self, **extra):
        return {
            "proxy": self.proxy or None,
            "cookiesfrombrowser": self.cookies or None,
            "quiet": self.quiet,
            "no_warnings": True,
            **extra,
        }

    def __aiter__(self) -> AsyncIterator[str]:
        return self._run()

    async def _run(self) -> AsyncGenerator[str, None]:
        download_path = self._get_download_path()
        loop = asyncio.get_event_loop()

        cpu_count = min(self.max_concurrent, os.cpu_count() or 4)
        process_executor = concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count)
        thread_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_concurrent * 2
        )

        def _download_single(entry, url):
            thread_local = threading.local()

            def hook(d):
                if d["status"] == "finished":
                    filepath = d["info_dict"].get("filepath") or d.get("filename")
                    thread_local.downloaded_file = Path(filepath) if filepath else None

            title = entry.get("title", "")
            video_url = entry.get("webpage_url") or entry.get("url") or url
            opts = self._create_base_opts(
                format="bestaudio/best",
                outtmpl=f"{download_path}/%(title)s.%(ext)s",
                writethumbnail=True,
                postprocessors=[
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": self.codec,
                        "preferredquality": str(self.kbps),
                    },
                    {"key": "EmbedThumbnail"},
                ],
                postprocessor_hooks=[hook],
                concurrent_fragment_downloads=8,
                extractor_retries=3,
                file_access_retries=3,
                fragment_retries=3,
            )

            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([video_url])

                downloaded_file = getattr(thread_local, "downloaded_file", None)
                if not downloaded_file:
                    for ext in [self.codec, "m4a", "opus", "webm", "mp3"]:
                        candidate = Path(download_path) / f"{title}.{ext}"
                        if candidate.exists():
                            downloaded_file = candidate
                            break

                if not downloaded_file:
                    return {
                        "success": False,
                        "title": title,
                        "error": "File not found after download",
                    }

                return {
                    "success": True,
                    "title": title,
                    "file": downloaded_file,
                    "artist": entry.get("uploader") or entry.get("channel") or "",
                    "album": entry.get("album") or entry.get("channel") or "",
                }
            except Exception as e:
                return {
                    "success": False,
                    "title": title,
                    "error": f"{type(e).__name__}: {e}",
                }

        async def process_metadata(result):
            if not result.get("success"):
                return f"{RED}\n✗ {result['title']} - {result['error']}{RESET}"

            try:
                await loop.run_in_executor(
                    process_executor,
                    add_metadata,
                    result["file"],
                    self.codec,
                    result["title"],
                    result["artist"],
                    result["album"],
                )
                return f"{GREEN}✓ {result['title']}{RESET}"
            except Exception as e:
                return f"{YELLOW}⚠ {result['title']} - metadata failed: {e}{RESET}"

        def _cancel_tasks(tasks):
            for task in tasks:
                if not task.done():
                    task.cancel()

        async def process_tasks(tasks, url_prefix=""):
            download_tasks = []
            metadata_tasks = []
            try:
                download_tasks = [asyncio.create_task(t) for t in tasks]
                results = await asyncio.gather(*download_tasks, return_exceptions=True)

                for r in results:
                    if isinstance(r, Exception):
                        metadata_tasks.append(
                            asyncio.ensure_future(
                                asyncio.sleep(0, result=f"{RED}✗ Error: {r}{RESET}")
                            )
                        )
                    elif isinstance(r, dict):
                        metadata_tasks.append(asyncio.create_task(process_metadata(r)))
                    elif isinstance(r, str):
                        metadata_tasks.append(
                            asyncio.ensure_future(asyncio.sleep(0, result=r))
                        )
                    else:
                        metadata_tasks.append(
                            asyncio.ensure_future(
                                asyncio.sleep(
                                    0,
                                    result=f"{YELLOW}⚠ Unexpected result type: {type(r)}{RESET}",
                                )
                            )
                        )

                output = []
                for t in asyncio.as_completed(metadata_tasks):
                    try:
                        result = await t
                        if result:
                            output.append(result)
                    except asyncio.CancelledError:
                        break

                return (
                    f"{YELLOW}Results:{RESET}\n" + "\n".join(output) + "\n"
                    if output
                    else f"{RED}Nothing downloaded for {url_prefix}{RESET}\n"
                )

            except asyncio.CancelledError:
                _cancel_tasks(download_tasks + metadata_tasks)
                return f"{YELLOW}⚠ Download cancelled for {url_prefix}{RESET}\n"

        async def download_url(url: str) -> str:
            def _get_entries():
                try:
                    opts = self._create_base_opts(
                        extractor_args={"youtube": {"skip": ["hls", "dash"]}}
                    )
                    with YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                    entries = info.get("entries", [info]) if info else []
                    return [e for e in entries if e is not None], None
                except Exception as e:
                    return (
                        None,
                        f"{RED}\nFailed to extract info for {url}: {type(e).__name__}: {e}{RESET}",
                    )

            print(f"{YELLOW}\nStarting: {RESET}{BOLD}{url}{RESET}")
            entries, error = await loop.run_in_executor(thread_executor, _get_entries)
            if error:
                return error
            if not entries:
                return f"{RED}\nNo valid entries to download for {url}{RESET}"

            sem = asyncio.Semaphore(self.max_concurrent)

            async def limited(entry):
                async with sem:
                    return await loop.run_in_executor(
                        thread_executor, _download_single, entry, url
                    )

            return await process_tasks([limited(e) for e in entries], url)

        urls = [url.strip() for url in self.urls.split() if url.strip()]
        if not urls:
            yield f"{RED}\nNo URLs provided{RESET}"
            return

        url_tasks = [asyncio.create_task(download_url(u)) for u in urls]
        try:
            for t in asyncio.as_completed(url_tasks):
                try:
                    yield await t
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    yield f"{RED}\n✗ Critical error: {type(e).__name__}: {e}{RESET}"
        finally:
            _cancel_tasks(url_tasks)
            await asyncio.gather(*url_tasks, return_exceptions=True)
            process_executor.shutdown(wait=False)
            thread_executor.shutdown(wait=False)
