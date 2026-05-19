"""
Argument parser configuration for fm-dlp CLI.
"""

import argparse


def create_parser(version: str = "unknown") -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands.

    Args:
        version: Version string to display with --version flag.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="fm-dlp",
        description="fm-dlp is a CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    _add_search_parser(subparsers)
    _add_download_parser(subparsers)
    _add_config_parser(subparsers)

    return parser


def _add_search_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add search subcommand parser."""
    search_parser = subparsers.add_parser("search", help="Search for music on YouTube")
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Number of results to return (default: 10)",
    )
    search_parser.add_argument(
        "-p",
        "--platform",
        choices=["yt-video", "yt-music"],
        default="yt-music",
        help="Search platform (default: yt-music)",
    )
    search_parser.add_argument(
        "-t",
        "--type",
        choices=["track", "album"],
        default="track",
        help="Content type (default: track)",
    )
    search_parser.add_argument(
        "--proxy",
        default=None,
        help="Proxy URL. yt-video: http, https, socks4, socks5, socks5h. yt-music: http, https only. Example: socks5://127.0.0.1:9050",
    )


def _add_download_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add download subcommand parser."""
    download_parser = subparsers.add_parser(
        "download", help="Download audio or video from URLs"
    )
    download_parser.add_argument("urls", help="URL(s) - space or comma separated")
    download_parser.add_argument(
        "-c",
        "--codec",
        default=None,
        help="Audio codec or video container. Audio: mp3, aac, flac, m4a, opus, vorbis, wav. Video: mp4, mkv, webm, mov, avi, flv. Default: 'm4a' on macOS, 'opus' otherwise.",
    )
    download_parser.add_argument(
        "-k",
        "--kbps",
        type=int,
        default=256,
        help="Audio bitrate in kbps (64-320). Ignored for video (default: 256)",
    )
    download_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress yt-dlp output",
    )
    download_parser.add_argument(
        "--max-concurrent",
        type=int,
        default=5,
        help="Maximum parallel downloads (default: 5)",
    )
    download_parser.add_argument(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        help="Do not embed metadata and thumbnail (audio only)",
    )
    download_parser.set_defaults(metadata=True)
    download_parser.add_argument(
        "--cookies",
        default=None,
        help="Browser for cookies (chrome, firefox, edge, etc.)",
    )
    download_parser.add_argument(
        "--proxy", default=None, help="Proxy URL (http, https, socks4, socks5, socks5h)"
    )


def _add_config_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add config subcommand parser."""
    config_parser = subparsers.add_parser(
        "config", help="Set or display the download directory"
    )
    config_parser.add_argument(
        "path",
        nargs="?",
        default="",
        help="Directory path for downloads. Empty to show current",
    )
