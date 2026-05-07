"""
CLI entry point for fm-dlp using cyclopts library.
Commands: search, download, config
"""

import sys


def main():
    from typing import Optional

    from cyclopts import App

    fm_dlp = App(name="fm-dlp", version="2.0.0")

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
            proxy: Proxy URL for requests (e.g., 'socks5://127.0.0.1:9050').
        """
        from modules.search import Search

        program = Search(query, limit, type, proxy)

        match platform:
            case "yt-video":
                for video_info in program.yt_video():
                    print(video_info)
            case "yt-music":
                for track_info in program.yt_music():
                    print(track_info)

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
        """Download audio or video from YouTube URLs.

        Args:
            urls: YouTube URL(s) - space or comma separated.
            codec: Audio codec (mp3, aac, flac, m4a, opus, vorbis, wav)
                or video container (mp4, mkv, webm, mov, avi, flv).
                Default: 'm4a' on macOS, 'opus' otherwise.
            kbps: Audio bitrate in kbps (64-320). Ignored for video downloads.
            quiet: Suppress yt-dlp output.
            max_concurrent: Maximum parallel downloads.
            metadata: Embed title, artist, album and thumbnail. Audio only.
            cookies: Browser to extract cookies from (chrome, firefox, edge, etc.).
            proxy: Proxy URL for requests (e.g., 'socks5://127.0.0.1:9050').
        """
        if codec is None:
            codec = "m4a" if sys.platform == "darwin" else "opus"

        if codec == "wav":
            metadata = False

        from asyncio import run

        from modules.download import Download

        program = Download(
            urls, codec, kbps, quiet, max_concurrent, metadata, cookies, proxy
        )
        run(program.download_all())

    @fm_dlp.command()
    def config(path: str):
        """Set or display the download directory configuration.

        Args:
            path: Directory path for downloads. If empty, shows current setting.
        """
        from modules.configer import configer

        print(configer(path))

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
        from modules.colors import GREEN, RESET

        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
