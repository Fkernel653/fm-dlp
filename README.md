# fm-dlp — Download music/video from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp.svg)](https://pypi.org/project/fm-dlp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ platforms

## 🚀 Quick Start

```bash
pip install fm-dlp                    # Requires Python 3.10+ & FFmpeg
fm-dlp config ~/Music                 # Set download directory
fm-dlp search "artist"                # Search tracks (YouTube Music by default)
fm-dlp download "URL" --codec flac    # Download audio
fm-dlp download urls.txt --codec mp3  # Download from file
```

## 📋 Commands

### `search` — Find music
```bash
fm-dlp search <query> [--limit 10] [--yt-video] [--album] [--raw]
```
Search uses **YouTube Music by default**. Use `--yt-video` to search YouTube instead.

| Option | Default | Description |
|--------|---------|-------------|
| `--yt-video` | — | Search YouTube instead of YTMusic |
| `--album` | — | Search by albums |
| `--limit` | 10 | Results count |
| `--raw` | — | Output of results in RAW format |

**RAW format output** includes complete unformatted data (JSON/YAML) suitable for scripting and external tool integration, preserving all metadata fields without pretty-printing or truncation.

### `download` — Download audio/video
```bash
fm-dlp download <urls> [--codec CODEC] [--kbps 256] [--jobs 5] [--quiet] [--no-metadata]
```

**URLs can be:**
- Single URL: `"https://youtube.com/watch?v=..."`
- Multiple URLs: `"URL1 URL2 URL3"` or `"URL1,URL2,URL3"`
- File with URLs: `"urls.txt"` (one URL per line, supports `#` comments)

| Option | Default | Description |
|--------|---------|-------------|
| `--codec` | `m4a`/`opus` | Audio: `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`<br>Video: `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| `--kbps` | 256 | Bitrate 64–320 (audio) |
| `--jobs` | 5 | Parallel downloads |
| `--quiet` | — | Suppress yt-dlp output |
| `--no-metadata` | — | Skip metadata embedding |
| `--path` | config | Override download directory |
| `--cookies` | — | Path to cookies file OR browser name (`chrome`, `firefox`, `edge`, `safari`, `brave`, `opera`) |

## 📖 Examples

```bash
# Search
fm-dlp search "Sewerslvt" --limit 10                # YTMusic
fm-dlp search "usedcvnt" --album
fm-dlp search "breakcore" --yt-video                # YouTube

# RAW output for scripting
fm-dlp search "Sewerslvt" --raw                     # Machine-readable output
fm-dlp search "breakcore" --yt-video --raw          # RAW from YouTube
fm-dlp search "album" --album --raw > results.json  # Save to file

# Audio - single URL
fm-dlp download "https://youtube.com/watch?v=..." --codec mp3 --kbps 320
fm-dlp download "https://youtu.be/..." --codec flac

# Audio - multiple URLs
fm-dlp download "URL1 URL2 URL3" --codec flac
fm-dlp download "URL1,URL2,URL3" --jobs 10

# Audio - from file
echo "https://youtube.com/watch?v=123" > urls.txt
echo "https://youtu.be/456" >> urls.txt
fm-dlp download urls.txt --codec mp3

# Video
fm-dlp download "URL" --codec mp4
fm-dlp download "URL" --codec mkv

# Custom path
fm-dlp download "URL" --path ~/Downloads

# Advanced
fm-dlp download "URL" --cookies firefox
fm-dlp download "URL" --cookies /path/to/cookies.txt
fm-dlp download "URL1 URL2 URL3" --quiet --jobs 10
fm-dlp download urls.txt --codec opus --kbps 192 --no-metadata
```

## 🔧 Dependencies

| Library | Purpose |
|---------|---------|
| `yt-dlp` | Download engine |
| `ytmusicapi` | YouTube Music API |
| `mutagen` | Metadata tagging |
| `platformdirs` | Config paths |
| `arg-kiss` | CLI framework |
| **FFmpeg** | Audio/video conversion (system) |

## ❓ FAQ

**Why fm-dlp over yt-dlp?** Simplifies complex flags into clean commands: readable search output, single `--codec` option, automatic metadata tagging.

**Why M4A on macOS?** macOS treats M4A/AAC as native (Finder, Music.app). Linux/Windows default to Opus for better quality. Override with `--codec`.

**How to use cookies?** Provide either browser name for automatic extraction (`--cookies firefox`) or path to exported cookies file (`--cookies cookies.txt`).

**How to use a URL file?** Pass a path to a text file instead of URLs. Each URL on new line, lines starting with `#` are ignored as comments. Supports UTF-8 encoding.

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
- [arg-kiss](https://github.com/Fkernel653/arg-kiss) — CLI framework

---

**Author:** [Fkernel653](https://github.com/Fkernel653)
**Repository:** [github.com/Fkernel653/fm-dlp](https://github.com/Fkernel653/fm-dlp)
**PyPI:** [pypi.org/project/fm-dlp](https://pypi.org/project/fm-dlp/)
