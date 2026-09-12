def create_download_parser(subparsers):
    import os

    from fm_dlp_core.utils import ALL_CODECS

    cpu_count = os.cpu_count() or 1
    choices_jobs = range(1, cpu_count + 1)
    default_jobs = min(5, cpu_count)
    metavar_jobs = f"1-{cpu_count}" if cpu_count > 1 else "1"

    download_parser = subparsers.add_parser(
        "download",
        help="Download audio or video content from supported platforms",
        description="Download audio or video content from supported platforms",
    )
    add_arg = download_parser.add_argument

    add_arg(
        "url",
        help="Single URL or comma/space-separated list of URLs. Can also be a path to a text file containing URLs (one per line).",
    )
    add_arg(
        "-c",
        "--codec",
        type=str,
        choices=ALL_CODECS,
        default="opus",
        help="Audio codec or video container. Default depends on platform. For audio: mp3, aac, flac, m4a, opus, vorbis, wav, alac. For video: mp4, mov, mkv, webm, avi, flv. (default: opus)",
    )
    add_arg(
        "-K",
        "--kbps",
        type=int,
        choices=range(64, 321, 64),
        default=256,
        help="Audio bitrate in kbps (64–320). Higher bitrate = better quality but larger file size. (default: 256)",
    )
    add_arg(
        "-Q",
        "--quality",
        type=str,
        default="best",
        help="Video quality preset: best, worst, 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p, or custom height (e.g., 720). (default: best)",
    )
    add_arg(
        "-j",
        "--jobs",
        type=int,
        choices=choices_jobs,
        default=default_jobs,
        metavar=metavar_jobs,
        help=f"Maximum number of concurrent downloads. Increase for faster batch downloads. (default: {default_jobs})",
    )
    add_arg(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress yt-dlp output messages. Errors will still be shown.",
    )
    add_arg(
        "--no-metadata",
        action="store_false",
        dest="metadata",
        help="Disable embedding metadata (title, artist, album) and thumbnail into audio files.",
    )
    add_arg(
        "-k",
        "--keep",
        action="store_true",
        help="Keep the original downloaded file after conversion/post-processing. Useful when you want to retain both the original and converted versions.",
    )
    add_arg("-s", "--save", action="store_true", help="Saving settings (except URL)")
    add_arg(
        "-u",
        "--use-config",
        action="store_true",
        help="Use saved parameters from config file as defaults.",
    )
    add_arg(
        "-p",
        "--path",
        help="Custom download directory path. Uses configured default if not specified.",
    )
    add_arg(
        "-v",
        "--only-video",
        action="store_true",
        help="Download a video file without audio track (video-only). Useful for editing, re-encoding, or when audio is not needed.",
    )
    add_arg(
        "-C",
        "--cookies",
        help="Path to cookies file (e.g., 'cookies.txt') for authenticated downloads, or browser name ('brave', 'chrome', 'chromium', 'edge', 'opera', 'vivaldi', 'whale', 'firefox', 'safari') to extract cookies from browser.",
    )
    add_arg(
        "-r",
        "--remote",
        choices={"ejs:github", "ejs:npm"},
        help="Download external JavaScript components for bypassing anti-bot protections (e.g., JS challenges).\n'ejs:github' - download from yt-dlp GitHub repository,\n'ejs:npm' - download from NPM package registry.",
    )
