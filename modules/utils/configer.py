"""
Persistent download path storage using JSON config file.
"""

import json
from pathlib import Path

from modules.utils.colors import BLUE, GRAY, GREEN, RED, RESET, YELLOW

_CONFIG_FILE = Path(__file__).parent.parent.parent / "config.json"
KEY_NAME = "path"


def set_path(path: str) -> str:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    try:
        input_path = Path(path)
        if not input_path.is_dir():
            return f"{RED}Please enter the correct path!{RESET}"

        path_str = str(input_path)

        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({KEY_NAME: path_str}, f, ensure_ascii=False, indent=4)

        return f"{GREEN}\nConfiguration saved successfully!{RESET}\n{YELLOW}Path: {RESET}{path_str}\n{BLUE}Config file: {RESET}{_CONFIG_FILE}"
    except Exception as e:
        return f"{RED}\nError saving configuration: {e}{RESET}"


def get_path() -> str | None:
    import sys

    home_path = str(Path.home())
    if not _CONFIG_FILE.exists():
        print(
            f"{RED}\nConfig file not found!{RESET}\n{GRAY}Run: fm-dlp config /path or continue in the home directory{RESET}\n"
        )
        user_input = str(
            input(
                f"{BLUE}Do you want to continue in the home directory? (Y/n): {RESET}"
            )
        )
        if user_input.lower() == "y":
            return home_path
        else:
            sys.exit(1)

    data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    download_path = data.get(KEY_NAME)
    if not download_path or not Path(download_path).is_dir():
        print(f"{RED}\nDownload path does not exist.{RESET}")
        sys.exit(1)
    return download_path
