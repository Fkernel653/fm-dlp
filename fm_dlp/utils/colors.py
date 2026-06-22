RESET = "\033[0m"

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"

_COLORS_ENABLED = True


def set_colors(enabled: bool):
    global _COLORS_ENABLED
    _COLORS_ENABLED = enabled


def is_colors_enabled() -> bool:
    return _COLORS_ENABLED


def success(text: str) -> str:
    """Format text as a success message.

    Adds 'Success: ' prefix and colors everything in bold green.

    Args:
        text (str): The message content.

    Returns:
        str: Formatted success message.
    """
    prefix = "SUCCESS: "
    if is_colors_enabled():
        return BOLD_GREEN + prefix + RESET + text
    else:
        return prefix + text


def error(text: str) -> str:
    """Format text as an error message.

    Adds 'Error: ' prefix and colors everything in bold red.

    Args:
        text (str): The message content.

    Returns:
        str: Formatted error message.
    """
    prefix = "ERROR: "
    if is_colors_enabled():
        return BOLD_RED + prefix + RESET + text
    else:
        return prefix + text


def info(text: str) -> str:
    """Format text as an info message.

    Adds 'Info: ' prefix and colors everything in bold cyan.

    Args:
        text (str): The message content.

    Returns:
        str: Formatted info message.
    """
    prefix = "INFO: "
    if is_colors_enabled():
        return BOLD_CYAN + prefix + RESET + text
    else:
        return prefix + text
