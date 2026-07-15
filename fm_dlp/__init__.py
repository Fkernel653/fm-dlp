"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from .commands.download import Download
from .commands.search import Search

__all__ = ["Download", "Search"]

__version__ = "4.4.0"
