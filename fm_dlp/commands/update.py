"""
fm-dlp update module

This module provides self-update functionality for fm-dlp.
Supports both PyInstaller binaries and Python script installations.
"""

import sys


def is_bin():
    """Check if the application is running as a PyInstaller bundled executable.

    Returns:
        bool: True if running as a frozen binary (PyInstaller), False otherwise.

    Note:
        PyInstaller sets sys.frozen = True and creates sys._MEIPASS attribute
        when bundling the application into a single executable.
    """
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_asset_for_os(assets):
    """Select the correct binary asset from GitHub release for the current OS.

    Args:
        assets (list): List of release assets from GitHub API response.
                      Each asset is a dict with 'name' and 'browser_download_url' keys.

    Returns:
        str: The browser_download_url of the matching binary for the current OS.

    Raises:
        StopIteration: If no matching asset is found for the current OS.

    Selection logic:
        - Windows: Files ending with '.exe'
        - macOS (darwin): Files with no extension and 'mac' in the name
        - Linux: Files with no extension and 'linux' in the name
    """
    if sys.platform == "win32":
        return next(
            a["browser_download_url"] for a in assets if a["name"].endswith(".exe")
        )
    elif sys.platform == "darwin":
        return next(
            a["browser_download_url"]
            for a in assets
            if "." not in a["name"] and "mac" in a["name"].lower()
        )
    else:
        return next(
            a["browser_download_url"]
            for a in assets
            if "." not in a["name"] and "linux" in a["name"].lower()
        )


def update(color: bool):
    """Update fm-dlp to the latest version from GitHub.

    Automatically detects whether running as a PyInstaller binary or Python script,
    then updates accordingly. For binaries, downloads the OS-specific executable
    from GitHub Releases. For scripts, upgrades via pip or uv.

    Args:
        color: Enable colored output for success/error messages.

    Returns:
        str: Status message indicating success or failure.

    Raises:
        Exception: If update fails (handled with user-friendly message).

    Behavior:
        - Binary mode: Downloads and replaces current executable with OS-specific binary
        - Script mode: Uses uv (preferred) or pip to upgrade the package
        - No version checking: Always updates to the latest GitHub release
    """
    import json
    import subprocess
    import urllib.error
    import urllib.request

    from fm_dlp.utils.colors import error, set_colors, success

    set_colors(color)

    try:
        repo = "fm-dlp"
        url = f"https://api.github.com/repos/Fkernel653/{repo}/releases/latest"

        with urllib.request.urlopen(url) as response:
            r = json.loads(response.read())

        latest = r["tag_name"].lstrip("v")
    except urllib.error.URLError:
        return error("Failed to connect to GitHub API. Check your internet connection.")
    except json.JSONDecodeError:
        return error("Invalid response from GitHub API.")
    except KeyError:
        return error("No releases found for fm-dlp on GitHub.")

    try:
        if is_bin():
            import os
            import shutil
            import tempfile

            try:
                asset_url = get_asset_for_os(r["assets"])
            except StopIteration:
                return error(
                    f"No binary found for your OS ({sys.platform}) in the latest release. "
                    "Please download manually from GitHub."
                )

            temp_path = f"{tempfile.gettempdir()}/fm-dlp-update"
            urllib.request.urlretrieve(asset_url, temp_path)

            shutil.move(temp_path, sys.executable)
            os.chmod(sys.executable, 0o755)
            return success(f"Updated binary to {latest}")

        else:
            has_uv = (
                subprocess.run(
                    ["uv", "--version"], capture_output=True, shell=False
                ).returncode
                == 0
            )

            cmd = "uv" if has_uv else "pip"
            result = subprocess.run(
                [sys.executable, "-m", cmd, "install", "--upgrade", repo],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return error(
                    f"Package update failed via {cmd}.\n"
                    f"Error: {result.stderr.strip() or result.stdout.strip()}"
                )

            return success(f"Updated package to {latest} via {cmd}")

    except PermissionError:
        return error(
            "Permission denied. "
            f"Try running with administrator/sudo privileges or "
            f"update manually via 'pip install --upgrade {repo}'."
        )
    except urllib.error.URLError:
        return error("Failed to download update. Check your internet connection.")
    except Exception as e:
        return error(f"Update failed: {str(e)}")
