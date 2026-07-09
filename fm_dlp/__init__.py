"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from fm_dlp.commands.download import Download
from fm_dlp.commands.search import Search
from fm_dlp.utils import functions, validate
from fm_dlp.utils.config import configer
from fm_dlp.utils.config.path import Path

__all__ = ["Download", "Search", "validate", "configer", "Path", "functions"]

__version__ = "4.3.3"
