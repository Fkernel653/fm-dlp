RESET = "\033[0m"

BOLD_WHITE = "\033[37m"
GRAY = "\033[90m"

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"

colors_enabled = True


def set_colors(enabled: bool):
    global colors_enabled
    colors_enabled = enabled


def styled(text: str, color: str) -> str:
    """Apply ANSI color codes to text if color output is enabled."""
    if colors_enabled:
        return color + text + RESET
    return text


def success(text: str, prefix: str = "Success: ") -> str:
    """Format text as a success message with bold green coloring."""
    if colors_enabled:
        return BOLD_GREEN + prefix + RESET + text
    return prefix + text


def error(text: str, prefix: str = "Error: ") -> str:
    """Format text as an error message with bold red coloring."""
    if colors_enabled:
        return BOLD_RED + prefix + RESET + text
    return prefix + text


def info(text: str, prefix: str = "Info: ") -> str:
    """Format text as an informational message with bold cyan coloring."""
    if colors_enabled:
        return BOLD_CYAN + prefix + RESET + text
    return prefix + text
