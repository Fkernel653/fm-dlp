"""Custom Path implementation mimicking pathlib.Path."""

from __future__ import annotations

import os


class Path:
    """Custom Path implementation."""

    def __init__(self, *args):
        """Initialize Path object.

        Args:
            *args: Path components to join.
        """
        if not args:
            self._path = ""
        else:
            parts = []
            for arg in args:
                if isinstance(arg, Path):
                    parts.append(str(arg))
                elif hasattr(arg, "__fspath__"):
                    parts.append(os.fspath(arg))
                else:
                    parts.append(str(arg))

            parts = [p for p in parts if p]
            self._path = os.path.join(*parts) if parts else ""

    def __str__(self) -> str:
        return self._path

    def __truediv__(self, other: str | Path) -> Path:
        return Path(self._path, str(other))

    @property
    def parent(self) -> Path:
        """Return parent directory."""
        parts = self._path.rsplit("/", 1)
        return Path(parts[0] if len(parts) > 1 else "")

    @property
    def suffix(self) -> str:
        """Return file extension."""
        name = self._path.rsplit("/", 1)[-1] if "/" in self._path else self._path
        return name[name.rfind(".") :] if "." in name else ""

    def exists(self) -> bool:
        """Check if path exists."""
        return os.path.exists(self._path)

    def is_dir(self) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(self._path)

    def is_file(self) -> bool:
        """Check if path is a file."""
        return os.path.isfile(self._path)

    def mkdir(self, exist_ok: bool) -> None:
        """Create directory."""
        os.makedirs(self._path, exist_ok=exist_ok)

    def read_text(self, encoding: str = "utf-8") -> str:
        """Read file content as text."""
        with open(self._path, "r", encoding=encoding) as f:
            return f.read()

    def write_text(self, data: str, encoding: str = "utf-8") -> int:
        """Write text to file."""
        with open(self._path, "w", encoding=encoding) as f:
            return f.write(data)

    def resolve(self) -> Path:
        """Resolve absolute path."""
        return Path(os.path.abspath(self._path))

    def expanduser(self) -> Path:
        """Expand ~ to user home."""
        return Path(os.path.expanduser(self._path))

    def stat(self):
        """Return stat info."""
        return os.stat(self._path)

    @classmethod
    def home(cls) -> Path:
        """Return user home directory."""
        return cls(os.path.expanduser("~"))
