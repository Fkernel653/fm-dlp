# download.py
"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from modules.colors import RESET, RED, GREEN
from fake_useragent import UserAgent
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    url: str
    ua = UserAgent().random
    this_file_folder = Path(__file__).parent
    config_file = Path(this_file_folder).parent / "config.json"

    def validate_config_file(self) -> None:
        """Check if config file exists, exit if not found."""
        if not self.config_file.exists():
            print(f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n")
            return exit(1)

    def saved_path(self) -> str:
        """Read and validate download path from config file."""
        import json

        with open(self.config_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                path = data.get("path")
                if not path or not Path(path).exists():
                    print(f"{RED}\nDownload path '{path}' does not exist or is invalid. Please reconfigure.{RESET}\n")
                    return exit(1)
                return path
            except json.JSONDecodeError:
                print(f"{RED}\nConfig file is corrupted! Please reconfigure.{RESET}\n")
                return exit(1)

    def normal(self, ffmpeg: str, codec: str, kbps: int, cookies: str) -> None:
        """Download audio using yt-dlp with FFmpeg processing."""
        self.validate_config_file()

        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError, ExtractorError

        opts = {
            "user_agent": self.ua,
            "format": "bestaudio/best",
            "outtmpl": f"{self.saved_path()}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
                "preferredquality": str(kbps),
            }],
            "cookiesfrombrowser": (cookies,) if cookies else None,
            "quiet": False,
            "no_warnings": False,
        }

        try:
            with YoutubeDL(opts) as ydl:
                ydl.download([self.url])
                print(f"{GREEN}\nDownload completed successfully!{RESET}\n")
                return exit(0)
        except DownloadError:
            print(f"{RED}\nDownload error! Video may be unavailable, private, or restricted.{RESET}\n")
            return exit(1)
        except ExtractorError:
            print(f"{RED}\nExtraction error! Unable to retrieve video information.{RESET}\n")
            return exit(1)
        except KeyboardInterrupt:
            print(f"{GREEN}\nDownload cancelled. Goodbye!\n{RESET}")
            return exit(0)