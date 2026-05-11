"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys
from typing import Optional, Tuple

from modules.colors import GREEN, RED, RESET

PROTOCOLS: Tuple[str, ...] = (
    "http://",
    "https://",
    "socks4://",
    "socks5://",
    "socks5h://",
)
HTTP_PROTOCOLS: Tuple[str, ...] = ("http://", "https://")
CODECS: Tuple[str, ...] = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
CONTAINERS: Tuple[str, ...] = ("mp4", "mov", "mkv", "webm", "avi", "flv")


def print_and_exit(text: str, error: bool = True) -> None:
    """Print colored message and exit."""
    color = RED if error else GREEN
    print(f"\n{color}{'❌' if error else ''} {text}{RESET}")
    sys.exit(1 if error else 0)


def validate_input(
    url: Optional[str] = None,
    codec: Optional[str] = None,
    proxy: Optional[str] = None,
    proxy_only_http: bool = False,
) -> None:
    """
    Validate URL, codec/container, and proxy.

    Args:
        url: YouTube URL (HTTP/HTTPS only).
        codec: Audio codec or video container.
        proxy: Proxy URL.
        proxy_only_http: If True, allow only HTTP/HTTPS for proxy.
    """
    allowed_proxy = HTTP_PROTOCOLS if proxy_only_http else PROTOCOLS

    if url is not None and not url.startswith(HTTP_PROTOCOLS):
        print_and_exit(f"Invalid URL: {url}")

    if codec is not None and codec not in CODECS and codec not in CONTAINERS:
        print_and_exit(
            f"Invalid codec/container: {codec}\n"
            f"   Audio codecs: {', '.join(CODECS)}\n"
            f"   Video containers: {', '.join(CONTAINERS)}"
        )

    if proxy is not None and not proxy.startswith(allowed_proxy):
        print_and_exit(
            f"Invalid proxy: {proxy}\n   Allowed: {', '.join(allowed_proxy)}"
        )


def main():
    from cyclopts import App

    fm_dlp = App(name="fm_dlp", version="2.1.3")

    @fm_dlp.command()
    def search(
        query: str,
        limit: int = 10,
        platform: Optional[str] = "yt-music",
        type: Optional[str] = "track",
        proxy: Optional[str] = None,
    ):
        """Search for music on YouTube.

        Args:
            query: Search query string.
            limit: Number of results to return.
            platform: Search platform - 'yt-video' or 'yt-music'.
            type: Content type - 'track' or 'album'.
            proxy: Proxy URL for requests.
                yt-video supports: http://, https://, socks4://, socks5://, socks5h://
                yt-music supports: http://, https://
                Example: 'socks5://127.0.0.1:9050'
        """
        from modules.search import Search

        program = Search(query, limit, type, proxy)

        match platform:
            case "yt-video":
                validate_input(proxy=proxy)
                for video_info in program.yt_video():
                    print(video_info)
            case "yt-music":
                validate_input(proxy=proxy, proxy_only_http=True)
                for track_info in program.yt_music():
                    print(track_info)
            case _:
                print_and_exit("Invalid platform")

    @fm_dlp.command()
    def download(
        urls: str,
        codec: Optional[str] = None,
        kbps: Optional[int] = 256,
        quiet: Optional[bool] = False,
        max_concurrent: Optional[int] = 5,
        metadata: Optional[bool] = True,
        cookies: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """Download audio or video from URLs.

        Args:
            urls: URL(s) - space or comma separated.
            codec: Audio codec (mp3, aac, flac, m4a, opus, vorbis, wav)
                or video container (mp4, mkv, webm, mov, avi, flv).
                Default: 'm4a' on macOS, 'opus' otherwise.
            kbps: Audio bitrate in kbps (64-320). Ignored for video downloads.
            quiet: Suppress yt-dlp output.
            max_concurrent: Maximum parallel downloads.
            metadata: Embed title, artist, album and thumbnail. Audio only.
            cookies: Browser to extract cookies from (chrome, firefox, edge, etc.).
            proxy: Proxy URL for requests.
                Supports: http://, https://, socks4://, socks5://, socks5h://
                Example: 'socks5://127.0.0.1:9050'
        """
        if codec is None:
            codec = "m4a" if sys.platform == "darwin" else "opus"

        validate_input(url=urls, codec=codec, proxy=proxy)

        if codec == "wav":
            metadata = False

        import asyncio

        from modules.download import Download

        asyncio.run(
            Download(
                urls, codec, kbps, quiet, max_concurrent, metadata, cookies, proxy
            ).download_all()
        )

    @fm_dlp.command()
    def config(path: str):
        """Set or display the download directory configuration.

        Args:
            path: Directory path for downloads. If empty, shows current setting.
        """
        from modules.configer import set_path

        print(set_path(path))

    @fm_dlp.command()
    def update():
        """Update fm-dlp to the latest stable version.

        Pulls the latest changes from the remote Git repository.
        Requires Git to be installed and accessible in PATH.
        """
        from modules.update import update_project

        print(update_project())

    fm_dlp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_and_exit("Goodbye!", False)
