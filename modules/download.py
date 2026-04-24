"""
YouTube audio downloader using yt-dlp with FFmpeg post-processing.
"""

from dataclasses import dataclass
from pathlib import Path
import asyncio
from typing import AsyncGenerator
from yt_dlp import YoutubeDL

from modules.add_metadata import add_metadata
from modules.colors import RESET, BOLD, RED, GREEN, YELLOW, MAGENTA


@dataclass
class Download:
    """Manages audio download operations from YouTube URLs."""

    urls: str
    config_file = Path(__file__).parent.parent / "config.json"

    def __post_init__(self):
        """Validate requirements on initialization."""
        self._validate_ffmpeg()
        self._validate_config_file()

    def _validate_ffmpeg(self) -> None:
        """Check if FFmpeg is installed."""
        import shutil

        if shutil.which("ffmpeg") is None:
            print(f"{RED}FFmpeg not found in PATH! Please install FFmpeg.{RESET}")
            exit(1)

    def _validate_config_file(self) -> None:
        """Check if config file exists, exit if not found."""
        if not self.config_file.exists():
            print(
                f"{RED}\nConfig file not found!{RESET}\n"
                f"{YELLOW}Run: fm-dlp config /path/to/downloads{RESET}\n"
            )
            exit(1)

    def _withdrawal_of_the_path(self) -> str:
        """Read and validate download path from config file."""
        import json

        try:
            data = json.loads(self.config_file.read_text(encoding="utf-8"))
            path = data.get("path")
            if not path or not Path(path).exists():
                print(
                    f"{RED}\nDownload path '{path}' does not exist or is invalid. Please reconfigure.{RESET}\n"
                )
                exit(1)
            return path
        except json.JSONDecodeError:
            print(f"{RED}\nConfig file is corrupted! Please reconfigure.{RESET}\n")
            exit(1)

    def _find_downloaded_file(self, title: str, download_path: str, possible_extensions: list) -> Path | None:
        """Find the downloaded file by title after FFmpeg processing."""
        safe_title = "".join(c for c in title if c.isalnum() or c in " ,.-_()[]")
        
        for ext in possible_extensions:
            test_path = Path(download_path) / f"{safe_title}.{ext}"
            if test_path.exists():
                return test_path
        return None

    async def classic(
        self, codec: str, kbps: int, quiet: bool, cookies: str, proxy: str
    ) -> AsyncGenerator[str, None]:
        """Download audio using yt-dlp with FFmpeg processing."""

        download_path = self._withdrawal_of_the_path()
        possible_extensions = list(set([codec, "m4a", "mp3", "flac", "opus"]))
        
        loop = asyncio.get_event_loop()

        async def download_single_url(url: str) -> str:
            """Download single URL and add metadata."""
            
            def sync_download():
                info_opts = {
                    "proxy": proxy or None,
                    "cookiesfrombrowser": cookies or None,
                    "quiet": quiet,
                    "no_warnings": True,
                }
                
                try:
                    with YoutubeDL(info_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                except Exception as e:
                    return f"{RED}\nFailed to extract info: {e}{RESET}"
                
                if not info:
                    return f"{RED}\nFailed to get video info{RESET}"
                
                entries = info.get("entries", [info])
                
                results = []
                for entry in entries:
                    if not entry:
                        continue
                    
                    video_url = entry.get("webpage_url") or entry.get("url") or url
                    title = entry.get("title", "Unknown")
                    
                    opts = {
                        "proxy": proxy or None,
                        "format": "bestaudio/best",
                        "outtmpl": f"{download_path}/%(title)s.%(ext)s",
                        "writethumbnail": True,
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": codec,
                                "preferredquality": str(kbps),
                            },
                            {"key": "EmbedThumbnail"},
                        ],
                        "cookiesfrombrowser": cookies or None,
                        "quiet": quiet,
                        "no_warnings": True,
                    }
                    
                    try:
                        with YoutubeDL(opts) as ydl:
                            ydl.download([video_url])
                        
                        file_path = self._find_downloaded_file(title, download_path, possible_extensions)
                        
                        if file_path and file_path.exists():
                            channel = entry.get("channel", "")
                            artist = entry.get("uploader") or channel or "Unknown"
                            album = entry.get("album") or channel or "Unknown"
                            
                            try:
                                add_metadata(
                                    file=file_path,
                                    codec=codec,
                                    title=title,
                                    artist=artist,
                                    album=album,
                                )
                                results.append(f"{GREEN}\n✓ {title}{RESET}")
                            except Exception as meta_err:
                                results.append(f"{YELLOW}\n⚠ {title} (metadata failed: {meta_err}){RESET}")
                        else:
                            results.append(f"{RED}\n✗ {title} (file not found){RESET}")
                            
                    except Exception as e:
                        results.append(f"{RED}\n✗ {title} - Error: {e}{RESET}")
                
                return "\n".join(results) if results else f"{RED}\nNothing downloaded{RESET}"

            print(f"{YELLOW}\nDownloading: {RESET}{BOLD}{url}{RESET}")
            result = await loop.run_in_executor(None, sync_download)
            return result

        urls_list = self.urls.split()
        
        if not urls_list:
            yield f"{RED}\nNo URLs provided{RESET}"
            return

        tasks = [asyncio.create_task(download_single_url(url)) for url in urls_list]

        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            yield result