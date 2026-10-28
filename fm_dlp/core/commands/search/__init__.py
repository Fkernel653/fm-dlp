"""
Search module for discovering content on YouTube and YouTube Music.

This module provides search capabilities across YouTube and YouTube Music
platforms, supporting:
- YouTube video and playlist search via yt-dlp
- YouTube Music track and album search via ytmusicapi
- Formatted output with colors and structured tree layouts
- Raw dictionary output for programmatic processing
- URL-only output for piping to downloaders
- Configurable result limits and search filters

Classes:
    ResultFormatter: Format search results with metadata and colors
    BaseProvider: Abstract base class for search providers
    YouTubeProvider: YouTube video/playlist search implementation
    YouTubeMusicProvider: YouTube Music track/album search implementation
    Search: Main search handler that delegates to appropriate providers

Functions:
    search: Convenience function for quick searches with minimal setup
"""

from .formatters import ResultFormatter
from .providers import BaseProvider, YouTubeMusicProvider, YouTubeProvider
from .search import Search

__all__ = [
    "BaseProvider",
    "ResultFormatter",
    "Search",
    "YouTubeMusicProvider",
    "YouTubeProvider",
]
