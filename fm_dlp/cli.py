def main():

    import sys
    from functools import lru_cache

    from cliss import CLI

    from .utils.colors import say_goodbye
    from .utils.functions import echo

    @lru_cache(maxsize=1)
    def get_version() -> str | None:
        """Get version from installed package metadata."""
        try:
            from importlib.metadata import version

            return version("fm-dlp")
        except Exception:
            return "unknown"

    app = CLI(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version=get_version(),
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        yt_video: bool = False,
        type: str = "track",
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            yt-video: Search for Youtube videos.
            type: Content type — "track" or "album".
        """
        from .utils.validator import validate_input

        if not validate_input(
            limit=limit,
            search_type=type,
        ):
            return

        from .commands.search import Search

        program = Search(query, limit, type)

        for result in program.search("yt-video" if yt_video else "yt-music"):
            echo(result)

    @app.command()
    def download(
        urls: str,
        codec: str | None = None,
        kbps: int = 256,
        jobs: int = 5,
        quiet: bool = False,
        metadata: bool = True,
        path: str | None = None,
        cookies: str | None = None,
    ):
        """Download audio or video content from supported platforms.

        Args:
            urls: Single URL or comma/space-separated list of URLs.
            codec: Audio codec or video container. Default depends on platform.
            kbps: Audio bitrate in kbps (64–320).
            jobs: Maximum concurrent downloads.
            quiet: Suppress yt-dlp output.
            metadata: Embed metadata and thumbnail (audio only).
            path: Download directory path.
            cookies: Path to cookies file (e.g., 'cookies.txt') or browser name
                         (e.g., 'chrome', 'firefox', 'edge', 'safari', 'brave', 'opera')
                         for cookie extraction.
        """
        from .utils.configer import get_path
        from .utils.validator import (
            AUDIO_CODECS,
            validate_input,
            validate_with_shutil,
        )

        codec = codec or "m4a" if sys.platform == "darwin" else "opus"
        path = path or get_path()

        if not validate_input(
            url=urls,
            codec=codec,
            kbps=kbps,
            jobs=jobs,
        ):
            return

        if codec in AUDIO_CODECS:
            validate_with_shutil("ffmpeg", "FFmpeg")

        import asyncio

        from .commands.download import Download

        async def run():
            async with Download(
                urls=urls,
                codec=codec,
                kbps=kbps,
                jobs=jobs,
                quiet=quiet,
                metadata=metadata,
                path=path,
                cookies=cookies,
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

        echo(set_path(path))

    try:
        app.run()
    except KeyboardInterrupt:
        echo(say_goodbye())
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
