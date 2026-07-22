"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from .commands.downloader import Download
from .commands.search import Search, search

__all__ = ["Download", "Search", "search"]

__version__ = "4.4.4"
