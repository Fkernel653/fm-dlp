"""
Utility modules for the fm-dlp core package.

This package provides shared utilities used across the application including:
- Color management and styled terminal output with ANSI escape codes
- Codec and container format constants for media processing
- Terminal output helper functions with standardized formatting

The `colors` submodule provides comprehensive color formatting for terminal
output with both predefined styles and a flexible `styled()` function for
custom formatting.
"""

import sys
from typing import TextIO

from .colors import (
    BOLD_CYAN,
    BOLD_GREEN,
    BOLD_RED,
    BOLD_WHITE,
    BOLD_YELLOW,
    GRAY,
    RESET,
    error,
    info,
    set_colors,
    styled,
    success,
)

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS
VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print a message to the specified output stream with a newline."""
    file.write(text + "\n")


def echo_error(text: str, exit: bool = True) -> None:
    """Print an error message to stderr and terminate execution."""
    echo(error(text), file=sys.stderr)
    if exit:
        sys.exit(1)


__all__ = [
    "ALL_CODECS",
    "AUDIO_CODECS",
    "BOLD_CYAN",
    "BOLD_GREEN",
    "BOLD_RED",
    "BOLD_WHITE",
    "BOLD_YELLOW",
    "GRAY",
    "RESET",
    "VIDEO_CONTAINERS",
    "VIDEO_CONTAINER_AUDIO_MAP",
    "echo",
    "echo_error",
    "error",
    "info",
    "set_colors",
    "styled",
    "success",
]
