"""
Command handlers for fm-dlp CLI.
"""

import sys

from color_kiss import GREEN, RED, RESET


def handle_search(args) -> None:
    """Handle the search command.

    Args:
        args: Parsed command-line arguments.
    """
    try:
        from modules.commands.search import Search
        from modules.utils.validator import validate_input

        validate_input(
            limit=args.limit,
            platform=args.platform,
            type=args.type,
            proxy=args.proxy,
            proxy_only_http=(args.platform == "yt-music"),
        )

        program = Search(args.query, args.limit, args.type, args.proxy)

        match args.platform:
            case "yt-video":
                for video_info in program.yt_video():
                    print(video_info)
            case "yt-music":
                for track_info in program.yt_music():
                    print(track_info)

    except Exception as e:
        print(f"\n{RED}Search Error:{RESET} {e}")
        sys.exit(1)


def handle_download(args) -> None:
    """Handle the download command.

    Args:
        args: Parsed command-line arguments.
    """
    try:
        from modules.utils.validator import (
            AUDIO_CODECS,
            DEFAULT_CODEC,
            validate_input,
            validate_with_shutil,
        )

        # Set default codec
        codec = args.codec if args.codec is not None else DEFAULT_CODEC

        # Validate inputs
        validate_input(
            url=args.urls,
            codec=codec,
            kbps=args.kbps,
            max_concurrent=args.max_concurrent,
            proxy=args.proxy,
        )

        # Check ffmpeg only for audio codecs
        if codec in AUDIO_CODECS:
            validate_with_shutil("ffmpeg", "FFmpeg")

        # WAV doesn't support metadata
        if codec == "wav" and args.metadata:
            args.metadata = False
            print(f"{GREEN}Note:{RESET} WAV format doesn't support metadata embedding")

        import asyncio

        from modules.commands.download import Download

        async def run_download():
            async with Download(
                args.urls,
                codec,
                args.kbps,
                args.quiet,
                args.max_concurrent,
                args.metadata,
                args.cookies,
                args.proxy,
            ) as downloader:
                await downloader.download_all()

        asyncio.run(run_download())

    except Exception as e:
        print(f"\n{RED}Download Error:{RESET} {e}")
        sys.exit(1)


def handle_config(args) -> None:
    """Handle the config command.

    Args:
        args: Parsed command-line arguments.
    """
    try:
        from modules.utils.configer import set_path

        print(set_path(args.path))
    except Exception as e:
        print(f"\n{RED}Configuration Error:{RESET} {e}")
        sys.exit(1)
