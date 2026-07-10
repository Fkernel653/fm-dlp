"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from .commands.download import Download
from .commands.search import Search
from .utils import colors, functions, validate
from .utils.config import configer
from .utils.config.path import Path

__all__ = ["Download", "Search", "validate", "configer", "Path", "functions", "colors"]

__version__ = "4.3.4"
