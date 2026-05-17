"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Optional, Tuple

from modules.utils.colors import RED, RESET

# Constants
PROTOCOLS: Tuple[str, ...] = (
    "http://",
    "https://",
    "socks4://",
    "socks5://",
    "socks5h://",
)
HTTP_PROTOCOLS: Tuple[str, ...] = ("http://", "https://")
TYPE_SEARCHING: Tuple[str, ...] = ("track", "album")
PLATFORMS: Tuple[str, ...] = ("yt-video", "yt-music")
AUDIO_CODECS: Tuple[str, ...] = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
VIDEO_CONTAINERS: Tuple[str, ...] = ("mp4", "mov", "mkv", "webm", "avi", "flv")
DEFAULT_CODEC = "m4a" if sys.platform == "darwin" else "opus"


# Custom Exceptions
class ValidationError(ValueError):
    """Base exception for all input validation errors."""


class URLValidationError(ValidationError):
    """Invalid or malformed URL."""


class CodecValidationError(ValidationError):
    """Unsupported audio codec or video container."""


class ProxyValidationError(ValidationError):
    """Invalid proxy URL format or protocol."""


class PlatformError(ValidationError):
    """Invalid platform selection."""


class DependencyError(ValidationError):
    """Required system dependency (ffmpeg, git) not found in PATH."""


def validate_with_shutil(target: str, text: str) -> None:
    """Verify a system dependency is installed and accessible.

    Args:
        target: Executable name to check (e.g., 'ffmpeg', 'git').
        text: Human-readable name for error messages (e.g., 'FFmpeg').

    Raises:
        DependencyError: If the executable is not found in system PATH.
    """
    import shutil

    if shutil.which(target) is None:
        raise DependencyError(
            f"{RED}{text} is not installed or not found in system PATH!{RESET}\n"
            f"Please install {text} and ensure it's accessible from the command line.\n"
            f"Tip: Run '{RED}{target} --version{RESET}' to verify installation."
        )


def validate_input(
    url: Optional[str] = None,
    codec: Optional[str] = None,
    kbps: Optional[int] = None,
    max_concurrent: Optional[int] = None,
    limit: Optional[int] = None,
    platform: Optional[str] = None,
    type: Optional[str] = None,
    proxy: Optional[str] = None,
    proxy_only_http: bool = False,
) -> None:
    """Validate all CLI input parameters."""

    if url is not None:
        if not url.startswith(HTTP_PROTOCOLS) or len(url) < 10 or "." not in url:
            raise URLValidationError(
                f"Invalid URL: '{url}'\n"
                f"   URL must start with http:// or https://\n"
                f"   Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )

    if (
        codec is not None
        and codec not in AUDIO_CODECS
        and codec not in VIDEO_CONTAINERS
    ):
        raise CodecValidationError(
            f"Invalid codec/container: '{codec}'\n"
            f"   Audio codecs: {', '.join(AUDIO_CODECS)}\n"
            f"   Video containers: {', '.join(VIDEO_CONTAINERS)}"
        )

    if kbps is not None and not (64 <= kbps <= 320):
        raise ValidationError(
            f"Invalid bitrate: {kbps} kbps\n   Bitrate must be between 64 and 320 kbps"
        )

    if max_concurrent is not None and max_concurrent < 1:
        raise ValidationError(
            f"Invalid concurrent downloads: {max_concurrent}\n   Must be at least 1"
        )

    if limit is not None and limit < 0:
        raise ValidationError(f"Invalid limit: {limit}\n   Limit must be non-negative")

    if type is not None and type not in TYPE_SEARCHING:
        raise ValidationError(
            f"Invalid type: '{type}'\n   Available types: {', '.join(TYPE_SEARCHING)}"
        )

    if platform is not None and platform not in PLATFORMS:
        raise PlatformError(
            f"Invalid platform: '{platform}'\n"
            f"   Available platforms: yt-video, yt-music"
        )

    if proxy is not None:
        allowed_protocols = HTTP_PROTOCOLS if proxy_only_http else PROTOCOLS
        if not proxy.startswith(allowed_protocols):
            raise ProxyValidationError(
                f"Invalid proxy URL: '{proxy}'\n"
                f"   Allowed protocols: {', '.join(allowed_protocols)}"
            )
