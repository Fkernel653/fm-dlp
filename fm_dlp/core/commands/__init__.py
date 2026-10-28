"""
Command modules for the YouTube Music/Video downloader and searcher.

This package contains the core command implementations that handle:
- Downloading audio/video content from YouTube and YouTube Music
- Searching for tracks, videos, albums, and playlists
- Configuration management for download preferences

Modules:
    downloader: Core download functionality with async/await support,
                concurrent downloads, and format conversion.
    search: Search across YouTube and YouTube Music with formatted results,
            raw output, or URL-only modes.

The downloader module provides the `Download` class and `run_downloader`
function for programmatic use, while the search module offers the `search`
function for quick lookups.
"""
