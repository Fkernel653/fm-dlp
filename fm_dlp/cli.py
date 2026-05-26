from functools import lru_cache


@lru_cache(maxsize=1)
def get_version() -> str | None:
    """Get version from installed package metadata."""
    try:
        from importlib.metadata import version

        return version("fm-dlp")
    except KeyboardInterrupt:
        pass
    except Exception:
        return "unknown"


def main():
    from cliss import CLI

    app = CLI(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version=get_version(),
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        platform: str = "yt-music",
        type: str = "track",
        proxy: str | None = None,
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            platform: Search platform — "yt-video" or "yt-music".
            type: Content type — "track" or "album".
            proxy: Optional proxy URL.
        """
        from .utils.validator import validate_input

        validate_input(
            limit=limit,
            platform=platform,
            type=type,
            proxy=proxy,
            proxy_only_http=(platform == "yt-music"),
        )

        from .commands.search import Search

        program = Search(query, limit, type, proxy)

        for result in program.search(platform):
            print(result)

    @app.command()
    def download(
        urls: str,
        codec: str | None = None,
        kbps: int = 256,
        max_concurrent: int = 5,
        quiet: bool = False,
        metadata: bool = True,
        path: str | None = None,
        cookies: str | None = None,
        proxy: str | None = None,
    ):
        """Download audio or video content from supported platforms.

        Args:
            urls: Single URL or comma/space-separated list of URLs.
            codec: Audio codec or video container. Default depends on platform.
            kbps: Audio bitrate in kbps (64–320).
            max_concurrent: Maximum concurrent downloads.
            quiet: Suppress yt-dlp output.
            metadata: Embed metadata and thumbnail (audio only).
            path: Download directory path.
            cookies: Browser name for cookie extraction.
            proxy: Optional proxy URL.
        """
        from .utils.validator import (
            AUDIO_CODECS,
            DEFAULT_CODEC,
            validate_input,
            validate_with_shutil,
        )

        codec = codec or DEFAULT_CODEC

        validate_input(
            url=urls,
            codec=codec,
            kbps=kbps,
            max_concurrent=max_concurrent,
            proxy=proxy,
        )

        if path is None:
            from .utils.configer import get_path

            path = get_path()

        if codec in AUDIO_CODECS:
            validate_with_shutil("ffmpeg", "FFmpeg")

            if codec == "wav" and metadata:
                from color_kiss.utils import info

                metadata = False
                print(info("WAV format doesn't support metadata embedding"))

        import asyncio

        from .commands.download import Download

        async def run():
            async with Download(
                urls=urls,
                codec=codec,
                kbps=kbps,
                max_concurrent=max_concurrent,
                quiet=quiet,
                metadata=metadata,
                download_path=path,
                cookies=cookies,
                proxy=proxy,
            ) as downloader:
                await downloader.download_all()

        asyncio.run(run())

    @app.command()
    def config(path: str):
        """Configure the application settings path.

        Args:
            path: Directory path for downloaded files.
        """
        from .utils.configer import set_path

        print(set_path(path))

    app.run()
