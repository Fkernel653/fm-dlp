"""Main downloader class."""

import asyncio
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import AsyncIterator

from yt_dlp import YoutubeDL

from ...utils import VIDEO_CONTAINERS, echo
from ...utils.colors import BOLD_YELLOW, RESET, info, set_colors, success
from .config import DownloadConfig
from .options_builder import OptionsBuilder
from .url_parser import URLParser


class Download:
    """Async YouTube audio/video downloader."""

    def __init__(
        self,
        url: str,
        codec: str,
        kbps: int,
        quality: str,
        jobs: int,
        quiet: bool,
        metadata: bool,
        keep: bool,
        save: bool,
        use_config: bool,
        path: str,
        only_video: bool,
        cookies: str | None,
        color: bool,
    ):
        """Initialize downloader with configuration."""
        self.config = DownloadConfig(
            url=url,
            codec=codec,
            kbps=kbps,
            quality=quality,
            jobs=jobs,
            quiet=quiet,
            metadata=metadata,
            keep=keep,
            save=save,
            use_config=use_config,
            path=path,
            only_video=only_video,
            cookies=cookies,
            color=color,
        )

        params = self.config.apply_config()
        self.codec = params["codec"]
        self.kbps = params["kbps"]
        self.quality = params["quality"]
        self.jobs = params["jobs"]
        self.quiet = params["quiet"]
        self.metadata = params["metadata"]
        self.keep = params["keep"]
        self.only_video = params["only_video"]
        self.cookies = params["cookies"]

        if not self.config.save_config():
            return

        self.path = path
        self.color = color
        self._executor = self._get_executor()
        self._url_list = URLParser(url, quiet).parse()

        set_colors(color)

        self.c = {
            "reset": RESET if color else "",
            "bold_yellow": BOLD_YELLOW if color else "",
        }

    def _get_executor(self):
        """Choose executor based on task type."""
        if self.only_video or self.codec in VIDEO_CONTAINERS:
            return ProcessPoolExecutor(max_workers=self.jobs)
        else:
            return ThreadPoolExecutor(max_workers=self.jobs)

    async def __aenter__(self):
        """Setup thread pool executor on context enter."""
        self._executor = self._get_executor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup thread pool executor on context exit."""
        self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    def __aiter__(self):
        """Return async iterator for download results."""
        return self._aiter()

    async def _aiter(self) -> AsyncIterator[str | None]:
        """Async iterator yielding download results with concurrency control."""
        sem = asyncio.Semaphore(self.jobs)

        async def download_one(url):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in self._url_list]
        for task in asyncio.as_completed(tasks):
            yield await task

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
            echo(f"\n{self.c['bold_yellow']}Starting:{self.c['reset']} {url}\n")

        await asyncio.to_thread(self._sync_download, url)

        return "\n" + success(url) + "\n" if not self.quiet else None

    def _sync_download(self, url: str) -> None:
        """Synchronous download using yt-dlp (runs in thread pool)."""
        options = OptionsBuilder(
            codec=self.codec,
            kbps=self.kbps,
            quality=self.quality,
            jobs=self.jobs,
            quiet=self.quiet,
            metadata=self.metadata,
            keep=self.keep,
            only_video=self.only_video,
            cookies=self.cookies,
            path=self.path,
            color=self.color,
        ).build()

        with YoutubeDL(options) as ydl:
            ydl.download([url])


async def run_downloader(
    url: str,
    codec: str,
    kbps: int,
    quality: str,
    jobs: int,
    quiet: bool,
    metadata: bool,
    keep: bool,
    save: bool,
    use_config: bool,
    path: str,
    only_video: bool,
    cookies: str | None,
    color: bool,
) -> None:
    """Run downloader with given parameters."""

    async with Download(
        url=url,
        codec=codec,
        kbps=kbps,
        quality=quality,
        jobs=jobs,
        quiet=quiet,
        metadata=metadata,
        keep=keep,
        save=save,
        use_config=use_config,
        path=path,
        only_video=only_video,
        cookies=cookies,
        color=color,
    ) as dl:
        try:
            await dl.download_all()
        except Exception as e:
            echo(str(e), file=sys.stderr)
