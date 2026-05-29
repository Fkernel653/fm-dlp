# fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

Download high-quality music and video from YouTube, YouTube Music, and 1000+ sites — with metadata tagging, from your terminal.

## 🚀 Quick Start

```bash
pip install fm-dlp          # Requires Python 3.10+ & FFmpeg
fm-dlp config ~/Music        # Set download directory
fm-dlp search "artist"       # Search tracks (YouTube Music by default)
fm-dlp download "URL" --codec flac  # Download audio
```

## 📋 Commands

### `search` — Find music
```bash
fm-dlp search <query> [--limit 10] [--yt-video] [--type track|album]
```
Search uses **YouTube Music by default**. Use `--yt-video` to search YouTube instead.

| Option | Default | Description |
|--------|---------|-------------|
| `--yt-video` | — | Search YouTube instead of YTMusic |
| `--type` | `track` | `track`, `album` |
| `--limit` | 10 | Results count |

### `download` — Download audio/video
```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--jobs 5] [--quiet] [--no-metadata]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--codec` | `m4a`/`opus` | Audio: `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav` Video: `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| `--kbps` | 256 | Bitrate 64–320 (audio) |
| `--jobs` | 5 | Parallel downloads |
| `--quiet` | — | Suppress yt-dlp output |
| `--no-metadata` | — | Skip metadata embedding |
| `--path` | config | Override download directory |
| `--cookies` | — | Browser: `chrome`, `firefox`, `edge` |

### `config` — Set download path
```bash
fm-dlp config ~/Music
```

## 📖 Examples

```bash
# Search
fm-dlp search "Sewerslvt" --limit 10          # YTMusic
fm-dlp search "usedcvnt" --type album
fm-dlp search "breakcore" --yt-video               # YouTube

# Audio
fm-dlp download "URL" --codec mp3 --kbps 320
fm-dlp download "URL1 URL2 URL3" --codec flac

# Video
fm-dlp download "URL" --codec mp4
fm-dlp download "URL" --codec mkv

# Custom path
fm-dlp download "URL" --path ~/Downloads

# Advanced
fm-dlp download "URL" --cookies firefox
fm-dlp download "URL1 URL2 URL3" --quiet --jobs 10
```

## 🔧 Dependencies

| Library | Purpose |
|---------|---------|
| `yt-dlp` | Download engine |
| `ytmusicapi` | YouTube Music API |
| `mutagen` | Metadata tagging |
| `platformdirs` | Config paths |
| `color-kiss` | Terminal colors |
| `cliss` | CLI framework |
| **FFmpeg** | Audio/video conversion (system) |

## ❓ FAQ

**Why fm-dlp over yt-dlp?** Simplifies complex flags into clean commands: readable search output, single `--codec` option, automatic metadata tagging.

**Why M4A on macOS?** macOS treats M4A/AAC as native (Finder, Music.app). Linux/Windows default to Opus for better quality. Override with `--codec`.

**How to use a proxy?** fm-dlp doesn't include built-in proxy support. Use [proxychains](https://github.com/haad/proxychains) or similar tools:
```bash
proxychains fm-dlp download "URL"
```

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
