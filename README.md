# fm-dlp — Download from YouTube, YTMusic, and 1000+ sites

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/fm-dlp?style=for-the-badge&logo=pypi&logoColor=fff&label=PyPI&color=007ec6)](https://pypi.org/project/fm-dlp)
[![License](https://img.shields.io/badge/License-AGPLv3-00b96b?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-9cf?style=for-the-badge)](<>)
[![Ruff](https://img.shields.io/badge/Code%20Style-Ruff-ff69b4?logo=ruff&logoColor=fff&style=for-the-badge)](https://docs.astral.sh/ruff)

**fm-dlp** is a CLI tool for searching YouTube/YTMusic and downloading audio/video from [1000+ sites](https://github.com/yt-dlp/yt-dlp/supportedsites.md)

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Requirements](#️-requirements)
- [Color Output](#-color-output)
- [Commands](#-commands)
  - [`search`](#search)
  - [`download`](#download)
  - [`config`](#config)
- [Examples](#-examples)
  - [Basic Download](#basic-download)
  - [Search Examples](#search-examples)
  - [Subtitles](#-subtitles)
  - [Raw yt-dlp Arguments](#-raw-yt-dlp-arguments)
- [Search Output Examples](#-search-output-examples)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🚀 Quick Start

```bash
pip install fm-dlp                    # Python 3.11+ & FFmpeg required
fm-dlp config ~/Music                 # Set download directory
fm-dlp search "Sewerslvt"             # Search tracks
fm-dlp download "URL"                 # Download audio
```

---

## ⚙️ Requirements

- **Python 3.11+** - TOML support required
- **FFmpeg** - Required for audio/video processing and subtitle embedding. Install via:
  - **macOS:** `brew install ffmpeg`
  - **Linux:**
    - **Debian:** `sudo apt install ffmpeg`
    - **Fedora:** `sudo dnf install ffmpeg`
    - **Arch Linux:** `sudo pacman -S ffmpeg`
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

| Option             | Default | Description                                               |
| ------------------ | ------- | --------------------------------------------------------- |
| `query`            | **Req** | Search query string                                       |
| `--limit N`, `-l`  | `10`    | Maximum number of results to return (1-100)               |
| `--yt-video`, `-v` | `False` | Search for YouTube videos instead of music tracks         |
| `--album`, `-a`    | `False` | Search for albums instead of individual tracks            |
| `--raw`, `-r`      | `False` | Output results in raw format (Python dict representation) |
| `--only-url`, `-u` | `False` | Output only the URLs without any formatting               |

---

### `download`

Download audio or video content from supported platforms (YouTube, YTMusic, and 1000+ sites).

```bash
fm-dlp download <urls> [OPTIONS]
```

| Option               | Default         | Description                                                                                                                                                             |
| -------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `urls`               | **Required**    | Single URL, comma/space-separated list, or path to text file with URLs (one per line)                                                                                   |
| `--codec`, `-c`      | `opus`          | **Audio:** `mp3`, `aac`, `flac`, `m4a`, `opus`, `vorbis`, `wav`, `alac`<br>**Video:** `mp4`, `mov`, `mkv`, `webm`, `avi`, `flv`                                         |
| `--kbps`, `-K`       | `256`           | Audio bitrate in kbps (64, 128, 192, 256, 320). Higher = better quality, larger file                                                                                    |
| `--quality`, `-Q`    | `best`          | Video quality preset: `best`, `worst`, `2160p`, `1440p`, `1080p`, `720p`, `480p`, `360p`, `240p`, `144p`, or custom height (e.g., `720`)                                |
| `--jobs`, `-j`       | `5`             | Maximum number of concurrent downloads (1-24) for faster batch processing. The upper limit is automatically capped at your CPU core count (detected at runtime)         |
| `--quiet`, `-q`      | `False`         | Suppress yt-dlp output messages (errors still shown)                                                                                                                    |
| `--no-metadata`      | `False`         | Disable embedding metadata (title, artist, album) and thumbnail into audio files                                                                                        |
| `--keep`, `-k`       | `False`         | Keep the original downloaded file after conversion/post-processing                                                                                                      |
| `--save`, `-s`       | `False`         | Save settings (except URL) to config file                                                                                                                               |
| `--use-config`, `-u` | `False`         | Use saved parameters from config file as defaults                                                                                                                       |
| `--path`, `-p`       | Configured path | Custom download directory (overrides default config)                                                                                                                    |
| `--only-video`, `-v` | `False`         | Download video file without audio track                                                                                                                                 |
| `--cookies`, `-C`    | `None`          | Browser name: `brave`, `chrome`, `chromium`, `edge`, `opera`, `vivaldi`, `whale`, `firefox`, `safari`<br>Or path to cookies file (`.txt`, `.sqlite`, `.db`, `.cookies`) |
| `--remote`, `-r`     | `None`          | Download external JavaScript components for bypassing anti-bot protections.<br>**Options:** `github` (yt-dlp repo) or `npm` (NPM registry)                              |
| `--subtitles`        | `False`         | Download subtitles for the video. Use `--subtitle-langs` to specify languages                                                                                           |
| `--subtitle-langs`   | `en`            | Comma-separated subtitle language codes, e.g. `'en,ru,ja'`                                                                                                              |
| `--embed-subs`       | `False`         | Embed subtitles into the video container (requires FFmpeg)                                                                                                              |
| `--auto-subs`        | `False`         | Include auto-generated subtitles (in addition to manually uploaded ones)                                                                                                |
| `--ytdlp-args`       | `None`          | Extra yt-dlp options as a dict object. Merged last; `postprocessors` are extended, other keys override                                                                  |

> **ℹ️ CPU Detection:** When parsing the `download` command, fm-dlp automatically detects the number of CPU cores on your system. The `--jobs` option is capped at this value to prevent overloading your system. If detection fails, a fallback value is used instead.

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

<details>
<summary>Basic Download</summary>

Download a track from YouTube Music:

```bash
fm-dlp download https://music.youtube.com/watch?v=0KNxOBerr_8
```

**With custom settings:**

```bash
# Download as high-quality MP3 with metadata
fm-dlp download "URL" --codec mp3 --kbps 320 --path ~/Music/Downloads

# Download video in 1080p
fm-dlp download "URL" --quality 1080p --codec mp4

# Batch download from file
fm-dlp download urls.txt --jobs 3 --quiet

# Use saved config and cookies from browser
fm-dlp download "URL" --use-config --cookies chrome

# Download video-only and keep original file
fm-dlp download "URL" --only-video --keep
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
</details>

<details>
<summary>Search Examples</summary>

Search for tracks, albums, and videos:

```bash
# Search for tracks on YouTube Music
fm-dlp search "Sewerslvt" --limit 5

# Search for albums
fm-dlp search "Draining Love Story" --album --limit 1

# Search for videos on YouTube
fm-dlp search "Sewerslvt goodbye" --yt-video --limit 1

# Get raw data for scripting
fm-dlp search "artist" --raw

# Get only URLs for batch processing
fm-dlp search "artist" --only-url > urls.txt
```

</details>

---

<details>
<summary><b>📝 Subtitles</b></summary>

Download subtitles alongside the video, save them as separate files, or embed them directly into the video container.

#### How it works

| Flag           | yt-dlp option(s)                                           | Effect                                           |
| -------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| `--subtitles`  | `writesubtitles=True`, `subtitleslangs=[...]`              | Downloads subtitle files for the given languages |
| `--auto-subs`  | `writeautomaticsub=True`                                   | Includes auto-generated subtitles                |
| `--embed-subs` | `embedsubtitles=True`, postprocessor `FFmpegEmbedSubtitle` | Muxes subtitles into the video container         |

> ⚠️ **Embedding caveats**
>
> - Requires FFmpeg.
> - Only makes sense for **video** codecs (`mp4`, `mkv`, `webm`, `mov`) or when `--only-video` is set.
> - For audio-only codecs (mp3, flac, etc.) `--embed-subs` is silently skipped.

#### Language selection

`--subtitle-langs` is a **comma-separated** string, e.g. `"en,ru,ja"`. Whitespace is stripped. If empty, defaults to `["en"]`.

#### Examples

**Download video with English + Russian subtitles embedded into MKV**

```bash
fm-dlp download "URL" \
  --codec mkv \
  --quality 1080p \
  --only-video \
  --subtitles \
  --subtitle-langs "en,ru" \
  --embed-subs
```

**Download audio with subtitles saved as separate .srt files**

```bash
fm-dlp download "URL" \
  --codec mp3 \
  --kbps 320 \
  --subtitles \
  --subtitle-langs "en" \
  --auto-subs
```

</details>

---

<details>
<summary><b>🧩 Raw yt-dlp Arguments</b></summary>

For anything not covered by the high-level CLI, you can pass arbitrary yt-dlp options via `--ytdlp-args`.

#### Rules

- Value must be a **dict** (Python literal).
- Keys are **snake_case** yt-dlp option names (the same keys used by `YoutubeDL(opts)`).
- Options are merged **last** into the built options dict → they **override** existing values.
- **Exception:** `postprocessors` are **extended** (built-in postprocessors are preserved) rather than replaced.

#### Examples

**Add retries and a custom subtitle format**

```bash
fm-dlp download "URL" --ytdlp-args '{"retries": 10, "fragment_retries": 10, "subtitlesformat": "srt/best"}'
```

**Extend postprocessors without losing built-ins**

```bash
fm-dlp download "URL" --ytdlp-args '{"postprocessors": [{"key": "FFmpegMetadata"}, {"key": "SponsorBlock", "categories": ["sponsor"]}]}'
```

**Rate-limit requests**

```bash
fm-dlp download "URL" --ytdlp-args '{"sleep_interval_requests": 1, "sleep_interval": 2, "max_sleep_interval": 5}'
```

</details>

---

## 📊 Search Output Examples

Examples of formatting search results from different sources. Click each example to expand.

<details>
<summary>🎵 YTMusic (Track)</summary>

```
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
```

</details>

<details>
<summary>💿 YTMusic (Album)</summary>

```
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
```

</details>

<details>
<summary>▶️ YouTube (Video)</summary>

```
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
```

</details>

---

### Format Elements

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
