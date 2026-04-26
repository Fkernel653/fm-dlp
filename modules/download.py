"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from typing import AsyncGenerator, AsyncIterator
from yt_dlp import YoutubeDL
from pathlib import Path
import asyncio
import concurrent.futures
import threading
import os

from modules.colors import RESET, BOLD, RED, GREEN, YELLOW
from modules.add_metadata import add_metadata


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

        if which("ffmpeg") is None:
            print(f"{RED}FFmpeg not found in PATH! Please install FFmpeg.{RESET}")
            exit(1)
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found!{RESET}\n{YELLOW}Run: fm-dlp config /path/to/downloads{RESET}\n"
            )
            exit(1)

    def _get_download_path(self):
        from json import loads, JSONDecodeError

        try:
            data = loads(self.config_file.read_text(encoding="utf-8"))
            path = data.get("path")
            if not path or not Path(path).exists():
                print(f"{RED}\nDownload path '{path}' does not exist.{RESET}\n")
                exit(1)
            return path
        except (JSONDecodeError, UnicodeDecodeError) as e:
            print(f"{RED}\nConfig file corrupted or has wrong encoding: {e}{RESET}\n")
            exit(1)
        except Exception as e:
            print(f"{RED}\nError reading config file: {e}{RESET}\n")
            exit(1)

    def _create_base_opts(self, extra=None):
        opts = {
            "proxy": self.proxy or None,
            "cookiesfrombrowser": self.cookies or None,
            "quiet": self.quiet,
            "no_warnings": True,
        }
        if extra:
            opts.update(extra)
        return opts

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
            """Загрузка в отдельном потоке (I/O bound)"""
            thread_local = threading.local()

            def hook(d):
                if d["status"] == "finished":
                    thread_local.downloaded_file = Path(d["info_dict"]["filepath"])

            title = entry.get("title", "")
            video_url = entry.get("webpage_url") or entry.get("url") or url
            opts = self._create_base_opts(
                {
                    "format": "bestaudio/best",
                    "outtmpl": f"{download_path}/%(title)s.%(ext)s",
                    "writethumbnail": True,
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": self.codec,
                            "preferredquality": str(self.kbps),
                        },
                        {"key": "EmbedThumbnail"},
                    ],
                    "postprocessor_hooks": [hook],
                    "concurrent_fragment_downloads": 8,
                    "extractor_retries": 3,
                    "file_access_retries": 3,
                    "fragment_retries": 3,
                }
            )

            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([video_url])

                if not thread_local.downloaded_file:
                    return f"{RED}\n✗ {title} (file not found after download){RESET}"

                return {
                    "success": True,
                    "title": title,
                    "file": thread_local.downloaded_file,
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
            """Добавление метаданных в process pool (CPU intensive)"""
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
                return f"{GREEN}\n✓ {result['title']}{RESET}"
            except Exception as e:
                return f"{YELLOW}\n⚠ {result['title']} - metadata failed: {e}{RESET}"

        def _cancel_tasks(tasks):
            for task in tasks:
                if not task.done():
                    task.cancel()

        async def process_tasks(tasks, url_prefix=""):
            results = []
            try:
                download_tasks = [asyncio.create_task(t) for t in tasks]
                results = await asyncio.gather(*download_tasks, return_exceptions=True)

                metadata_tasks = []
                for r in results:
                    if isinstance(r, Exception):
                        metadata_tasks.append(
                            asyncio.create_task(
                                asyncio.sleep(0, result=f"{RED}\n✗ Error: {r}{RESET}")
                            )
                        )
                    elif isinstance(r, dict):
                        metadata_tasks.append(asyncio.create_task(process_metadata(r)))
                    else:
                        metadata_tasks.append(
                            asyncio.create_task(asyncio.sleep(0, result=r))
                        )

                output = []
                for t in asyncio.as_completed(metadata_tasks):
                    result = await t
                    if result:
                        output.append(result)

                return (
                    "\n".join(output)
                    if output
                    else f"{RED}\nNothing downloaded for {url_prefix}{RESET}"
                )

            except asyncio.CancelledError:
                _cancel_tasks(download_tasks)
                _cancel_tasks(metadata_tasks)
                return f"{YELLOW}\n⚠ Download cancelled for {url_prefix}{RESET}"

        async def download_url(url: str) -> str:
            def _get_entries():
                try:
                    opts = self._create_base_opts()
                    opts["extractor_args"] = {"youtube": {"skip": ["hls", "dash"]}}
                    with YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                except Exception as e:
                    return (
                        None,
                        f"{RED}\nFailed to extract info for {url}: {type(e).__name__}: {e}{RESET}",
                    )

                if info is None:
                    return None, f"{RED}\nFailed to get video info for {url}{RESET}"
                entries = info.get("entries", [info])
                return [e for e in entries if e is not None], None

            try:
                print(f"{YELLOW}\nStarting: {RESET}{BOLD}{url}{RESET}")
                entries, error = await loop.run_in_executor(
                    thread_executor, _get_entries
                )
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

                download_tasks = [limited(e) for e in entries]
                return await process_tasks(download_tasks, url)

            except Exception as e:
                return f"{RED}\n✗ URL processing failed for {url}: {type(e).__name__}: {e}{RESET}"

        urls = [url.strip() for url in self.urls.split() if url.strip()]
        if not urls:
            yield f"{RED}\nNo URLs provided{RESET}"
            return

        try:
            url_tasks = [asyncio.create_task(download_url(u)) for u in urls]

            for t in asyncio.as_completed(url_tasks):
                try:
                    result = await t
                    yield result
                except asyncio.CancelledError:
                    _cancel_tasks(url_tasks)
                    break
                except Exception as e:
                    yield f"{RED}\n✗ Critical error: {type(e).__name__}: {e}{RESET}"

        finally:
            _cancel_tasks(url_tasks)
            await asyncio.gather(*url_tasks, return_exceptions=True)
            process_executor.shutdown(wait=False)
            thread_executor.shutdown(wait=False)
