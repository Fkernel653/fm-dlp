# fm-dlp — Download from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff)

CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms

## 🚀 Quick Start

```bash
pip install fm-dlp                    # Python 3.10+ & FFmpeg required
fm-dlp config ~/Music                 # Set download directory
fm-dlp search "artist"                # Search tracks
fm-dlp download "URL" --codec flac    # Download audio
```

## 📋 Commands

### `search`

```bash
fm-dlp search <query> [--limit 10] [--yt-video] [--album] [--raw] [--only-url] [--no-color]
```

| Option | Description |
|--------|-------------|
| `--limit N` | Maximum number of results (default: 10) |
| `--yt-video` | Search YouTube videos instead of YouTube Music |
| `--album` | Search for albums instead of individual tracks |
| `--raw` | Output raw JSON/Python dict format |
| `--only-url` | Output only URLs without any formatting |
| `--no-color` | Disable colored output in search results |

### `download`

```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--jobs 5] [--quiet] [--no-metadata] [--path PATH] [--cookies COOKIES] [--no-color]
```

**URLs:** Single, multiple (space/comma), or file path (one URL per line, `#` for comments)

| Option | Description |
|--------|-------------|
| `--codec` | Audio: `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac` <br>Video: `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| `--kbps` | Audio bitrate 64–320 (default: 256) |
| `--jobs` | Number of parallel downloads (default: 5) |
| `--quiet` | Suppress yt-dlp output messages |
| `--no-metadata` | Skip metadata and thumbnail embedding |
| `--path` | Override download directory |
| `--cookies` | Browser name (`brave`, `chrome`, `chromium`, `edge`, `opera`, `vivaldi`, `whale`, `firefox`, `safari`) or path to cookies file |
| `--no-color` | Disable colored output in download messages |

### `config`

```bash
fm-dlp config <path> [--no-color]
```

| Option | Description |
|--------|-------------|
| `path` | Default download directory |
| `--no-color` | Disable colored output in configuration messages |

### `update`

```bash
fm-dlp update [--no-color]
```

Self-update to the latest version from GitHub with automatic OS detection.

| Option | Description |
|--------|-------------|
| `--no-color` | Disable colored output in update messages |

| Behavior | Description |
|----------|-------------|
| **Binary mode** (PyInstaller) | Downloads the appropriate executable for your OS (`.exe` on Windows, no extension on macOS/Linux) and replaces the current binary |
| **Script mode** (pip install) | Updates the package via `pip` or `uv` (whichever is available, `uv` preferred for faster installation) |

**Features:**
- Automatic OS detection (Windows, macOS, Linux)
- Always updates to the latest GitHub release (no version checking)
- Cross-platform support
- Fallback to pip if uv is not installed
- Preserves executable permissions on Unix systems
- Error handling with user-friendly messages:
  - GitHub API connection failures
  - Missing assets for current OS
  - Permission denied (with admin/sudo suggestion)
  - Package installation errors (with detailed output)

**Note:** The application may need to be restarted after updating, especially when running as a binary.

## 📄 License & Acknowledgments

MIT License — Built with:

| Library | Purpose |
|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music API |
| [mutagen](https://github.com/quodlibet/mutagen) | Metadata tagging |
| [platformdirs](https://github.com/platformdirs/platformdirs) | Config paths |
| [argss](https://github.com/Fkernel653/argss) | CLI framework |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp) • [PyPI](https://pypi.org/project/fm-dlp)
