"""
Main entry point for the fm-dlp CLI application.

This module initializes the command-line interface using the Clite library
and defines all available commands: search, download, config, and help.
The application allows users to search for music on YouTube/SoundCloud and
download audio from YouTube videos.
"""

from clite import Clite
import asyncio

from modules.search import Search
from modules.download import Download
from modules.configer import configuring_path
from modules.help import message


# Initialize the CLI application with metadata
# This creates the command-line interface with the specified name and description
# The clite library will parse sys.argv and route to the appropriate command
fm_dlp = Clite(
    name="fm-dlp",
    description="A utility for searching and downloading music from YouTube, based on yt-dlp",
)


@fm_dlp.command()
def search(
    query: str,
    limit: int = 10,
    enable_filter: str = "false",
    variable: str = "youtube",
):
    """
    Search for music on YouTube or SoundCloud.

    Args:
        query: Search term to look for (e.g., artist name or song title)
        limit: Maximum number of results to display (default: 10)
        enable_filter: Filter out invalid results - accepts "true"/"false"/"1"/"yes"/"on" (default: "false")
        variable: Platform to search on - "youtube" or "soundcloud" (default: "youtube")

    Returns:
        None: Search results are printed directly to the console, including:
              - Thumbnail preview (if term_image is installed)
              - Result number and title
              - Channel/artist name
              - Metadata (date, views/duration for YouTube; date, duration for SoundCloud)
              - URL for playback or download

    Note:
        - YouTube search uses scrapetube library (no API key required)
        - SoundCloud search requires the soundcloud package
        - Results are displayed with ANSI color codes for better readability
        - The enable_filter parameter removes entries missing videoId or title
    """
    # Convert string parameter to boolean for internal use
    # Accepts various truthy string representations
    filter_bool = enable_filter.lower() in ["true", "1", "yes", "on"]
    program = Search(query, limit, filter_bool)

    if variable == "youtube":
        # Asynchronous YouTube search with 10-second timeout
        async def get_video_info():
            async for video_info in program.youtube():
                print(video_info)

        asyncio.run(get_video_info())

    elif variable == "soundcloud":
        # Asynchronous SoundCloud search with 30-second timeout
        async def get_track_info():
            async for track_info in program.soundcloud():
                print(track_info)

        asyncio.run(get_track_info())


@fm_dlp.command()
def download(url: str, cookies: str = None):
    """
    Download audio from a YouTube video.

    Args:
        url: YouTube video URL (e.g., https://youtu.be/... or https://www.youtube.com/watch?v=...)
        cookies: Browser name for cookie extraction (optional - chrome, firefox, edge, etc.)
                Required for age-restricted or private videos

    Returns:
        None: Download progress is displayed in the terminal. The audio file is saved
              as M4A format (256 kbps AAC) to the configured download directory.

    Note:
        - Requires FFmpeg to be installed on the system for audio extraction
        - Download directory must be configured first using the 'config' command
        - Uses yt-dlp for downloading with random user-agent rotation
        - Cookies parameter helps bypass age restrictions and rate limiting
    """
    program = Download(url)
    print(program.normal(cookies))


@fm_dlp.command()
def config(path: str):
    """
    Set or display the download directory configuration.

    Args:
        path: Directory path where downloaded audio files will be saved.
              If empty or omitted, displays the current configuration.

    Returns:
        None: Configuration status is printed directly to the console.
              Shows either confirmation of saved path or current settings.

    Note:
        - Configuration is stored in config.json in the project root
        - The path must exist on the filesystem (validated when retrieved)
        - Run this command before downloading to set a valid download location
        - Example: fm-dlp config ~/Music/Downloads
    """
    print(configuring_path(path))


@fm_dlp.command()
def help():
    """
    Display the help menu with usage instructions for all commands.

    This command prints a comprehensive help message showing all available
    commands, their arguments, and brief descriptions of what each command does.

    Returns:
        None: Help text is printed directly to the console.

    Note:
        This is also the default command shown when the user runs
        fm-dlp without any arguments or with invalid commands.
    """
    print(message())


if __name__ == "__main__":
    # Run the CLI application when this script is executed directly
    # This parses command-line arguments (sys.argv) and dispatches to the appropriate function
    # If no valid command is provided, clite automatically shows the help menu
    fm_dlp()