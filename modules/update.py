import subprocess
from pathlib import Path
from shutil import which

from tqdm import tqdm

from modules.colors import GREEN, RED, RESET


def update_project():
    if which("git") is None:
        return f"{RED}Git is not installed!{RESET}"

    project_dir = Path(__file__).parent.parent

    try:
        with tqdm(
            total=1, desc="Updating project", bar_format="{desc}: {elapsed}"
        ) as pbar:
            result = subprocess.run(
                ["git", "-C", str(project_dir), "pull"],
                check=True,
                capture_output=True,
                text=True,
                shell=False,
            )
            pbar.update(1)

        # Показываем результат git pull
        if result.stdout:
            output = result.stdout.strip()
            return f"{GREEN}Project updated successfully!\n{output}{RESET}"
        return f"{GREEN}Project updated successfully!{RESET}"

    except subprocess.CalledProcessError as e:
        return f"{RED}Update failed: {e.stderr}{RESET}"
