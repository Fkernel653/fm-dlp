import subprocess
import sys
from pathlib import Path

from modules.utils.colors import GREEN, RED, RESET


def _progress_bar(
    current: int, total: int, description: str = "", width: int = 30
) -> str:
    """Create a simple progress bar string.

    Args:
        current: Current progress value.
        total: Total value for completion.
        description: Text to show before the bar.
        width: Width of the progress bar in characters.

    Returns:
        Progress bar string like: "Fetching... [##########    ] 75%"
    """
    filled = int(width * current / total)
    bar = "#" * filled + " " * (width - filled)
    percent = int(100 * current / total)

    desc_str = f"{description} " if description else ""
    return f"\r{desc_str}[{bar}] {percent}%"


def update_project():
    """Update the project via Git with a simple progress indicator."""
    project_dir = Path(__file__).parent.parent.parent  # modules/utils/ -> root

    # Check if it's a git repository
    try:
        subprocess.run(
            ["git", "-C", str(project_dir), "rev-parse", "--git-dir"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return f"{RED}Not a git repository!{RESET}"

    # Get current branch
    try:
        branch_result = subprocess.run(
            ["git", "-C", str(project_dir), "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        current_branch = branch_result.stdout.strip()
    except subprocess.CalledProcessError:
        return f"{RED}Failed to determine current branch!{RESET}"

    # Update with progress
    try:
        # Step 1: Fetch
        print(_progress_bar(0, 2, "Fetching latest changes"), end="")
        sys.stdout.flush()

        subprocess.run(
            ["git", "-C", str(project_dir), "fetch", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )

        print(_progress_bar(2, 2, "Fetching latest changes"))  # 100%
        sys.stdout.flush()

        # Step 2: Reset
        print(_progress_bar(0, 1, f"Resetting to origin/{current_branch}"), end="")
        sys.stdout.flush()

        subprocess.run(
            [
                "git",
                "-C",
                str(project_dir),
                "reset",
                "--hard",
                f"origin/{current_branch}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(_progress_bar(1, 1, f"Resetting to origin/{current_branch}"))
        sys.stdout.flush()

        return f"{GREEN}✓ Project updated successfully!{RESET}"

    except subprocess.CalledProcessError as e:
        print()  # New line after progress bar
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return f"{RED}Update failed: {error_msg}{RESET}"
