"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from fm_dlp import utils

from .commands.download import Download
from .commands.search import Search

__all__ = ["Download", "Search", "utils"]

__version__ = "4.3.5"
