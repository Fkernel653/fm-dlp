"""
Help menu display module for the fm-dlp CLI application.

Provides the help menu text showing all available commands with their
arguments, usage examples, and descriptions. Displayed when the user
runs the 'help' command or provides no arguments to the CLI.
"""

from modules.colors import RESET, BOLD, GREEN, CYAN, YELLOW, MAGENTA, GRAY, RED


def message() -> str:
    """
    Generate the help menu text for the fm-dlp application.

    Returns:
        Formatted string containing all available commands with their usage instructions.
        Each command includes parameter descriptions and platform options.

    Command Details:
        search <query> [--limit=<n>] [--enable_filter=<bool>] [--variable=<platform>]
            - Searches for music on YouTube or SoundCloud
            - Parameters:
                query: Search term (required)
                limit: Max results, default 10
                enable_filter: Filter invalid results (true/false), default false
                variable: Platform selection - "youtube" or "soundcloud", default youtube

        download <url> [--cookies=<browser>]
            - Downloads audio from YouTube as M4A (256 kbps AAC)
            - Parameters:
                url: YouTube video URL (required)
                cookies: Browser for cookies - chrome, firefox, edge, etc. (optional)

        config <path>
            - Sets download directory (with path) or shows current config (without path)

        help
            - Displays this help message

    Note:
        - Download command requires FFmpeg installation for audio extraction
        - Config command must be used before downloading to set a valid directory
        - Search uses scrapetube (YouTube) or soundcloud package (SoundCloud)
        - Color output is enabled by default in compatible terminals
    """
    menu = f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗
║                     fm-dlp - Music Downloader                    ║
╚══════════════════════════════════════════════════════════════════╝{RESET}

{BOLD}{GREEN}USAGE:{RESET}
    {BOLD}fm-dlp <command> [arguments]{RESET}

{BOLD}{GREEN}COMMANDS:{RESET}

{BOLD}{YELLOW}search <query> [--limit=<n>] [--enable_filter=<bool>] [--variable=<platform>]{RESET}
    {GRAY}Search for music on YouTube or SoundCloud{RESET}
    {GRAY}Arguments:{RESET}
        {BOLD}query{RESET}               - Search term {RED}(required){RESET}
        {BOLD}--limit=<n>{RESET}         - Maximum results {GRAY}(default: 10){RESET}
        {BOLD}--enable_filter=<bool>{RESET} - Filter invalid results {GRAY}(default: false){RESET}
        {BOLD}--variable=<platform>{RESET}  - Platform: "youtube" or "soundcloud" {GRAY}(default: youtube){RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp search "Sewerslvt"{RESET}
        {CYAN}fm-dlp search "breakcore" --limit=5{RESET}
        {CYAN}fm-dlp search "ambient" --variable=soundcloud --limit=3{RESET}

{BOLD}{YELLOW}download <url> [--cookies=<browser>]{RESET}
    {GRAY}Download audio from YouTube as high-quality M4A (256 kbps AAC){RESET}
    {GRAY}Arguments:{RESET}
        {BOLD}url{RESET}                 - YouTube video URL {RED}(required){RESET}
        {BOLD}--cookies=<browser>{RESET} - Browser for cookies: chrome, firefox, edge {GRAY}(optional){RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp download https://youtu.be/dQw4w9WgXcQ{RESET}
        {CYAN}fm-dlp download https://youtube.com/watch?v=... --cookies=chrome{RESET}

{BOLD}{YELLOW}config <path>{RESET}
    {GRAY}Set download directory (with path) or view current config (without path){RESET}
    {GRAY}Examples:{RESET}
        {CYAN}fm-dlp config ~/Music/Downloads{RESET}
        {CYAN}fm-dlp config{RESET}

{BOLD}{YELLOW}help{RESET}
    {GRAY}Display this help message{RESET}

{BOLD}{GREEN}REQUIREMENTS:{RESET}
    {GRAY}• {RESET}{BOLD}FFmpeg{RESET}      {GRAY}(required for audio download){RESET}
    {GRAY}• {RESET}{BOLD}term_image{RESET}  {GRAY}(optional, for thumbnail previews in search results){RESET}

{BOLD}{MAGENTA}For issues or feature requests, please report on GitHub.{RESET}
"""
    return menu