"""Input validation module for fm-dlp CLI application."""

from color_kiss.utils import error, info

from .functions import echo

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS


def validate_with_shutil(target: str, name: str) -> bool:
    """Verify a system dependency is installed.

    Returns:
        True if dependency is found, False otherwise.
    """
    import shutil

    if shutil.which(target) is None:
        echo(error(f"{name} is not installed or not found in system PATH!"))
        echo(
            info(
                f"Please install {name} and ensure it's accessible from the command line."
            )
        )
        echo(info(f"Tip: Run '{target} --version' to verify installation."))
        return False
    return True


def validate_input(
    url: str | None = None,
    codec: str | None = None,
    kbps: int | None = None,
    jobs: int | None = None,
    limit: int | None = None,
    search_type: str | None = None,
) -> bool:
    """Validate all CLI input parameters.

    Returns:
        True if all parameters are valid, False otherwise.
    """

    # URLs
    if url is not None:
        if not isinstance(url, str):
            echo(error(f"URL must be a string, got {type(url).__name__}"))
            return False

        if not url.strip():
            echo(error("URL cannot be empty or whitespace only"))
            return False

        if not (url.startswith("http://") or url.startswith("https://")):
            echo(error(f"Invalid URL: '{url}'"))
            echo(info("Must start with 'http://' or 'https://'"))
            return False

    # Codec
    if codec is not None:
        if codec not in ALL_CODECS:
            echo(error(f"Invalid codec: '{codec}'"))
            echo(info(f"Allowed values: {', '.join(ALL_CODECS)}"))
            return False

    # Bitrate
    if kbps is not None:
        if not isinstance(kbps, int) or not (64 <= kbps <= 320):
            echo(error(f"Invalid bitrate: {kbps}"))
            echo(info("Must be an integer between 64 and 320."))
            return False

    # Jobs
    if jobs is not None:
        if not isinstance(jobs, int) or jobs < 1:
            echo(error(f"Invalid jobs: {jobs}"))
            echo(info("Must be an integer >= 1."))
            return False

    # Limit
    if limit is not None:
        if not isinstance(limit, int) or limit <= 0:
            echo(error(f"Invalid limit: {limit}"))
            echo(info("Must be a non-negative integer."))
            return False

    # Search type
    if search_type is not None:
        allowed = ("track", "album")
        if search_type not in allowed:
            echo(error(f"Invalid search type: '{search_type}'"))
            echo(info(f"Allowed values: {', '.join(allowed)}"))
            return False

    return True
