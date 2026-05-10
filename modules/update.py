import shutil
import subprocess
from pathlib import Path

from tqdm import tqdm

from modules.colors import GREEN, RED, RESET


def update_project():
    if shutil.which("git") is None:
        return f"{RED}Git is not installed!{RESET}"

    project_dir = Path(__file__).parent.parent

    try:
        subprocess.run(
            ["git", "-C", str(project_dir), "rev-parse", "--git-dir"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return f"{RED}Not a git repository!{RESET}"

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
        with tqdm(total=2, desc="Updating project") as pbar:
            pbar.set_description("Fetching latest changes")
            subprocess.run(
                ["git", "-C", str(project_dir), "fetch", "origin"],
                check=True,
                capture_output=True,
                text=True,
            )
            pbar.update(1)

            pbar.set_description(f"Resetting to origin/{current_branch}")
            reset_result = subprocess.run(
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
            pbar.update(1)

            if reset_result.stdout:
                output = reset_result.stdout.strip()
                return f"{GREEN}Project updated successfully!\n{output}{RESET}"
            return f"{GREEN}Project updated successfully!{RESET}"

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return f"{RED}Update failed: {error_msg}{RESET}"
