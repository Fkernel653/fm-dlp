"""
ANSI color codes for terminal output formatting.

These constants provide consistent color styling across all modules of the application.
Each code is an ANSI escape sequence that changes text appearance in compatible terminals.
Colors are used to distinguish different types of information in the output, improving
readability and user experience.

Usage Example:
    from modules.colors import RED, GREEN, RESET
    print(f"{RED}Error message{RESET}")
    print(f"{GREEN}Success message{RESET}")

Note:
    - These escape sequences work on most Unix-like terminals (Linux, macOS)
    - Windows terminals may require ANSI support (Windows 10+ with VT sequences)
    - Not all terminals support the ITALIC style
"""

# Reset all formatting to default (removes all styles and colors)
# This should be used after applying any color or style to prevent bleeding
RESET = "\033[01;0m"

# Text styles - these modify the appearance regardless of color
BOLD = "\033[01;1m"      # Bold/Bright text - used for numbers and URLs
ITALIC = "\033[01;3m"    # Italic text (may not work in all terminals)

# Standard colors - each used consistently across the application
RED = "\033[01;31m"      # Error messages, warnings, and video URLs
GREEN = "\033[01;32m"    # Success messages, confirmations, and goodbye messages
YELLOW = "\033[01;33m"   # Warnings and cautions (duration field)
BLUE = "\033[01;34m"     # Information and dates (creation date field)
MAGENTA = "\033[01;35m"  # Metadata and channel names (channel field)
CYAN = "\033[01;36m"     # Titles and headings (video title field)

# Color Usage by Module:
#   searching.py: Uses all colors for formatted video information output
#   downloader.py: Uses RED for errors, GREEN for success messages
#   configer.py: Uses RED for errors, GREEN for success and configuration info
#   helper.py: No direct color usage
#   fm-dlp.py: No direct color usage (delegates to modules)