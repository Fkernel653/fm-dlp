"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from .commands.downloader import Download, run_downloader
from .commands.search import Search, search

__all__ = ["Download", "Search", "run_downloader", "search"]

__version__ = "4.4.5"
