# download.py
"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from modules.colors import RESET, RED, GREEN, YELLOW
from modules.add_metadata import add_metadata
from dataclasses import dataclass
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError
from fake_useragent import UserAgent


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    url: str
    ua = UserAgent().random
    this_file_folder = Path(__file__).parent
    config_file = Path(this_file_folder).parent / "config.json"  # config one level up

    def validate_config_file(self) -> None:
        """Check if config file exists, exit if not found."""
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found! Please set download path first using 'config <path>'.{RESET}\n"
            )
            return exit(1)

    def saved_path(self) -> str:
        """Read and validate download path from config file."""
        import json

        with open(self.config_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                path = data.get("path")
                if not path or not Path(path).exists():
                    print(
                        f"{RED}\nDownload path '{path}' does not exist or is invalid. Please reconfigure.{RESET}\n"
                    )
                    return exit(1)
                return path
            except json.JSONDecodeError:
                print(f"{RED}\nConfig file is corrupted! Please reconfigure.{RESET}\n")
                return exit(1)

    def normal(self, ffmpeg: str, codec: str, kbps: int, cookies: str) -> None:
        """Download audio using yt-dlp with FFmpeg processing."""
        self.validate_config_file()

        opts = {
            "user_agent": self.ua,
            "format": "bestaudio/best",  # best available audio quality
            "outtmpl": f"{self.saved_path()}/%(title)s.%(ext)s",  # output filename template
            "writethumbnail": True,  # download thumbnail for embedding
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",  # convert to target codec
                    "preferredcodec": codec,
                    "preferredquality": str(kbps),
                },
                {
                    "key": "EmbedThumbnail",  # embed thumbnail into audio file
                },
            ],
            "cookiesfrombrowser": (cookies,)
            if cookies
            else None,  # use browser cookies for auth
            "quiet": False,
            "no_warnings": False,
        }

        try:
            with YoutubeDL(opts) as ydl:
                # Extract video info without downloading
                info = ydl.extract_info(self.url, download=False)

                if not info:
                    raise ExtractorError("No info extracted")

                # Perform actual download with post-processing
                ydl.process_info(info)

                filename = ydl.prepare_filename(info)  # get expected output path

                print(f"{GREEN}\nDownload completed successfully!{RESET}")

            # Verify file exists after download
            file_path = Path(filename)
            if not file_path.exists():
                print(f"{RED}\nError: File not found at {file_path}{RESET}")
                return exit(1)

            # Extract metadata from video info
            title = info.get("title", "Unknown Title")
            artist = info.get("uploader", info.get("channel", "Unknown Artist"))
            album = info.get("album", info.get("channel"))

            # Add metadata tags to downloaded file
            result = add_metadata(
                file=file_path, codec=codec, title=title, artist=artist, album=album
            )

            if result:
                return f"{GREEN}Metadata added successfully!{RESET}\n"
            else:
                return f"{YELLOW}\nFile downloaded but metadata could not be added{RESET}\n"

        except DownloadError:
            print(
                f"{RED}\nDownload error! Video may be unavailable, private, or restricted.{RESET}\n"
            )
            return exit(1)
        except ExtractorError:
            print(
                f"{RED}\nExtraction error! Unable to retrieve video information.{RESET}\n"
            )
            return exit(1)
        except KeyboardInterrupt:
            print(f"{GREEN}\nDownload cancelled. Goodbye!\n{RESET}")
            return exit(0)
