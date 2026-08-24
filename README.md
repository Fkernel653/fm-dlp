# fm-dlp — Download from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)](<>)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

CLI tool for searching YouTube/YTMusic and downloading audio/video from [1000+ sites](https://github.com/yt-dlp/yt-dlp/supportedsites.md)

---

## 📑 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [⚙️ Requirements](#️-requirements)
- [🌈 Color Output](#-color-output)
- [📋 Commands](#-commands)
  - [`search`](#search)
  - [`download`](#download)
  - [`config`](#config)
- [💡 Examples](#-examples)
  - [Basic Download](#basic-download)
  - [Search Examples](#search-examples)
- [📊 Search Output Examples](#-search-output-examples)
- [📄 License & Acknowledgments](#-license--acknowledgments)

---

## 🚀 Quick Start

```bash
pip install fm-dlp                    # Python 3.10+ & FFmpeg required
fm-dlp config ~/Music                 # Set download directory
fm-dlp search "Sewerslvt"                # Search tracks
fm-dlp download "URL"                 # Download audio
```

---

## ⚙️ Requirements

- **Python 3.11+** - Asyncio support required
- **FFmpeg** - Required for audio/video processing. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg` (Debian) or `sudo dnf install ffmpeg` (Fedora)
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

---

## 🌈 Color Output

By default, fm-dlp uses colored output for better readability. To disable colors globally, use the `--no-color` flag **before** the command:

```bash
fm-dlp --no-color search "artist"
fm-dlp --no-color download "URL"
fm-dlp --no-color config ~/Music
```

---

## 📋 Commands

### `search`

Search for music tracks, albums, or videos on YouTube/YTMusic.

```bash
fm-dlp search <query> [--limit LIMIT] [--yt-video] [--album] [--raw] [--only-url]
```

| Option             | Default      | Description                                               |
| ------------------ | ------------ | --------------------------------------------------------- |
| `query`            | **Required** | Search query string                                       |
| `--limit N`, `-l`  | `10`         | Maximum number of results to return                       |
| `--yt-video`, `-v` | `False`      | Search for YouTube videos instead of music tracks         |
| `--album`, `-a`    | `False`      | Search for albums instead of individual tracks            |
| `--raw`, `-r`      | `False`      | Output results in raw format (Python dict representation) |
| `--only-url`, `-u` | `False`      | Output only the URLs without any formatting               |

---

### `download`

Download audio or video content from supported platforms (YouTube, YTMusic, and 1000+ sites).

```bash
fm-dlp download <urls> [--codec CODEC] [--kbps KBPS] [--quality QUALITY] [--jobs JOBS] [--quiet] [--no-metadata] [--keep] [--save] [--path PATH] [--only-video] [--cookies COOKIES]
```

| Option               | Default                          | Description                                                                                                                                                             |
| -------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `urls`               | **Required**                     | Single URL, comma/space-separated list, or path to text file with URLs (one per line, `#` for comments)                                                                 |
| `--codec`, `-c`      | `m4a` (macOS)<br>`opus` (others) | **Audio:** `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac`<br>**Video:** `mp4`, `mov`, `mkv`, `webm`, `avi`, `flv`                                         |
| `--kbps`, `-K`       | `256`                            | Audio bitrate in kbps (64–320). Higher = better quality, larger file                                                                                                    |
| `--quality`, `-Q`    | `best`                           | Video quality preset: `best`, `worst`, `2160p`, `1440p`, `1080p`, `720p`, `480p`, `360p`, `240p`, `144p`, or custom height (e.g., `720`)                                |
| `--jobs`, `-j`       | `5`                              | Maximum number of concurrent downloads for faster batch processing                                                                                                      |
| `--quiet`, `-q`      | `False`                          | Suppress yt-dlp output messages (errors still shown)                                                                                                                    |
| `--no-metadata`      | `False`                          | Disable embedding metadata (title, artist, album) and thumbnail into audio files                                                                                        |
| `--keep`, `-k`       | `False`                          | Keep the original downloaded file after conversion/post-processing                                                                                                      |
| `--save`, `-s`       | `False`                          | Save settings (except URL) to config file                                                                                                                               |
| `--use-config`, `-u` | `False`                          | Use saved parameters from config file as defaults                                                                                                                       |
| `--path`, `-p`       | Configured path                  | Custom download directory (overrides default config)                                                                                                                    |
| `--only-video`, `-v` | `False`                          | Download video file without audio track                                                                                                                                 |
| `--cookies`, `-C`    | `None`                           | Browser name: `brave`, `chrome`, `chromium`, `edge`, `opera`, `vivaldi`, `whale`, `firefox`, `safari`<br>Or path to cookies file (`.txt`, `.sqlite`, `.db`, `.cookies`) |

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

| Option | Default      | Description                                                                                                       |
| ------ | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `path` | **Required** | Default directory path for downloads. Use absolute path for best results (e.g., `/home/user/Music` or `C:\Music`) |

**Config Location:**

- **Windows:** `%LOCALAPPDATA%/fm-dlp/config.toml`
- **macOS:** `~/Library/Application Support/fm-dlp/config.toml`
- **Linux:** `~/.config/fm-dlp/config.toml`

---

## 💡 Examples

### Basic Download

Example of downloading a track from YouTube Music:

```bash
fm-dlp download https://music.youtube.com/watch?v=0KNxOBerr_8
```

<details>
<summary>📦 Example Output</summary>

```text
Starting: https://music.youtube.com/watch?v=0KNxOBerr_8

[youtube] Extracting URL: https://music.youtube.com/watch?v=0KNxOBerr_8
[youtube] 0KNxOBerr_8: Downloading webpage
[youtube] 0KNxOBerr_8: Downloading android vr player API JSON
[info] 0KNxOBerr_8: Downloading 1 format(s): 251
[info] Downloading video thumbnail 41 ...
[info] Writing video thumbnail 41 to: /home/user/Music/Lexapro Delirium.webp
[download] Destination: /home/user/Music/Lexapro Delirium.webm
[download] 100% of    6.53MiB in 00:00:01 at 5.74MiB/s
[ExtractAudio] Destination: /home/user/Music/Lexapro Delirium.opus
Deleting original file /home/user/Music/Lexapro Delirium.webm (pass -k to keep)
[Metadata] Adding metadata to "/home/user/Music/Lexapro Delirium.opus"
[ThumbnailsConvertor] Converting thumbnail "/home/user/Music/Lexapro Delirium.webp" to png
[EmbedThumbnail] mutagen: Adding thumbnail to "/home/user/Music/Lexapro Delirium.opus"

Success: https://music.youtube.com/watch?v=0KNxOBerr_8
```

</details>

### Search Examples

Search for tracks, albums, and videos:

```bash
# Search for tracks on YouTube Music
fm-dlp search "Sewerslvt" --limit 1

# Search for albums
fm-dlp search "Draining Love Story" --album -l 1

# Search for videos on YouTube
fm-dlp search "Sewerslvt goodbye" --yt-video -l 1
```

---

## 📊 Search Output Examples

Examples of formatting search results from different sources.

### 🎵 YTMusic (Track)

    1. Mr. Kill Myself
        ├─ Sewerslvt
        ├─ Draining Love Story
        ├─ 13M │ 7:52
        └─ https://music.youtube.com/watch?v=y55fzyXZDSE
           ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Album
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

### 💿 YTMusic (Album)

    1. Draining Love Story
        ├─ Sewerslvt
        ├─ 2020
        └─ https://music.youtube.com/playlist?list=OLAK5uy_lwWVcID2Sw8o6Jfa9vz8-a2hqEFffKb-g
           ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Year
        └─ URL
           ──────────────────────────────────────────────────

### ▶️ YouTube (Video)

    1. Sewerslvt - goodbye
        ├─ Sewerslvt
        ├─ 2,405,647 │ 17:01
        └─ https://youtu.be/ABBpsy6rlVU
           ──────────────────────────────────────────────────

    N. Title
        ├─ Artist
        ├─ Views │ Duration
        └─ URL
           ──────────────────────────────────────────────────

---

### 🧩 Formatting Legend

| Element            | Description                               |
| ------------------ | ----------------------------------------- |
| `N.`               | Sequential number of search result        |
| `Title`            | Track, album, or video title              |
| `Artist`           | Artist or channel name                    |
| `├─└─│`            | Tree branch characters                    |
| `Views │ Duration` | View count and length (MM:SS or HH:MM:SS) |
| `URL`              | Direct link to content                    |
| `───`              | Visual separator line                     |

---

## 📄 License & Acknowledgments

AGPLv3 License — Built with:

| Library                                                  | Purpose   |
| -------------------------------------------------------- | --------- |
| [fm-dlp-core](https://github.com/Fkernel653/fm-dlp-core) | Main core |

**Author:** [Fkernel653](https://github.com/Fkernel653)

**Project:** [GitHub](https://github.com/Fkernel653/fm-dlp) • [PyPI](https://pypi.org/project/fm-dlp)
