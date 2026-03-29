# FM-dlp - YouTube Music Downloader

A powerful command-line tool for searching and downloading audio from YouTube videos. Built with Python, this tool uses scrapetube for searching (no API key required!) and yt-dlp for high-quality audio extraction.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)

## 📋 Features

- **YouTube Video Search**: Search for videos using scrapetube (no API key needed!)
- **Smart Result Filtering**: Automatically filters results to ensure query appears in title or channel name
- **High-Quality Audio Download**: Extract audio in M4A format at 256 kbps quality
- **Configurable Download Path**: Set and save your preferred download directory persistently
- **User-Friendly Interface**: Colorful terminal output with intuitive command system
- **Random User Agents**: Avoid detection by rotating user agents for each request
- **Comprehensive Error Handling**: Graceful handling of network errors, API limits, and user interruptions
- **Search Results Display**: View video titles, channels, upload dates, view counts, durations, and direct URLs

## 🚀 Installation

### Prerequisites

- **Python 3.6 or higher** - Check with `python --version`
- **FFmpeg** - Required for audio extraction (must be installed system-wide)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [FFmpeg official website](https://ffmpeg.org/download.html)
2. Extract the archive
3. Add the `bin` folder to your system PATH
4. Verify with `ffmpeg -version` in Command Prompt

### Install FM-dlp

1. Clone the repository:
```bash
git clone https://github.com/Fkernel653/fm-dlp.git
cd fm-dlp
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

### Requirements

The `requirements.txt` file includes:
```
fake-useragent
scrapetube
yt-dlp
clite
```

## 🔧 Configuration

### Download Path Configuration

Set your default download directory using the config command:
```bash
python fm-dlp.py config /path/to/your/music/folder
```

The path is saved in `config.json` for future sessions. To view the current configuration:
```bash
python fm-dlp.py config
```

## 📖 Usage

Run the program with any of the following commands:

```bash
python fm-dlp.py <command> [arguments]
```

### Available Commands

#### Search for Videos
```bash
python fm-dlp.py search "your query here" --limit=10
```
Example:
```bash
python fm-dlp.py search "Sewerslvt" --limit=5
```

The `--limit` parameter is optional (defaults to 10). Results are filtered to ensure your search query appears in either the video title or channel name.

Each result displays:
- Video title (in cyan)
- Channel name (in magenta)
- Upload date (in blue)
- View count (in green)
- Duration (in yellow)
- YouTube URL (in red, bold)

#### Download Audio
```bash
python fm-dlp.py download "youtube_url"
```
Example:
```bash
python fm-dlp.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Downloads will be saved to your configured directory as M4A files with 256 kbps quality.

**Note:** The download path must be configured first using the `config` command.

#### Configure Download Path
```bash
# Set a new download path
python fm-dlp.py config "/absolute/path/to/download/folder"

# View current configuration
python fm-dlp.py config
```

#### Get Help
```bash
python fm-dlp.py help
```

## 🎨 Terminal Color Scheme

The program uses consistent ANSI color codes for better readability:

| Color | Usage |
|-------|-------|
| 🔴 **Red** | Errors, warnings, and video URLs |
| 🟢 **Green** | Success messages, view counts, and goodbye |
| 🔵 **Blue** | Upload dates and information |
| 🟣 **Magenta** | Channel names and metadata |
| 🟡 **Yellow** | Video durations and warnings |
| 🔷 **Cyan** | Video titles and headings |
| **Bold White** | Numbers and emphasized text |

## 🛠️ Technical Architecture

### Module Structure

```
fm-dlp/
├── fm-dlp.py              # Main CLI entry point (using clite)
├── config.json            # Persistent configuration (auto-generated)
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
└── modules/
    ├── searching.py       # YouTube search with scrapetube
    ├── downloader.py      # Audio download with yt-dlp
    ├── configer.py        # Configuration management
    ├── helper.py          # Help menu display
    └── colors.py          # ANSI color constants
```

### Component Details

#### fm-dlp.py
- Main CLI entry point using the `clite` framework
- Defines commands: `search`, `download`, `config`, `help`
- Uses type hints for automatic argument parsing
- Delegates each command to its corresponding module

#### searching.py
- Uses `scrapetube` library to search YouTube (no API key required!)
- Filters results to ensure query relevance in title or channel name
- Returns formatted, color-coded output
- Handles network errors and keyboard interrupts gracefully

#### downloader.py
- Uses `yt-dlp` for robust video downloading
- Extracts best available audio stream
- Converts to M4A format with FFmpeg (256 kbps AAC)
- Implements random User-Agent rotation via `fake-useragent`
- Reads download path from `config.json`
- Handles georestrictions, extraction errors, and download failures

#### configer.py
- Manages JSON-based configuration
- Validates path existence
- Acts as both getter and setter
- Provides clear error messages for corrupted or missing configs

#### helper.py
- Provides help menu text with command descriptions

#### colors.py
- Defines ANSI color codes for consistent terminal styling
- Includes RESET, BOLD, ITALIC, and six standard colors

### Audio Specifications

- **Format**: M4A (MPEG-4 Audio)
- **Codec**: AAC (Advanced Audio Coding)
- **Bitrate**: 256 kbps (high quality)
- **Source**: Best available audio stream from YouTube

### Search Features

- **No API Key Required**: Uses scrapetube instead of YouTube Data API
- **Result Filtering**: Automatic filtering by title/channel relevance
- **Video Information**: Title, channel, date, views, duration, URL
- **Graceful Error Handling**: Network errors, keyboard interrupts

## ⚠️ Important Considerations

### System Requirements
- **Internet Connection**: Required for both search and download functions
- **FFmpeg**: Must be installed and accessible in system PATH
- **Disk Space**: Sufficient space for downloaded audio files
- **Write Permissions**: Download directory must be writable

### Dependencies
- **scrapetube**: Scrapes YouTube search results (no API key needed)
- **yt-dlp**: Downloads and extracts audio from YouTube videos
- **fake-useragent**: Provides random browser user agents
- **clite**: Simple CLI framework for command parsing

### Legal and Ethical Considerations
- **Respect Copyright**: Only download content you have rights to
- **Terms of Service**: Comply with YouTube's Terms of Service
- **Personal Use**: This tool is intended for personal, educational use
- **Rate Limiting**: Avoid excessive requests that could be considered abuse

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

#### 1. "No videos matching query after filtering"
**Possible causes:**
- Search query doesn't appear in any video titles or channel names
- Network connectivity issues
- YouTube may be blocking scrapetube requests

**Solutions:**
- Try a different search query (use fewer words or broader terms)
- Check your internet connection
- Wait a few minutes and try again (YouTube may temporarily block aggressive scraping)

#### 2. Download Fails
**Possible causes:**
- FFmpeg not installed
- Download path doesn't exist or isn't writable
- Video is private, age-restricted, or deleted
- URL format is incorrect

**Solutions:**
- Install FFmpeg and verify with `ffmpeg -version`
- Check if download path exists: `python fm-dlp.py config`
- Ensure URL is complete and correct
- Try downloading with a different video

#### 3. Config File Errors
**Possible causes:**
- Corrupted JSON in config.json
- Manual editing of config file
- Permission issues

**Solutions:**
- Delete config.json and reconfigure: `python fm-dlp.py config /new/path`
- Check file permissions
- Ensure config.json is valid JSON

#### 4. Connection Errors
**Possible causes:**
- Network issues
- YouTube blocking requests
- Proxy/firewall restrictions

**Solutions:**
- Check internet connection
- Try using a VPN
- Wait and retry (rate limiting may be temporary)

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### Ways to Contribute
- **Report Bugs**: Open an issue with detailed description
- **Suggest Features**: Share ideas for improvements
- **Submit Pull Requests**: Fix bugs or add features
- **Improve Documentation**: Enhance README or code comments
- **Share Feedback**: Tell us about your experience

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if applicable)
5. Submit a pull request

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings for all functions
- Include comments for complex logic
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

**MIT License Summary:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## 👨‍💻 Author

**Fkernel653**
- GitHub: [@Fkernel653](https://github.com/Fkernel653)
- Project Repository: [fm-dlp](https://github.com/Fkernel653/fm-dlp)

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - For the excellent, feature-rich downloading library
- **[scrapetube](https://github.com/dermasmid/scrapetube)** - For YouTube search without API keys
- **[clite](https://pypi.org/project/clite/)** - For the simple CLI framework
- **[fake-useragent](https://github.com/hellysmile/fake-useragent)** - For User-Agent rotation
- All contributors and users of this tool

## 📊 Version History

**v1.0.0** (Current)
- Initial release
- YouTube search with scrapetube (no API key!)
- Audio download with yt-dlp
- Configuration management
- Color-coded terminal output

**Planned Features**
- Playlist download support
- Search result pagination
- Download progress improvements
- Multiple audio format options
- Batch download from file

## ⭐ Support the Project

If you find this tool useful, please consider:
- **Starring** the repository on GitHub
- **Forking** to contribute improvements
- **Sharing** with others who might find it useful
- **Reporting** issues you encounter

---

**Disclaimer**: This tool is for educational purposes only. Users are responsible for complying with YouTube's Terms of Service, copyright laws, and all applicable regulations. The developers assume no liability for misuse of this software.