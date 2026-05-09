"""
Persistent download path storage using JSON config file.
"""

from json import dump, loads
from pathlib import Path

from modules.colors import BLUE, GREEN, RED, RESET, YELLOW

_CONFIG_FILE = Path(__file__).parent.parent / "config.json"
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
            dump({KEY_NAME: path_str}, f, ensure_ascii=False, indent=4)

        return f"{GREEN}Configuration saved successfully!{RESET}\n{YELLOW}Path: {RESET}{path_str}\n{BLUE}Config file: {RESET}{_CONFIG_FILE}"
    except Exception as e:
        return f"{RED}Error saving configuration: {e}{RESET}"


def get_path() -> str:
    if not _CONFIG_FILE.exists():
        return f"{RED}Config file not found! Run: fm-dlp config /path{RESET}"

    data = loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    download_path = data.get(KEY_NAME)
    if not download_path or not Path(download_path).exists():
        return f"{RED}Download path does not exist.{RESET}"
    return download_path
