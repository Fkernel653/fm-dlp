def main():

    import sys

    from arg_kiss import CLI

    from .utils.functions import echo

    app = CLI(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version="3.9.9",
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        yt_video: bool = False,
        album: bool = False,
        raw: bool = False,
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            yt-video: Search for Youtube videos.
            album: Search by albums
            raw: Output of results in RAW format
        """
        try:
            limit_int = int(limit) if limit is not None else 10
            if limit_int <= 0:
                from .utils.colors import error, info

                echo(error(f"Invalid limit: {limit}"))
                echo(info("Must be a positive integer."))
                return
            limit = limit_int
        except (TypeError, ValueError):
            from .utils.colors import error, info

            echo(error(f"Invalid limit: {limit}"))
            echo(info("Must be a non-negative integer."))
            return

        from .commands.search import Search

        program = Search(query, limit, album, raw)

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
            validate_download,
            validate_ffmpeg,
        )

        default_codec = "m4a" if sys.platform == "darwin" else "opus"
        codec = codec or default_codec
        path = path or get_path()

        if not validate_download(urls, codec, kbps, jobs, path):
            return

        if codec in AUDIO_CODECS:
            if not validate_ffmpeg():
                return

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
            ) as dl:
                await dl.download_all()

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
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
