"""
YouTube audio downloader module.

Handles downloading audio from YouTube videos using yt-dlp with FFmpeg post-processing.
Requires a valid configuration file with download path and optionally browser cookies.
"""

from modules.colors import RESET, RED, GREEN
from fake_useragent import UserAgent
from pathlib import Path
import json


class Download:
    """Manages audio download operations from YouTube URLs."""

    def __init__(self, url: str):
        """
        Initialize downloader with target URL.

        Args:
            url: YouTube video URL to download audio from
        """
        self.url = url

        self.ua = UserAgent().random  # Random user agent for anti-detection
        self.this_file_folder = Path(__file__).parent
        self.config_file = Path(self.this_file_folder).parent / "config.json"

    def validate_config_file(self) -> None:
        """Check if configuration file exists, exit with error if not found."""
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n"
            )
            return exit(1)

    def normal(self, cookies: str) -> None:
        """
        Download audio from YouTube video using standard yt-dlp method.

        Args:
            cookies: Browser name for cookie extraction (e.g., 'chrome', 'firefox')
                    or None if no cookies needed
        """
        self.validate_config_file()
        with open(self.config_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                saved_path = data.get("path")

                if not saved_path or not Path(saved_path).exists():
                    print(
                        f"{RED}\nDownload path '{saved_path}' does not exist or is invalid. "
                        f"Please reconfigure with 'config <path>'.{RESET}\n"
                    )
                    return exit(1)

            except json.JSONDecodeError:
                print(
                    f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.{RESET}\n"
                )
                return exit(1)

        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError, ExtractorError

        # yt-dlp configuration dictionary with all options
        opts = {
            "user_agent": self.ua,  # Rotate fingerprints to avoid detection
            "format": "bestaudio/best",  # Select highest quality audio stream
            "outtmpl": f"{saved_path}/%(title)s.%(ext)s",  # Save pattern: video_title.extension
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",  # Use FFmpeg for audio extraction
                    "preferredcodec": "m4a",  # Output format (AAC in MP4 container)
                    "preferredquality": "256",  # Bitrate in kbps (good quality/size balance)
                }
            ],
            "cookiesfrombrowser": (cookies,)
            if cookies
            else None,  # Browser cookies for age-restricted content
            "quiet": False,  # Show detailed progress in terminal
            "no_warnings": False,  # Display warnings for troubleshooting
        }

        try:
            # Context manager ensures proper cleanup of resources after download
            with YoutubeDL(opts) as ydl:
                # Download audio from the provided URL
                # ydl.download() expects a list, even for single videos
                ydl.download([self.url])
                print(f"{GREEN}\nDownload completed successfully!{RESET}\n")
                return exit(0)

        except DownloadError:
            # General download failure (network issues, unavailable video, age restriction, etc.)
            print(
                f"{RED}\nDownload error! The video may be unavailable, private, or restricted.{RESET}\n"
            )
            return exit(1)

        except ExtractorError:
            # Error extracting video information from YouTube's servers
            print(
                f"{RED}\nExtraction error! Unable to retrieve video information. "
                f"The video ID may be invalid or YouTube's API may have changed.{RESET}\n"
            )
            return exit(1)

        except KeyboardInterrupt:
            print(f"{GREEN}\nDownload cancelled. Goodbye!\n{RESET}")
            return exit(0)
