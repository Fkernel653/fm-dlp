import sys
from functools import lru_cache

from color_kiss import BLUE, RESET
from color_kiss.utils import error


@lru_cache(maxsize=1)
def get_version() -> str:
    """Get version from installed package metadata."""
    try:
        from importlib.metadata import version

        return version("fm-dlp")
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
        """Search for music tracks or videos on YouTube/YTMusic."""
        try:
            from fm_dlp.commands.search import Search
            from fm_dlp.utils.validator import validate_input

            validate_input(
                platform=platform,
                type=type,
                proxy=proxy,
                proxy_only_http=(platform == "yt-music"),
            )

            program = Search(query, limit, type, proxy)

            match platform:
                case "yt-video":
                    for video_info in program.yt_video():
                        print(video_info)
                case "yt-music":
                    for track_info in program.yt_music():
                        print(track_info)

        except Exception as e:
            sys.exit(error(str(e)))

    @app.command()
    def download(
        urls: str,
        codec: str | None = None,
        kbps: int = 256,
        max_concurrent: int = 5,
        quiet: bool = False,
        metadata: bool = True,
        cookies: str | None = None,
        proxy: str | None = None,
    ):
        """Download audio or video content from supported platforms."""
        try:
            from fm_dlp.utils.validator import (
                AUDIO_CODECS,
                DEFAULT_CODEC,
                validate_input,
                validate_with_shutil,
            )

            if codec is None:
                codec = DEFAULT_CODEC

            validate_input(
                url=urls,
                codec=codec,
                kbps=kbps,
                max_concurrent=max_concurrent,
                proxy=proxy,
            )

            if codec in AUDIO_CODECS:
                validate_with_shutil("ffmpeg", "FFmpeg")

            if codec == "wav" and metadata:
                metadata = False
                print(
                    f"{BLUE}Note: WAV format doesn't support metadata embedding{RESET}"
                )

            import asyncio

            from fm_dlp.commands.download import Download

            async def run_download():
                async with Download(
                    urls, codec, kbps, max_concurrent, quiet, metadata, cookies, proxy
                ) as downloader:
                    await downloader.download_all()

            asyncio.run(run_download())

        except Exception as e:
            sys.exit(error(str(e)))

    @app.command()
    def config(path: str):
        """Configure the application settings path."""
        try:
            from fm_dlp.utils.configer import set_path

            print(set_path(path))
        except Exception as e:
            sys.exit(error(str(e)))

    app.run()
