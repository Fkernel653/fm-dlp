"""Async YouTube audio downloader using yt-dlp."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

AUDIO_CODECS = frozenset({"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav"})

VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


class Download:
    """Asynchronous audio/video downloader using yt-dlp with parallel execution.

    Supports both context manager (``async with``) and async iteration (``async for``).
    """

    def __init__(
        self,
        urls: str,
        codec: str,
        kbps: int,
        jobs: int,
        quiet: bool,
        metadata: bool,
        path: str,
        cookies: str | None = None,
    ):
        self.urls = urls
        self.codec = codec
        self.kbps = kbps
        self.jobs = jobs
        self.quiet = quiet
        self.metadata = metadata
        self.path = path
        self.cookies = cookies
        self._executor: ThreadPoolExecutor | None = None
        self._url_list = self._parse_urls()

    def _parse_urls(self) -> list[str]:
        return [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]

    async def __aenter__(self):
        self._executor = ThreadPoolExecutor(max_workers=self.jobs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._executor:
            self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    def __aiter__(self):
        return self._aiter()

    async def _aiter(self):
        sem = asyncio.Semaphore(self.jobs)

        async def download_one(url):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in self._url_list]
        for task in asyncio.as_completed(tasks):
            yield await task

    def _get_opts(self) -> dict[str, Any]:  # type: ignore[explicit-any]
        is_audio = self.codec in AUDIO_CODECS

        base_opts: dict[str, Any] = {
            "quiet": self.quiet,
            "no_warnings": self.quiet,
            "outtmpl": f"{self.path}/%(title)s.%(ext)s",
            "concurrent_fragment_downloads": self.jobs,
            "extractor_retries": 3,
        }

        if is_audio:
            base_opts.update(
                format="bestaudio/best",
                postprocessors=[
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": self.codec,
                        "preferredquality": str(self.kbps),
                    },
                ],
            )
            if self.metadata:
                base_opts.setdefault("postprocessors", []).extend(
                    [{"key": "FFmpegMetadata"}, {"key": "EmbedThumbnail"}]
                )
                base_opts.update(embedmetadata=True, writethumbnail=True)
        else:
            audio_ext = VIDEO_CONTAINER_AUDIO_MAP.get(self.codec, "m4a")
            format_str = (
                f"bestvideo[ext=mp4]+bestaudio[ext={audio_ext}]/bestvideo+bestaudio/best"
                if self.codec == "mp4"
                else f"bestvideo+bestaudio[ext={audio_ext}]/bestvideo+bestaudio/best"
            )
            base_opts.update(format=format_str, merge_output_format=self.codec)

        if self.cookies:
            base_opts["cookiesfrombrowser"] = self.cookies

        return base_opts

    async def download_all(self) -> str | None:
        if not self._url_list:
            return
        async for result in self:
            if result is not None:
                print(result)

    async def _download_url(self, url: str) -> str | None:
        import sys

        from color_kiss import BOLD, GREEN, YELLOW
        from color_kiss.utils import info, styled
        from yt_dlp.utils import DownloadError

        if self.codec == "wav" and self.metadata:
            self.metadata = False
            print(info("WAV format doesn't support metadata embedding"))

        print(styled(f"\nStarting: {url}\n", YELLOW, BOLD))
        try:
            await asyncio.to_thread(self._sync_download, url)
            return styled(f"\nDone: {url}\n", GREEN, BOLD)
        except DownloadError:
            return sys.exit(1)

    def _sync_download(self, url: str):
        from yt_dlp import YoutubeDL

        with YoutubeDL(self._get_opts()) as ydl:  # type: ignore[explicit-any]
            ydl.download([url])
