"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Optional, Tuple

from modules.colors import GREEN, RED, RESET

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
CODECS: Tuple[str, ...] = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
CONTAINERS: Tuple[str, ...] = ("mp4", "mov", "mkv", "webm", "avi", "flv")
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


def _validate_url(url: str) -> None:
    """Validate YouTube URL format and scheme."""
    if not url.startswith(HTTP_PROTOCOLS):
        raise URLValidationError(
            f"Invalid URL: '{url}'\n"
            f"   URL must start with {RED}http://{RESET} or {RED}https://{RESET}\n"
            f"   Example: {GREEN}https://www.youtube.com/watch?v=dQw4w9WgXcQ{RESET}"
        )
    if len(url) < 10 or "." not in url:
        raise URLValidationError(
            f"URL appears malformed: '{url}'\n   Please provide a complete YouTube URL"
        )


def _validate_codec(codec: str) -> None:
    """Validate codec/container against supported formats."""
    if codec not in CODECS and codec not in CONTAINERS:
        raise CodecValidationError(
            f"Invalid codec/container: {RED}'{codec}'{RESET}\n"
            f"   {GREEN}Audio codecs{RESET}: {', '.join(CODECS)}\n"
            f"   {GREEN}Video containers{RESET}: {', '.join(CONTAINERS)}\n"
            f"   Tip: Use '{DEFAULT_CODEC}' for best quality audio"
        )


def _validate_numeric(
    value: int, min_val: int, max_val: int, label: str, unit: str = ""
) -> None:
    """Generic numeric range validator.

    Args:
        value: Value to validate.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
        label: Human-readable parameter name.
        unit: Unit of measurement (e.g., 'kbps').
    """
    unit_str = f" {unit}" if unit else ""
    if value < min_val or value > max_val:
        raise ValidationError(
            f"Invalid {label}: {RED}{value}{unit_str}{RESET}\n"
            f"   {label.capitalize()} must be between {min_val} and {max_val}{unit_str}"
        )


def _validate_proxy(proxy: str, allowed_protocols: Tuple[str, ...]) -> None:
    """Validate proxy URL format and allowed protocols."""
    if not proxy.startswith(allowed_protocols):
        raise ProxyValidationError(
            f"Invalid proxy URL: {RED}'{proxy}'{RESET}\n"
            f"   Allowed protocols: {', '.join(allowed_protocols)}\n"
            f"   Examples:\n"
            f"     • {GREEN}http://127.0.0.1:8080{RESET}\n"
            f"     • {GREEN}socks5://127.0.0.1:9050{RESET}\n"
            f"   Format: protocol://host:port"
        )
    # Validate proxy structure (protocol://host:port)
    try:
        host_port = proxy.split("://", 1)[1]
        if ":" not in host_port:
            raise ProxyValidationError(
                f"Proxy missing port number: {RED}'{proxy}'{RESET}\n"
                f"   Format: protocol://host:port\n"
                f"   Example: {GREEN}socks5://127.0.0.1:9050{RESET}"
            )
    except IndexError:
        raise ProxyValidationError(
            f"Malformed proxy URL: {RED}'{proxy}'{RESET}\n"
            f"   Format: protocol://host:port\n"
            f"   Example: {GREEN}http://127.0.0.1:8080{RESET}"
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
    """Validate all CLI input parameters.

    Args:
        url: YouTube URL to validate.
        codec: Audio codec or video container.
        kbps: Audio bitrate in kbps (64-320).
        max_concurrent: Maximum parallel downloads (≥1).
        limit: Search result limit (≥0).
        platform: Search platform ('yt-video' or 'yt-music').
        type: Content type ('track' or 'album').
        proxy: Proxy URL.
        proxy_only_http: Restrict proxy to HTTP/HTTPS only.

    Raises:
        URLValidationError: Invalid URL.
        CodecValidationError: Invalid codec/container.
        ValidationError: Invalid numeric parameter.
        PlatformError: Invalid platform.
        ProxyValidationError: Invalid proxy.
    """
    # Validate URL
    if url is not None:
        _validate_url(url)

    # Validate codec/container
    if codec is not None:
        _validate_codec(codec)

    # Validate numeric parameters
    if kbps is not None:
        _validate_numeric(kbps, 64, 320, "bitrate", "kbps")
    if max_concurrent is not None:
        _validate_numeric(max_concurrent, 1, float("inf"), "concurrent downloads")
    if limit is not None:
        _validate_numeric(limit, 0, float("inf"), "limit")

    # Validate content type
    if type is not None and type not in TYPE_SEARCHING:
        raise ValidationError(
            f"Invalid type: {RED}'{type}'{RESET}\n"
            f"   Available types: {', '.join(TYPE_SEARCHING)}"
        )

    # Validate platform
    if platform is not None and platform not in PLATFORMS:
        raise PlatformError(
            f"Invalid platform: {RED}'{platform}'{RESET}\n"
            f"   Available platforms:\n"
            f"     • {GREEN}yt-video{RESET}  - Search YouTube videos\n"
            f"     • {GREEN}yt-music{RESET}  - Search YouTube Music"
        )

    # Validate proxy
    if proxy is not None:
        allowed_protocols = HTTP_PROTOCOLS if proxy_only_http else PROTOCOLS
        _validate_proxy(proxy, allowed_protocols)
