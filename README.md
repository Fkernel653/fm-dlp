# fm-dlp — Download from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)]()
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

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
fm-dlp search <query> [--limit 10] [--yt-video] [--album] [--raw]
```
`--yt-video` (YouTube vs YTMusic), `--album`, `--limit N`, `--raw` (JSON output)

### `download`
```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--jobs 5]
```
**URLs:** Single, multiple (space/comma), or file (one per line, `#` comments)

| Option | Description |
|--------|-------------|
| `--codec` | Audio: `mp3,aac,flac,m4a,opus,vorbis,wav` Video: `mp4,mkv,webm,mov,avi,flv` |
| `--kbps` | Bitrate 64–320 (default: 256) |
| `--jobs` | Parallel downloads (default: 5) |
| `--quiet` | Suppress yt-dlp output |
| `--no-metadata` | Skip metadata tagging |
| `--path` | Override download directory |
| `--cookies` | Browser (`chrome,firefox`) or cookies file |

## 📄 License & Acknowledgments

MIT License — Built with:

| Library | Purpose |
|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music API |
| [mutagen](https://github.com/quodlibet/mutagen) | Metadata tagging |
| [platformdirs](https://github.com/platformdirs/platformdirs) | Config paths |
| [arg-kiss](https://github.com/Fkernel653/arg-kiss) | CLI framework |

**Author:** [Fkernel653](https://github.com/Fkernel653)
**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp) • [PyPI](https://pypi.org/project/fm-dlp/)
