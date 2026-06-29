"""fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites."""

from fm_dlp.commands import update
from fm_dlp.commands.download import Download
from fm_dlp.commands.search import Search
from fm_dlp.utils import config, functions, validate

__all__ = ["Download", "Search", "update", "validate", "config", "functions"]
