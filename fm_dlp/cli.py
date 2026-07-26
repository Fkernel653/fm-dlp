"""
fm-dlp - Download music/video from YouTube, YTMusic, and 1000+ sites.

This module serves as the main entry point for the fm-dlp CLI application, providing
functionality to search YouTube/YTMusic for tracks and albums, download audio/video
content from over 1000+ platforms, and configure application settings.

The CLI is built using the argss library and offers three primary commands:
- search: Search for music tracks, albums, or videos on YouTube/YTMusic
- download: Download audio or video content from various supported platforms
- config: Configure the default download directory path

Features:
    - Search YouTube Music and YouTube with customizable result limits
    - Download from 1000+ platforms using yt-dlp backend
    - Multiple audio codec support (mp3, aac, flac, m4a, opus, vorbis, wav, alac)
    - Video format support (mp4, mov, mkv, webm, avi, flv)
    - Video-only download mode (without audio track)
    - Concurrent downloads with configurable job limits
    - Metadata embedding with thumbnails for audio files
    - Keep original files after conversion
    - Cookie-based authentication for platform-specific downloads
    - Colored terminal output for better user experience

Environment:
    - Platform-agnostic (Windows, macOS, Linux)
    - Requires ffmpeg for audio/video processing
    - Python 3.10+ with asyncio support

Usage Examples:
    fm-dlp config /path/to/download/folder
    fm-dlp search "Sewerslvt"
    fm-dlp download https://music.youtube.com/watch?v=y55fzyXZDSE

For more information, visit: https://github.com/Fkernel653/fm-dlp
"""


def main():
    """Main entry point for fm-dlp CLI."""
    import sys

    from arg_kiss import Argkiss

    from fm_dlp import __version__
    from fm_dlp.utils import echo, get_output
    from fm_dlp.utils.config.configer.path import get_path, set_path
    from fm_dlp.utils.validate import (
        validate_download,
        validate_ffmpeg,
        validate_search,
    )

    cli = Argkiss(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version=__version__,
    )

    # Global argument for disabling colored output
    cli.add_global_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output globally",
    )

    # Search command
    @cli.argument("query", help="Search query string")
    @cli.argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)",
    )
    @cli.argument(
        "-v",
        "--yt-video",
        action="store_true",
        help="Search for YouTube videos instead of music tracks",
    )
    @cli.argument(
        "-a",
        "--album",
        action="store_true",
        help="Search for albums instead of individual tracks",
    )
    @cli.argument(
        "-r",
        "--raw",
        action="store_true",
        help="Output results in raw format (Python dict representation)",
    )
    @cli.argument(
        "-u",
        "--only-url",
        action="store_true",
        help="Output only the URLs without any formatting",
    )
    @cli.command()
    def search(
        query: str,
        limit: int = 10,
        yt_video: bool = False,
        album: bool = False,
        raw: bool = False,
        only_url: bool = False,
        no_color: bool = False,
    ):
        """Search for music tracks or videos on YouTube/YTMusic."""
        color = not no_color

        validate_search(limit, color)

        from fm_dlp.commands.search import search

        for result in search(query, limit, yt_video, album, raw, only_url, color):
            echo(result, file=get_output(result))

    # Download command
    @cli.argument(
        "urls",
        help="Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).",
    )
    @cli.argument(
        "-c",
        "--codec",
        help="Audio codec or video container. Default depends on platform. For audio: mp3, aac, flac, m4a, opus, vorbis, wav, alac. For video: mp4, mov, mkv, webm, avi, flv.",
    )
    @cli.argument(
        "-K",
        "--kbps",
        type=int,
        default=256,
        help="Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size. (default: 256)",
    )
    @cli.argument(
        "-Q",
        "--quality",
        type=str,
        default="best",
        help="Video quality preset: best, worst, 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p, or custom height (e.g., 720). (default: best)",
    )
    @cli.argument(
        "-j",
        "--jobs",
        type=int,
        default=5,
        help="Maximum number of concurrent downloads. Increase for faster batch downloads. (default: 5)",
    )
    @cli.argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress yt-dlp output messages. Errors will still be shown.",
    )
    @cli.argument(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        help="Disable embedding metadata (title, artist, album) and thumbnail into audio files.",
    )
    @cli.argument(
        "-k",
        "--keep",
        action="store_true",
        help="Keep the original downloaded file after conversion/post-processing. Useful when you want to retain both the original and converted versions.",
    )
    @cli.argument(
        "-s", "--save", action="store_true", help="Saving settings (except URL)"
    )
    @cli.argument(
        "-u",
        "--use-config",
        action="store_true",
        help="Use saved parameters from config file as defaults.",
    )
    @cli.argument(
        "-p",
        "--path",
        help="Custom download directory path. Uses configured default if not specified.",
    )
    @cli.argument(
        "-v",
        "--only-video",
        action="store_true",
        help="Download a video file without audio track (video-only). Useful for editing, re-encoding, or when audio is not needed.",
    )
    @cli.argument(
        "-C",
        "--cookies",
        help="Path to cookies file (e.g., 'cookies.txt') for authenticated downloads, or browser name ('brave', 'chrome', 'chromium', 'edge', 'opera', 'vivaldi', 'whale', 'firefox', 'safari') to extract cookies from browser.",
    )
    @cli.command()
    def download(
        urls: str,
        codec: str | None = None,
        kbps: int = 256,
        quality: str = "best",
        jobs: int = 5,
        quiet: bool = False,
        metadata: bool = True,
        keep: bool = False,
        save: bool = False,
        use_config: bool = False,
        path: str | None = None,
        only_video: bool = False,
        cookies: str | None = None,
        no_color: bool = False,
    ):
        """Download audio or video content from supported platforms."""
        color = not no_color

        default_codec = "m4a" if sys.platform == "darwin" else "opus"
        codec = codec or default_codec
        path = path or get_path(color)

        validate_download(urls, codec, kbps, quality, jobs, path, cookies, color)
        validate_ffmpeg(color)

        import asyncio

        from fm_dlp.commands.downloader import run_downloader

        asyncio.run(
            run_downloader(
                url=urls,
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
        )

    # Config command
    @cli.argument(
        "path",
        help="Default directory path where downloaded files will be saved. Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').",
    )
    @cli.command()
    def config(path: str, no_color: bool = False):
        """Configure the application settings."""
        color = not no_color
        result = set_path(path, color)
        echo(result, file=get_output(result))

    try:
        cli.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
