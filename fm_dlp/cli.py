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


def main():

    import sys

    from argss import Argss

    from fm_dlp.utils.config import get_path, set_path
    from fm_dlp.utils.functions import echo
    from fm_dlp.utils.validate import (
        validate_download,
        validate_ffmpeg,
        validate_search,
    )

    cli = Argss(
        name="fm-dlp",
        description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms",
        version="4.2.0",
    )

    @cli.command()
    def search(
        query: str,
        limit: int = 10,
        yt_video: bool = False,
        album: bool = False,
        raw: bool = False,
        only_url: bool = False,
        color: bool = True,
    ):
        """Search for music tracks or videos on YouTube/YTMusic.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.
            yt_video: Search for YouTube videos instead of music tracks.
            album: Search for albums instead of individual tracks.
            raw: Output results in raw format (Python dict representation).
            only_url: Output only the URLs without any formatting.
            color: Colored output in search results.
        """
        if not validate_search(limit, color):
            return

        from fm_dlp.commands.search import search

        for result in search(query, limit, yt_video, album, raw, only_url, color):
            echo(result)

    @cli.command()
    def download(
        urls: str,
        codec: str | None = None,
        kbps: int = 256,
        jobs: int = 5,
        quiet: bool = False,
        metadata: bool = True,
        path: str | None = None,
        cookies: str | None = None,
        color: bool = True,
    ):
        """Download audio or video content from supported platforms.

        Args:
            urls: Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).
            codec: Audio codec or video container. Default depends on platform.
                  For audio: mp3, aac, flac, m4a, opus, vorbis, wav, alac.
                  For video: mp4, mov, mkv, webm, avi, flv.
            kbps: Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size.
            jobs: Maximum number of concurrent downloads. Increase for faster batch downloads.
            quiet: Suppress yt-dlp output messages. Errors will still be shown.
            metadata: Embed metadata (title, artist, album) and thumbnail into audio files.
            path: Custom download directory path. Uses configured default if not specified.
            cookies: Path to cookies file (e.g., 'cookies.txt') for authenticated downloads,
                    or browser name ('brave', 'chrome', 'chromium', 'edge', 'opera', 'vivaldi', 'whale', 'firefox', 'safari')
                    to extract cookies from browser.
            color: Colored output in download progress and status messages.
        """
        default_codec = "m4a" if sys.platform == "darwin" else "opus"
        codec = codec or default_codec
        path = path or get_path(color)

        if not validate_download(urls, codec, kbps, jobs, path, cookies, color):
            return

        if not validate_ffmpeg(color):
            return

        import asyncio

        from fm_dlp.commands.download import run_downloader

        asyncio.run(
            run_downloader(
                urls, codec, kbps, jobs, quiet, metadata, path, cookies, color
            )
        )

    @cli.command()
    def config(path: str, color: bool = True):
        """Configure the application settings.

        Args:
            path: Default directory path where downloaded files will be saved.
                 Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').
            color: Colored output in configuration messages.
        """
        echo(set_path(path, color))

    @cli.command()
    def update(color: bool = True):
        """Update fm-dlp to the latest version.

        This command automatically detects whether you're running:
        - A PyInstaller binary (.exe on Windows, no extension on macOS/Linux):
            Downloads the appropriate binary from GitHub Releases and replaces itself.
        - A Python script (source installation):
            Updates the package via pip or uv (whichever is available).

        The update process:
            1. Checks GitHub for the latest release tag
            2. If running as binary, downloads the matching executable for your OS
            3. If running as script, runs 'pip install --upgrade fm-dlp' or 'uv pip install --upgrade fm-dlp'
            4. Returns a success message with the new version number

        Args:
            color: Enable colored output in update messages (default: True).

        Error handling:
            - GitHub API connection failures
            - Missing binary assets for current OS
            - Permission denied (suggests admin/sudo)
            - Package installation failures (shows stderr)

        Note:
            - The binary update replaces the currently running executable
            - You may need to restart the application after updating
            - For script mode, uv is preferred if available (faster than pip)
        """
        from fm_dlp.commands.update import update

        echo(update(color))

    try:
        cli.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
