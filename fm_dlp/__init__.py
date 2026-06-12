"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from .commands.download import Download
from .commands.search import Search
from .utils import configer, validator

__all__ = ["Download", "Search", "validator", "configer"]
