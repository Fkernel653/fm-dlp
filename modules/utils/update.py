import subprocess
from pathlib import Path

from modules.utils.colors import GREEN, RED, RESET


def update_project():
    """Update the project via Git with a simple progress indicator."""
    project_dir = Path(__file__).parent.parent.parent

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

    try:
        subprocess.run(
            ["git", "-C", str(project_dir), "fetch", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )

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

        return f"{GREEN}✓ Project updated successfully!{RESET}"

    except subprocess.CalledProcessError as e:
        return f"{RED}Update failed: {e}{RESET}"
