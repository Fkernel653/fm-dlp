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

## 🌈 Color Output

By default, fm-dlp uses colored output for better readability. To disable colors globally, use the `--no-color` flag **before** the command:

```bash
fm-dlp --no-color search "artist"
fm-dlp --no-color download "URL"
fm-dlp --no-color config ~/Music
```

## 📋 Commands

### `search`

Search for music tracks, albums, or videos on YouTube/YTMusic.

```bash
fm-dlp search <query> [--limit LIMIT] [--yt-video] [--album] [--raw] [--only-url]
```

| Option | Default | Description |
|--------|---------|-------------|
| `query` | **Required** | Search query string |
| `--limit N`, `-l` | `10` | Maximum number of results to return |
| `--yt-video`, `-v` | `False` | Search for YouTube videos instead of music tracks |
| `--album`, `-a` | `False` | Search for albums instead of individual tracks |
| `--raw`, `-r` | `False` | Output results in raw format (Python dict representation) |
| `--only-url`, `-u` | `False` | Output only the URLs without any formatting |

---

### `download`

Download audio or video content from supported platforms (YouTube, YTMusic, and 1000+ sites).

```bash
fm-dlp download <urls> [--codec CODEC] [--kbps KBPS] [--jobs JOBS] [--quiet] [--no-metadata] [--save] [--path PATH] [--only-video] [--cookies COOKIES]
```

| Option | Default | Description |
|--------|---------|-------------|
| `urls` | **Required** | Single URL, comma/space-separated list, or path to text file with URLs (one per line, `#` for comments) |
| `--codec`, `-c` | `m4a` (macOS)<br>`opus` (others) | **Audio:** `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac`<br>**Video:** `mp4`, `mov`, `mkv`, `webm`, `avi`, `flv` |
| `--kbps`, `-k` | `256` | Audio bitrate in kbps (64–320). Higher = better quality, larger file |
| `--jobs`, `-j` | `5` | Maximum number of concurrent downloads for faster batch processing |
| `--quiet`, `-q` | `False` | Suppress yt-dlp output messages (errors still shown) |
| `--no-metadata` | `False` | Disable embedding metadata (title, artist, album) and thumbnail into audio files |
| `--save`, `-s` | `False` | Saving settings (except URL) |
| `--use-config`, `-u` | `False` | Use saved parameters from config file as defaults |
| `--path`, `-p` | Configured path | Custom download directory (overrides default config) |
| `--only-video`, `-v` | `False` | Download video file without audio track |
| `--cookies`, `-C` | `None` | Browser name: `brave`, `chrome`, `chromium`, `edge`, `opera`, `vivaldi`, `whale`, `firefox`, `safari`<br>Or path to cookies file (`.txt`, `.sqlite`, `.db`, `.cookies`) |

**Audio Codec Details:**
- **Lossy:** `mp3` (universal), `aac` (Apple), `m4a` (Apple), `opus` (modern web) - smaller files
- **Lossless:** `flac` (high quality), `wav` (uncompressed), `alac` (Apple lossless) - larger files
- **Recommended:** `opus` for best quality/size ratio, `flac` for archival

**Video Container Details:**
- **`mp4`** - Most compatible, uses `m4a` audio
- **`mkv`** - Open format, uses `opus` audio
- **`webm`** - Web optimized, uses `opus` audio
- **`mov`** - Apple format, uses `m4a` audio
- **`avi`** - Legacy Windows, uses `mp3` audio
- **`flv`** - Flash video, uses `aac` audio

---

### `config`

Configure the default download directory path.

```bash
fm-dlp config <path>
```

| Option | Default | Description |
|--------|---------|-------------|
| `path` | **Required** | Default directory path for downloads. Use absolute path for best results (e.g., `/home/user/Music` or `C:\Music`) |

**Config Location:**
- **Windows:** `%LOCALAPPDATA%/fm-dlp/config.json`
- **macOS:** `~/Library/Application Support/fm-dlp/config.json`
- **Linux:** `~/.config/fm-dlp/config.json`

---

## ⚙️ Requirements

- **Python 3.10+** - Asyncio support required
- **FFmpeg** - Required for audio/video processing. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg` (Debian) or `sudo dnf install ffmpeg` (Fedora)
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

Verify installation: `ffmpeg --version`

---

## 🔧 Validation & Error Handling

The CLI performs comprehensive validation before executing commands:

**Search:**
- Validates that `--limit` is a positive integer

**Download:**
- Validates URLs (must start with `http://` or `https://` or be a valid file)
- Validates codec against supported list
- Validates bitrate range (64–320 kbps)
- Validates job count (must be >= 1)
- Validates download path (must exist and be a directory)
- Validates cookies (browser name or valid file path with correct extension)
- Checks FFmpeg installation

**Config:**
- Validates path exists and is a directory
- Creates config directory if it doesn't exist
- Handles permission errors gracefully

---

## 📄 License & Acknowledgments

MIT License — Built with:

| Library | Purpose |
|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine supporting 1000+ sites |
| [ytmusicapi](https://github.com/sigma67/ytmusicapi) | YouTube Music search API |
| [mutagen](https://github.com/quodlibet/mutagen) | Metadata tagging for audio files |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp) • [PyPI](https://github.com/Fkernel653/fm-dlp)
