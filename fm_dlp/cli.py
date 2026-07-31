"""
fm-dlp - Download music/video from YouTube, YTMusic, and 1000+ sites.

This module serves as the main entry point for the fm-dlp CLI application, providing
functionality to search YouTube/YTMusic for tracks and albums, download audio/video
content from over 1000+ platforms, and configure application settings.

The CLI is built using the argparse library and offers three primary commands:
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
    fm-dlp search "Sewerslvt" --limit 5
    fm-dlp download https://music.youtube.com/watch?v=y55fzyXZDSE --codec mp3 --kbps 320

For more information, visit: https://github.com/Fkernel653/fm-dlp
"""


def main():
    """Main entry point for fm-dlp CLI."""
    import argparse
    import sys

    from fm_dlp_core import echo, run_downloader, search
    from fm_dlp_core.utils.config.path import get_path, set_path

    from . import __version__
    from .parsers import (
        create_config_parser,
        create_download_parser,
        create_search_parser,
    )
    from .validate import validate_download, validate_ffmpeg, validate_search

    parser = argparse.ArgumentParser(
        prog="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output globally"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_search_parser(subparsers)
    create_download_parser(subparsers)
    create_config_parser(subparsers)

    args = parser.parse_args()
    color = not args.no_color

    try:
        if args.command == "search":
            validate_search(args.limit, color)

            for result in search(
                args.query,
                args.limit,
                args.yt_video,
                args.album,
                args.raw,
                args.only_url,
                color,
            ):
                echo(result)

        elif args.command == "download":
            path = args.path or get_path(color)

            if not args.codec:
                args.codec = "m4a" if sys.platform == "darwin" else "opus"

            validate_download(
                args.url,
                args.codec,
                args.kbps,
                args.quality,
                args.jobs,
                path,
                args.cookies,
                color,
            )

            validate_ffmpeg(color)

            import asyncio

            asyncio.run(
                run_downloader(
                    url=args.url,
                    codec=args.codec,
                    kbps=args.kbps,
                    quality=args.quality,
                    jobs=args.jobs,
                    quiet=args.quiet,
                    metadata=args.metadata,
                    keep=args.keep,
                    save=args.save,
                    use_config=args.use_config,
                    path=path,
                    only_video=args.only_video,
                    cookies=args.cookies,
                    color=color,
                )
            )

        elif args.command == "config":
            result = set_path(args.path, color)

            echo(result)

    except KeyboardInterrupt:
        sys.exit(0)
