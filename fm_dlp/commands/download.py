"""Async YouTube audio/video downloader using yt-dlp."""

import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from ..utils import AUDIO_CODECS, echo
from ..utils.colors import (
    BOLD_GREEN,
    BOLD_YELLOW,
    RESET,
    error,
    info,
    set_colors,
    success,
)
from ..utils.config.configer import get_parameters, set_parameters
from ..utils.config.path import Path

VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


class Download:
    def __init__(
        self,
        url: str,
        codec: str,
        kbps: int,
        jobs: int,
        quiet: bool,
        metadata: bool,
        save: bool,
        use_config: bool,
        path: str,
        only_video: bool,
        cookies: str | None,
        color: bool,
    ):
        """Initialize downloader with configuration.

        Args:
            url: Single URL, comma/space-separated list, or path to file with URLs.
            codec: Audio codec (mp3, aac, flac, m4a, opus, vorbis, wav)
                   or video container (mp4, mov, mkv, webm, avi, flv).
            kbps: Audio bitrate in kbps (64-320).
            jobs: Maximum concurrent downloads.
            quiet: Suppress yt-dlp output.
            metadata: Embed metadata and thumbnail into audio files.
            save: Saving settings (except URL).
            use_config: Use saved parameters from config file as defaults.
            path: Download directory path.
            only_video: Download a video file without audio.
            cookies: Path to cookies file or browser name for authentication.
            color: Colored output.
        """
        self.urls = url

        if use_config:
            params = get_parameters(color)

            self.codec = params.get("codec", codec)
            self.kbps = params.get("kbps", kbps)
            self.jobs = params.get("jobs", jobs)
            self.quiet = params.get("quiet", quiet)
            self.metadata = params.get("metadata", metadata)
            self.only_video = params.get("only_video", only_video)
            self.cookies = params.get("cookies", cookies)
        else:
            self.codec = codec
            self.kbps = kbps
            self.jobs = jobs
            self.quiet = quiet
            self.metadata = metadata
            self.only_video = only_video
            self.cookies =

        if save:
            if not set_parameters(
                codec, kbps, jobs, quiet, metadata, only_video, cookies, color
            ):
                return

        self.path = path
        self.color = color
        self._executor: ThreadPoolExecutor | None = None
        self._url_list = self._parse_urls()

        set_colors(color)

        self._green = BOLD_GREEN if color else ""
        self._yellow = BOLD_YELLOW if color else ""

    def _parse_urls(self) -> list[str]:
        """Parse URLs from string or file path."""
        if not self.urls:
            return []

        url_path = Path(self.urls)
        if url_path.is_file():
            return self._parse_url_file(url_path)

        return [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]

    def _parse_url_file(self, file_path: Path) -> list[str]:
        """Read and parse URLs from a text file (one URL per line)."""
        urls_from_file = []

        try:
            content = file_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    urls_from_file.extend(
                        u.strip() for u in line.replace(",", " ").split() if u.strip()
                    )

            if not self.quiet:
                echo(info(f"Loaded {len(urls_from_file)} URLs from file: {self.urls}"))

        except UnicodeDecodeError:
            echo(
                error(
                    f"File '{self.urls}' is not UTF-8 encoded. Please save it as UTF-8.",
                ),
                file=sys.stderr,
            )
        except Exception as e:
            echo(error(f"Error reading URL file: {e}"), file=sys.stderr)

        return urls_from_file

    async def __aenter__(self):
        """Setup thread pool executor on context enter."""
        self._executor = ThreadPoolExecutor(max_workers=self.jobs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup thread pool executor on context exit."""
        if self._executor:
            self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    def __aiter__(self):
        """Return async iterator for download results."""
        return self._aiter()

    async def _aiter(self):
        """Async iterator yielding download results with concurrency control."""
        sem = asyncio.Semaphore(self.jobs)

        async def download_one(url):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in self._url_list]
        for task in asyncio.as_completed(tasks):
            yield await task

    def _get_opts(self) -> dict[str, Any]:
        """Build yt-dlp options dictionary."""
        base_opts: dict[str, Any] = {
            "quiet": self.quiet,
            "no_warnings": self.quiet,
            "outtmpl": str(Path(self.path) / "%(title)s.%(ext)s"),
            "concurrent_downloads": self.jobs,
            "concurrent_fragment_downloads": self.jobs,
            "extractor_retries": 3,
            "postprocessors": [],
        }

        if not self.color:
            base_opts["color"] = "no_color"

        if self.only_video:
            base_opts["format"] = "bestvideo/bestvideo"
            if self.codec in VIDEO_CONTAINER_AUDIO_MAP:
                base_opts["postprocessors"].append(
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": self.codec,
                    }
                )

            return base_opts

        if self.codec in AUDIO_CODECS:
            base_opts["format"] = "bestaudio/best"
            base_opts["postprocessors"].append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.codec,
                    "preferredquality": str(self.kbps),
                }
            )

            if self.metadata:
                base_opts["postprocessors"].extend(
                    [
                        {"key": "FFmpegMetadata"},
                        {"key": "EmbedThumbnail"},
                    ]
                )
                base_opts["embedmetadata"] = True
                base_opts["writethumbnail"] = True
        else:
            audio_ext = VIDEO_CONTAINER_AUDIO_MAP[self.codec]

            base_opts["format"] = (
                f"bestvideo+bestaudio[ext={audio_ext}]/bestvideo+bestaudio/best"
            )
            base_opts["merge_output_format"] = self.codec

        if self.cookies:
            cookie_path = Path(self.cookies)
            if cookie_path.is_file():
                base_opts["cookiefile"] = str(cookie_path)
            else:
                base_opts["cookiesfrombrowser"] = (self.cookies,)

        return base_opts

    async def download_all(self) -> None:
        """Download all URLs and echo results as they complete."""
        if not self._url_list:
            return
        async for result in self:
            if result is not None:
                echo(result)

    async def _download_url(self, url: str) -> str | None:
        """Download a single URL and return status message."""

        if self.codec == "wav" and self.metadata:
            self.metadata = False
            if not self.quiet:
                echo(info("WAV format doesn't support metadata embedding"))

        if not self.quiet:
            echo(f"\n{BOLD_YELLOW}Starting:{RESET} {url}\n")

        await asyncio.to_thread(self._sync_download, url)

        return "\n" + success(url) + "\n" if not self.quiet else None

    def _sync_download(self, url: str) -> None:
        """Synchronous download using yt-dlp (runs in thread pool)."""
        from yt_dlp import YoutubeDL

        with YoutubeDL(self._get_opts()) as ydl:
            ydl.download([url])


async def run_downloader(
    urls: str,
    codec: str,
    kbps: int,
    jobs: int,
    quiet: bool,
    metadata: bool,
    save: bool,
    use_config: bool,
    path: str,
    only_video: bool,
    cookies: str | None,
    color: bool,
) -> None:
    """Run downloader with given parameters."""
    async with Download(
        urls=urls,
        codec=codec,
        kbps=kbps,
        jobs=jobs,
        quiet=quiet,
        metadata=metadata,
        save=save,
        use_config=use_config,
        path=path,
        only_video=only_video,
        cookies=cookies,
        color=color,
    ) as dl:
        await dl.download_all()
