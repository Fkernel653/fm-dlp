"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Optional

from color_kiss import RED, RESET

# Constants
PROTOCOLS = ("http://", "https://", "socks4://", "socks5://", "socks5h://")
HTTP_PROTOCOLS = ("http://", "https://")
TYPE_SEARCHING = ("track", "album")
PLATFORMS = ("yt-video", "yt-music")
AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
DEFAULT_CODEC = "m4a" if sys.platform == "darwin" else "opus"


class ValidationError(ValueError):
    """Base validation error."""


def validate_with_shutil(target: str, text: str) -> None:
    """Verify a system dependency is installed."""
    import shutil

    if shutil.which(target) is None:
        raise ValidationError(
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

    checks = []

    if url is not None:
        if not url.startswith(HTTP_PROTOCOLS) or len(url) < 10 or "." not in url:
            checks.append(
                f"Invalid URL: '{url}'\n"
                f"   URL must start with http:// or https://\n"
                f"   Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )

    if codec is not None and codec not in AUDIO_CODECS + VIDEO_CONTAINERS:
        checks.append(
            f"Invalid codec/container: '{codec}'\n"
            f"   Audio codecs: {', '.join(AUDIO_CODECS)}\n"
            f"   Video containers: {', '.join(VIDEO_CONTAINERS)}"
        )

    if kbps is not None and not (64 <= kbps <= 320):
        checks.append(
            f"Invalid bitrate: {kbps} kbps\n   Must be between 64 and 320 kbps"
        )

    if max_concurrent is not None and max_concurrent < 1:
        checks.append(
            f"Invalid concurrent downloads: {max_concurrent}\n   Must be at least 1"
        )

    if limit is not None and limit < 0:
        checks.append(f"Invalid limit: {limit}\n   Must be non-negative")

    if type is not None and type not in TYPE_SEARCHING:
        checks.append(
            f"Invalid type: '{type}'\n   Available types: {', '.join(TYPE_SEARCHING)}"
        )

    if platform is not None and platform not in PLATFORMS:
        checks.append(
            f"Invalid platform: '{platform}'\n"
            f"   Available platforms: yt-video, yt-music"
        )

    if proxy is not None:
        allowed = HTTP_PROTOCOLS if proxy_only_http else PROTOCOLS
        if not proxy.startswith(allowed):
            checks.append(
                f"Invalid proxy URL: '{proxy}'\n"
                f"   Allowed protocols: {', '.join(allowed)}"
            )

    if checks:
        raise ValidationError("\n" + "\n".join(checks))
