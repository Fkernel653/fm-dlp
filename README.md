# fm-dlp — Download and tag music/video from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

Download and tag high-quality music and video from YouTube, YouTube Music, and 1000+ sites — all from your terminal.

## ✨ Features

- **Multi-platform Search** — YouTube, YouTube Music (tracks & albums)
- **1000+ Supported Sites** — Any site yt-dlp supports
- **Audio/Video Formats** — MP3, FLAC, MP4, MKV, WebM, and more with configurable bitrate
- **Metadata Embedding** — Title, artist, album tags + thumbnail (audio)
- **Proxy Support** — HTTP, HTTPS, SOCKS4/SOCKS5/SOCKS5h
- **Cookie Support** — Browser cookies for restricted content
- **Parallel Downloads** — Async support for multiple URLs
- **Cross-platform Config** — XDG, AppData, Application Support

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ & FFmpeg

### Installation
```bash
pip install fm-dlp        # pip
uv pip install fm-dlp     # uv
pipx install fm-dlp       # pipx
```

### Usage
```bash
fm-dlp config ~/Music                          # Set download directory (first run)
fm-dlp search "artist" --platform yt-music     # Search tracks
fm-dlp search "album" --type album             # Search albums
fm-dlp download "URL" --codec mp3 --kbps 320   # Download audio
fm-dlp download "URL" --codec mp4              # Download video
```

## 📋 Commands

### `search` — Find music
```bash
fm-dlp search <query> [--limit 10] [--platform yt-music|yt-video] [--type track|album] [--proxy URL]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--platform` | `yt-music` | Search platform: `yt-music`, `yt-video` |
| `--type` | `track` | Content type: `track`, `album` |
| `--limit` | 10 | Number of results |
| `--proxy` | — | Proxy URL |

### `download` — Download audio/video
```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--quiet] [--max-concurrent 5] [--cookies browser] [--proxy URL]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--codec` | `m4a`/`opus` | Audio: `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`<br>Video: `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| `--kbps` | 256 | Bitrate 64–320 (audio only) |
| `--max-concurrent` | 5 | Parallel downloads |
| `--quiet` | — | Suppress output |
| `--no-metadata` | — | Disable metadata embedding |
| `--cookies` | — | Browser: `chrome`, `firefox`, `edge`, etc. |
| `--proxy` | — | `http://`, `socks5://`, etc. |

### `config` — Set download path
```bash
fm-dlp config ~/Music    # Set directory
fm-dlp config             # View current path
```
Stored in: `~/.config/fm-dlp/` (Linux), `~/Library/Application Support/fm-dlp/` (macOS), `%APPDATA%\fm-dlp\` (Windows).

## 📖 Examples

```bash
# Search
fm-dlp search "Sewerslvt" --limit 10 --platform yt-music
fm-dlp search "usedcvnt" --type album

# Audio
fm-dlp download "URL" --codec flac
fm-dlp download "URL1 URL2 URL3" --codec mp3 --kbps 320

# Video
fm-dlp download "URL" --codec mp4
fm-dlp download "URL" --codec mkv

# Advanced
fm-dlp download "URL" --cookies firefox
fm-dlp download "URL" --proxy socks5://127.0.0.1:9050
fm-dlp download "URL1 URL2 URL3 URL4 URL5" --quiet --max-concurrent 10
```

## 📁 Project Structure
```
fm-dlp/
├── modules/
│   ├── __init__.py          # Package initializer
│   ├── cli.py               # CLI entry point (cliss)
│   ├── commands/
│   │   ├── search.py        # YouTube & YTMusic search
│   │   └── download.py      # Async download engine (yt-dlp)
│   └── utils/
│       ├── configer.py      # JSON config manager
│       └── validator.py     # Input validation & dependency checks
├── pyproject.toml
├── README.md
└── LICENSE
```

## 🔧 Requirements

| Dependency | Purpose |
|------------|---------|
| `yt-dlp` | YouTube extraction & download |
| `ytmusicapi` | YouTube Music API |
| `mutagen` | Audio metadata tagging |
| `platformdirs` | Cross-platform config paths |
| `color-kiss` | Terminal colors |
| `cliss` | CLI framework |
| **FFmpeg** | Audio/video conversion (system) |

## ❓ FAQ

### Why fm-dlp when yt-dlp exists?

fm-dlp wraps yt-dlp's complex flags into a clean workflow: **search** with readable output, **download** with a single `--codec` option, and **automatic metadata tagging** from structured music data — no memorising flag combinations.

### macOS defaults to M4A, others to Opus — why?

macOS treats M4A/AAC as first-class (Finder, Music.app, QuickTime). Linux/Windows default to Opus for superior quality at equivalent bitrates. Override with `--codec`.

### How does CLI parsing work?

Uses [cliss](https://github.com/Fkernel653/cliss) — a zero-dependency wrapper over `argparse` with type-driven arguments and async support.

### Proxy support?

| Protocol | Download | Search (yt-video) | Search (yt-music) |
|----------|:--------:|:-----------------:|:-----------------:|
| `http://`, `https://` | ✅ | ✅ | ✅ |
| `socks4://`, `socks5://`, `socks5h://` | ✅ | ✅ | ❌ |

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Download engine
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) — YouTube Music API
- [mutagen](https://github.com/quodlibet/mutagen) — Metadata tagging
- [platformdirs](https://github.com/platformdirs/platformdirs) — Config paths
- [color-kiss](https://github.com/Fkernel653/color-kiss) — Terminal colors
- [cliss](https://github.com/Fkernel653/cliss) — CLI framework

---

**Author:** [Fkernel653](https://github.com/Fkernel653)
**Repository:** [github.com/Fkernel653/fm-dlp](https://github.com/Fkernel653/fm-dlp)
**PyPI:** [pypi.org/project/fm-dlp](https://pypi.org/project/fm-dlp/)
