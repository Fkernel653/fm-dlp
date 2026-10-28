"""
Downloader module for extracting audio and video from YouTube/YouTube Music.

This module provides the core download functionality with support for:
- Audio extraction in various formats (mp3, m4a, flac, wav, opus, etc.)
- Video downloading with quality selection
- Concurrent downloads with configurable job count
- Metadata embedding (tags and thumbnails)
- Persistent configuration for download preferences
- Cookie-based authentication for private/age-restricted content

Classes:
    Download: Main async downloader class with context manager support
    DownloadConfig: Configuration container for download settings
    DownloadParams: Data container for all download configuration parameters.
    OptionsBuilder: yt-dlp options builder with format/quality handling
    URLParser: Parse single URLs or bulk imports from text files

Functions:
    run_downloader: Async entry point for running downloads with given parameters
"""

from .config import DownloadConfig
from .downloader import Download, run_downloader
from .options_builder import OptionsBuilder
from .params import DownloadParams
from .url_parser import URLParser

__all__ = [
    "Download",
    "DownloadConfig",
    "DownloadParams",
    "OptionsBuilder",
    "URLParser",
    "run_downloader",
]
