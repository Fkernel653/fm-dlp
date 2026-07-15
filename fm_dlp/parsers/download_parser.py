def create_download_parser(subparsers) -> None:
    """Create and configure the download command parser.

    Args:
        subparsers: Subparsers object from argparse.ArgumentParser.
    """

    download_parser = subparsers.add_parser(
        "download",
        help="Download audio or video content from supported platforms",
        description="Download audio or video content from supported platforms",
    )
    download_parser.add_argument(
        "url",
        help="Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).",
    )
    download_parser.add_argument(
        "-c",
        "--codec",
        help="Audio codec or video container. Default depends on platform. For audio: mp3, aac, flac, m4a, opus, vorbis, wav, alac. For video: mp4, mov, mkv, webm, avi, flv.",
    )
    download_parser.add_argument(
        "-k",
        "--kbps",
        type=int,
        default=256,
        help="Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size. (default: 256)",
    )
    download_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=5,
        help="Maximum number of concurrent downloads. Increase for faster batch downloads. (default: 5)",
    )
    download_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress yt-dlp output messages. Errors will still be shown.",
    )
    download_parser.add_argument(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        help="Disable embedding metadata (title, artist, album) and thumbnail into audio files.",
    )
    download_parser.add_argument(
        "-s", "--save", action="store_true", help="Saving settings (except URL)"
    )
    download_parser.add_argument(
        "-u",
        "--use-config",
        action="store_true",
        help="Use saved parameters from config file as defaults.",
    )
    download_parser.add_argument(
        "-p",
        "--path",
        help="Custom download directory path. Uses configured default if not specified.",
    )
    download_parser.add_argument(
        "-v",
        "--only-video",
        action="store_true",
        help="Download a video file without audio track (video-only). Useful for editing, re-encoding, or when audio is not needed.",
    )
    download_parser.add_argument(
        "-C",
        "--cookies",
        help="Path to cookies file (e.g., 'cookies.txt') for authenticated downloads, or browser name ('brave', 'chrome', 'chromium', 'edge', 'opera', 'vivaldi', 'whale', 'firefox', 'safari') to extract cookies from browser.",
    )
