"""
Persistent download path storage using JSON config file.
"""

from json import dump
from pathlib import Path

from modules.colors import BLUE, GREEN, RED, RESET, YELLOW

_CONFIG_FILE = Path(__file__).parent.parent / "config.json"


def configer(path: str) -> str:
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
            dump({"path": path_str}, f, ensure_ascii=False, indent=4)

        return f"{GREEN}Configuration saved successfully!{RESET}\n{YELLOW}Path: {RESET}{path_str}\n{BLUE}Config file: {RESET}{_CONFIG_FILE}"
    except Exception as e:
        return f"{RED}Error saving configuration: {e}{RESET}"
