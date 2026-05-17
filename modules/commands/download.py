"""
Async YouTube audio downloader using yt-dlp.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from modules.utils.colors import GREEN, RED, RESET, YELLOW

AUDIO_CODECS = frozenset({"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav"})

VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


@dataclass
class Download:
    """Asynchronous audio/video downloader using yt-dlp with parallel execution.

    Supports both context manager (``async with``) and async iteration (``async for``).
    """

    urls: str
    codec: str
    kbps: int
    quiet: bool
    max_concurrent: int
    metadata: bool
    cookies: str
    proxy: str

    _executor: ThreadPoolExecutor = field(init=False, repr=False, default=None)

    def __post_init__(self):
        """Resolve download path from config on instantiation."""
        from modules.utils.configer import get_path

        self.download_path = get_path()
        self._url_list = self._parse_urls()

    def _parse_urls(self) -> list[str]:
        """Split and clean URL string into a list of individual URLs."""
        return [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]

    async def __aenter__(self):
        """Create thread pool on context entry."""
        self._executor = ThreadPoolExecutor(max_workers=self.max_concurrent)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Gracefully shut down thread pool on context exit."""
        if self._executor:
            self._executor.shutdown(wait=True, cancel_futures=False)
        return False

    async def __aiter__(self):
        """Stream download results as they complete using async iteration."""
        sem = asyncio.Semaphore(self.max_concurrent)

        async def download_one(url):
            async with sem:
                return await self._download_url(url)

        tasks = [asyncio.create_task(download_one(u)) for u in self._url_list]

        for task in asyncio.as_completed(tasks):
            yield await task

    def _get_opts(self) -> dict:
        """Build yt-dlp options dict based on codec type (audio or video)."""
        is_audio = self.codec in AUDIO_CODECS

        base_opts = {
            "quiet": self.quiet,
            "no_warnings": True,
            "outtmpl": f"{self.download_path}/%(title)s.%(ext)s",
            "concurrent_fragment_downloads": self.max_concurrent,
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
                base_opts["postprocessors"].extend(
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

        if self.proxy:
            base_opts["proxy"] = self.proxy
        if self.cookies:
            base_opts["cookiesfrombrowser"] = self.cookies

        return base_opts

    async def download_all(self):
        """Download all URLs concurrently and print results as they complete."""
        if not self._url_list:
            return

        async for result in self:
            print(result)

    async def _download_url(self, url: str) -> str:
        """Download a single URL with status formatting."""
        print(f"{YELLOW}Starting: {url}{RESET}")
        try:
            await asyncio.to_thread(self._sync_download, url)
            return f"{GREEN}✅ Done: {url}{RESET}"
        except Exception as e:
            return f"{RED}❌ Failed: {url} — {e}{RESET}"

    def _sync_download(self, url: str):
        """Synchronous yt-dlp download callable from a thread."""
        from yt_dlp import YoutubeDL

        with YoutubeDL(self._get_opts()) as ydl:
            ydl.download([url])
