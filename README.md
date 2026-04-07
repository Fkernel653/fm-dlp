# fm-dlp - YouTube & SoundCloud Music Downloader

A command-line tool for searching and downloading audio from YouTube and SoundCloud. Built with Python, using `yt-dlp` for downloads and native search implementations.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)

## 📋 Features

- **YouTube & SoundCloud Search**: Search using `yt-dlp` (YouTube) and `soundcloud-v2` (SoundCloud)
- **High-Quality Audio Download**: Extract audio in multiple formats using `yt-dlp` + FFmpeg
- **Multiple Audio Formats**: M4A, MP3, AAC, OPUS, WAV via `--codec` parameter
- **Configurable Bitrate**: Adjust quality from 128-320 kbps with `--kbps`
- **Browser Cookie Support**: Pass cookies from Chrome/Firefox/Edge for restricted content
- **Persistent Configuration**: Save download directory in `config.json`
- **Colorful Terminal Output**: ANSI color codes for better readability
- **Async Search Operations**: Non-blocking SoundCloud search with timeout
- **Formatted Results**: Tree structure output with metadata

## 🚀 Installation

### Prerequisites

- **Python 3.9 or higher** (uses `match` statement from Python 3.10+)
- **FFmpeg** - Required for audio conversion

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [FFmpeg.org](https://ffmpeg.org/download.html)
2. Add the `bin` folder to your system PATH

### Install fm-dlp

```bash
git clone https://github.com/Fkernel653/fm-dlp.git
cd fm-dlp
pip install -r requirements.txt
```

## 🔧 Configuration

### Set Download Directory

```bash
python fm-dlp.py config /path/to/your/music/folder
```

View current config:
```bash
python fm-dlp.py config
```

The path is saved in `config.json` in the project root.

## 📖 Usage

```bash
python fm-dlp.py <command> [arguments]
```

### Commands

#### Search for Music

```bash
# YouTube search (default)
python fm-dlp.py search "your query" --limit=10

# SoundCloud search
python fm-dlp.py search "your query" --variable=soundcloud --limit=5

# Filter out results without required fields
python fm-dlp.py search "query" --enable_filter=True
```

**Parameters:**
- `query` (required) - Search term
- `--limit` - Max results (default: 10)
- `--enable_filter` - Filter incomplete results - "True"/"False" (default: "False")
- `--variable` - Platform: `youtube` or `soundcloud` (default: `youtube`)

**Examples:**
```bash
python fm-dlp.py search "Sewerslvt"
python fm-dlp.py search "breakcore" --variable=soundcloud --limit=5
python fm-dlp.py search "ambient" --enable_filter=True
```

#### Download Audio

```bash
# Basic download (M4A, 256 kbps)
python fm-dlp.py download "https://youtu.be/VIDEO_ID"

# Custom format and quality
python fm-dlp.py download "URL" --codec=mp3 --kbps=192

# With browser cookies for age-restricted content
python fm-dlp.py download "URL" --cookies=chrome
```

**Parameters:**
- `url` (required) - YouTube video URL
- `--codec` - Output format: `m4a`, `mp3`, `aac`, `opus`, `wav` (default: `m4a`)
- `--kbps` - Bitrate in kbps (default: 256)
- `--cookies` - Browser for cookies: `chrome`, `firefox`, `edge`, etc. (optional)
- `--ffmpeg` - Reserved for future use (default: "True")

**Note:** Download path must be configured first with `config` command.

#### Get Help

```bash
python fm-dlp.py help
```

## 📁 Project Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (clite framework)
├── config.json            # Persistent configuration (auto-generated)
├── requirements.txt       # Dependencies
├── README.md              # This file
└── modules/
    ├── __init__.py
    ├── search.py          # YouTube + SoundCloud search
    ├── download.py        # Audio download with yt-dlp
    ├── configer.py        # Config management (JSON)
    ├── help.py            # Help menu generation
    └── colors.py          # ANSI color constants
```

## 🛠️ Technical Details

### Search Implementation

- **YouTube**: Uses `yt-dlp` with `extract_flat=True` and `ytsearch{n}:{query}` format
  - No API key required
  - Returns title, channel, view count, duration, and URL
  - Filtering removes videos without required fields

- **SoundCloud**: Uses `soundcloud-v2` library
  - Async execution with 30-second timeout
  - Returns title, artist, date, duration, and permalink URL

### Download Implementation

- Uses `yt-dlp.YoutubeDL` with FFmpeg post-processing
- Format: `bestaudio/best` (highest quality audio stream)
- Output template: `{config_path}/%(title)s.%(ext)s`
- Supports browser cookie extraction for restricted videos

### Color Scheme

| Color | Usage |
|-------|-------|
| 🔴 Red | Errors, URLs |
| 🟢 Green | Success messages, config status |
| 🔵 Blue | (Reserved) |
| 🟡 Yellow | Command names in help |
| 🔷 Cyan | Result numbering, headers |
| ⚪ Gray | Tree lines, separators, descriptions |

## ⚠️ Requirements

### Python Dependencies (from `requirements.txt`)

| Package | Purpose |
|---------|---------|
| `yt-dlp` | YouTube downloading and audio extraction |
| `soundcloud-v2` | SoundCloud API wrapper |
| `fake-useragent` | Random user agent rotation |
| `clite` | CLI framework for command routing |

### System Dependencies

- **FFmpeg** - Required for audio conversion (must be in PATH)

## 🐛 Troubleshooting

### "Config file not found!"
Run `python fm-dlp.py config /your/download/path` first.

### Download fails with FFmpeg error
Ensure FFmpeg is installed: `ffmpeg -version`

### Age-restricted video error
Use cookies from logged-in browser:
```bash
python fm-dlp.py download "URL" --cookies=chrome
```

### SoundCloud search timeout
Reduce limit or try again:
```bash
python fm-dlp.py search "query" --variable=soundcloud --limit=3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Use color constants from `colors.py`

## 📄 License

MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Fkernel653** - [GitHub](https://github.com/Fkernel653)

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloading library
- [soundcloud-v2](https://github.com/7x11x13/soundcloud-v2) - SoundCloud API wrapper
- [clite](https://pypi.org/project/clite/) - CLI framework
- [fake-useragent](https://github.com/hellysmile/fake-useragent) - User agent rotation

---

**Disclaimer**: For educational purposes only. Users are responsible for complying with platform Terms of Service and copyright laws.