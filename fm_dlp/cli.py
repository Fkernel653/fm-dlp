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
    - Concurrent downloads with configurable job limits
    - Metadata embedding with thumbnails for audio files
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

import argparse
import sys

from . import __version__
from .utils import echo
from .utils.config.configer import get_path, set_path
from .utils.validate import validate_download, validate_ffmpeg, validate_search


def main():
    parser = argparse.ArgumentParser(
        prog="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output globally"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    search_parser = subparsers.add_parser(
        "search",
        help="Search for music tracks or videos on YouTube/YTMusic",
        description="Search for music tracks or videos on YouTube/YTMusic",
    )
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)",
    )
    search_parser.add_argument(
        "-v",
        "--yt-video",
        action="store_true",
        help="Search for YouTube videos instead of music tracks",
    )
    search_parser.add_argument(
        "-a",
        "--album",
        action="store_true",
        help="Search for albums instead of individual tracks",
    )
    search_parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Output results in raw format (Python dict representation)",
    )
    search_parser.add_argument(
        "-u",
        "--only-url",
        action="store_true",
        help="Output only the URLs without any formatting",
    )

    # download
    download_parser = subparsers.add_parser(
        "download",
        help="Download audio or video content from supported platforms",
        description="Download audio or video content from supported platforms",
    )
    download_parser.add_argument(
        "urls",
        help="Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).",
    )
    download_parser.add_argument(
        "-c",
        "--codec",
        help="Audio codec or video container. Default depends on platform. For audio: mp3, aac, flac, m4a, opus, vorbis, wav, alac. For video: mp4, mov, mkv, webm, avi, flv.",
    )
    download_parser.add_argument(
        "-k",
        "--kbps",
        type=int,
        default=256,
        help="Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size. (default: 256)",
    )
    download_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=5,
        help="Maximum number of concurrent downloads. Increase for faster batch downloads. (default: 5)",
    )
    download_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress yt-dlp output messages. Errors will still be shown.",
    )
    download_parser.add_argument(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        help="Disable embedding metadata (title, artist, album) and thumbnail into audio files.",
    )
    download_parser.add_argument(
        "-p",
        "--path",
        help="Custom download directory path. Uses configured default if not specified.",
    )
    download_parser.add_argument(
        "-C",
        "--cookies",
        help="Path to cookies file (e.g., 'cookies.txt') for authenticated downloads, or browser name ('brave', 'chrome', 'chromium', 'edge', 'opera', 'vivaldi', 'whale', 'firefox', 'safari') to extract cookies from browser.",
    )

    # config
    config_parser = subparsers.add_parser(
        "config",
        help="Configure the application settings",
        description="Configure the application settings",
    )
    config_parser.add_argument(
        "path",
        help="Default directory path where downloaded files will be saved. Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').",
    )

    args = parser.parse_args()

    color = not args.no_color

    try:
        if args.command == "search":
            if not validate_search(args.limit, color):
                return
            from .commands.search import search

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
            default_codec = "m4a" if sys.platform == "darwin" else "opus"
            codec = args.codec or default_codec
            path = args.path or get_path(color)

            if not validate_download(
                args.urls, codec, args.kbps, args.jobs, path, args.cookies, color
            ):
                return
            if not validate_ffmpeg(color):
                return

            import asyncio

            from .commands.download import run_downloader

            asyncio.run(
                run_downloader(
                    args.urls,
                    codec,
                    args.kbps,
                    args.jobs,
                    args.quiet,
                    args.metadata,
                    path,
                    args.cookies,
                    color,
                )
            )

        elif args.command == "config":
            echo(set_path(args.path, color))

    except KeyboardInterrupt:
        sys.exit(0)
