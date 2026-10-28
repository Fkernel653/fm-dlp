"""
fm-dlp — Python CLI wrapper over yt-dlp.

This module serves as the main entry point for the fm-dlp CLI application, providing
functionality to search YouTube/YTMusic for tracks and albums, download audio/video
content from over 1000+ platforms, and configure application settings.

The CLI is built using the argparse library and offers three primary commands:
- config: Configure the default download directory path
- search: Search for music tracks, albums, or videos on YouTube/YTMusic
- download: Download audio or video content from various supported platforms

Features:
    - Search YouTube Music and YouTube with customizable result limits
    - Download from 1000+ platforms using yt-dlp backend
    - Multiple audio codec support (mp3, aac, flac, m4a, opus, vorbis, wav, alac)
    - Video format support (mp4, mov, mkv, webm, avi, flv)
    - Video-only download mode (without audio track)
    - Concurrent downloads with configurable job limits
    - Metadata embedding with thumbnails for audio files
    - Keep original files after conversion
    - Cookie-based authentication for platform-specific downloads
    - Colored terminal output for better user experience

Environment:
    - Python 3.11+ with tomllib support
    - Platform-agnostic (Windows, macOS, Linux)
    - Requires ffmpeg for audio/video processing (required for conversion)

Usage Examples:
    fm-dlp config ~/Music
    fm-dlp search "query"
    fm-dlp download "URL"

For more information, visit: https://github.com/Fkernel653/fm-dlp
"""
