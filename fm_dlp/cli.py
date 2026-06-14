def main():

    import sys

    from arg_kiss import CLI

    from .utils.functions import echo

    app = CLI(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version="4.0.0",
    )

    @app.command()
    def search(
        query: str,
        limit: int = 10,
        yt_video: bool = False,
        album: bool = False,
        raw: bool = False,
        only_url: bool = False,
        no_color: bool = False,
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            yt_video: Search for YouTube videos instead of music tracks.
            album: Search for albums instead of individual tracks.
            raw: Output results in raw format (Python dict representation).
            only_url: Output only the URLs without any formatting.
            no_color: Disable colored output in search results.
        """
        if no_color:
            from fm_dlp.utils.colors import set_colors

            set_colors(False)
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

        program = Search(query, limit, yt_video, album, raw, only_url, no_color)

        for result in program.search():
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
        no_color: bool = False,
    ):
        """Download audio or video content from supported platforms.

        Args:
            urls: Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).
            codec: Audio codec or video container. Default depends on platform.
                  For audio: mp3, aac, flac, m4a, opus, vorbis, wav.
                  For video: mp4, mov, mkv, webm, avi, flv.
            kbps: Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size.
            jobs: Maximum number of concurrent downloads. Increase for faster batch downloads.
            quiet: Suppress yt-dlp output messages. Errors will still be shown.
            metadata: Embed metadata (title, artist, album) and thumbnail into audio files.
            path: Custom download directory path. Uses configured default if not specified.
            cookies: Path to cookies file (e.g., 'cookies.txt') for authenticated downloads,
                    or browser name ('chrome', 'firefox', 'edge', 'safari', 'brave', 'opera')
                    to extract cookies from browser.
            no_color: Disable colored output in download progress and status messages.
        """
        from .utils.configer import get_path
        from .utils.validator import (
            AUDIO_CODECS,
            validate_download,
            validate_ffmpeg,
        )

        default_codec = "m4a" if sys.platform == "darwin" else "opus"
        codec = codec or default_codec
        path = path or get_path(no_color)

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
                no_color=no_color,
            ) as dl:
                await dl.download_all()

        asyncio.run(run())

    @app.command()
    def config(path: str, no_color: bool = False):
        """Configure the application settings.

        Args:
            path: Default directory path where downloaded files will be saved.
                 Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').
            no_color: Disable colored output in configuration messages.
        """
        from .utils.configer import set_path

        echo(set_path(path, no_color))

    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
