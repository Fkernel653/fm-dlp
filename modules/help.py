# help.py
"""
Help menu display module for fm-dlp CLI.
"""

from modules.colors import RESET, BOLD, GREEN, CYAN, YELLOW, MAGENTA, GRAY, RED


def message() -> str:
    """Generate the help menu text with all available commands."""
    menu = f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║                     fm-dlp - Music Downloader                    ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GREEN}USAGE:{RESET}
    {BOLD}fm-dlp <command> [arguments]{RESET}

{BOLD}{GREEN}COMMANDS:{RESET}

{BOLD}{YELLOW}search <query> [--limit=<n>] [--enable_filter=<bool>] [--variable=<platform>]{RESET}
    {GRAY}Search for music on YouTube or SoundCloud{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp search "Sewerslvt"{RESET}
        {CYAN}fm-dlp search "breakcore" --limit=5{RESET}

{BOLD}{YELLOW}download <url> [--ffmpeg=<bool>] [--codec=<format>] [--kbps=<bitrate>] [--cookies=<browser>]{RESET}
    {GRAY}Download audio from YouTube (default: M4A 256 kbps){RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp download https://youtu.be/dQw4w9WgXcQ{RESET}
        {CYAN}fm-dlp download https://youtu.be/... --codec=mp3 --kbps=192{RESET}

{BOLD}{YELLOW}config <path>{RESET}
    {GRAY}Set or view download directory{RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp config ~/Music/Downloads{RESET}
        {CYAN}fm-dlp config{RESET}

{BOLD}{YELLOW}help{RESET}
    {GRAY}Display this help message{RESET}

{BOLD}{GREEN}REQUIREMENTS:{RESET}
    {GRAY}• {RESET}{BOLD}FFmpeg{RESET}      {GRAY}(required for audio download){RESET}
    {GRAY}• {RESET}{BOLD}yt-dlp{RESET}      {GRAY}(required for downloads){RESET}

{BOLD}{MAGENTA}For issues or feature requests, please report on GitHub.{RESET}
"""
    return menu