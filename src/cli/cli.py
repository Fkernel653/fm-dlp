def main():
    """
    Main entry point for fm-dlp CLI.

    Parses arguments and dispatches to one of three subcommands:
        - search:   query YouTube/YTMusic and stream results to stdout.
        - download: validate and run the async downloader for a given URL.
        - config:   persist the default download directory.

    Global flags:
        -V/--version : print version and exit.
        --no-color   : disable ANSI colors for the whole session.

    Heavy imports are done lazily so --help/--version stay fast.
    KeyboardInterrupt is caught for a clean Ctrl+C exit.
    """
    try:
        """Set up the root parser, global flags, and subparsers."""
        import argparse

        from .parsers import (
            create_config_parser,
            create_download_parser,
            create_search_parser,
        )

        parser = argparse.ArgumentParser(
            prog="fm-dlp",
            description="CLI tool for searching YouTube/YTMusic and downloading audio/video from 1000+ sites",
        )
        parser.add_argument("-V", "--version", action="version", version="4.7.8")
        parser.add_argument(
            "--no-color",
            action="store_true",
            help="Disable colored output globally",
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        create_search_parser(subparsers)
        create_download_parser(subparsers)
        create_config_parser(subparsers)

        args = parser.parse_args()
        color = not args.no_color

        if args.command == "search":
            """Search YouTube/YTMusic and echo each formatted result."""
            from fm_dlp_core import Search, echo

            for result in Search(
                args.query,
                args.limit,
                args.yt_video,
                args.album,
                args.raw,
                args.only_url,
                color,
            ).search():
                echo(result)

        elif args.command == "download":
            """Resolve path, validate request, then run the async downloader."""
            from fm_dlp_core.utils.config import ConfigParams, PathManager

            from .validate_download import ValidateDownload

            path = args.path or PathManager(ConfigParams(color=color)).get_path()

            ValidateDownload(
                args.url,
                args.quality,
                path,
                args.ffmpeg_path,
                args.cookies,
                color,
            ).validate()

            import asyncio

            from fm_dlp_core import DownloadParams, run_downloader

            asyncio.run(
                run_downloader(
                    DownloadParams(
                        url=args.url,
                        codec=args.codec,
                        kbps=args.kbps,
                        quality=args.quality,
                        jobs=args.jobs,
                        quiet=args.quiet,
                        metadata=args.metadata,
                        keep=args.keep,
                        save=args.save,
                        use_config=args.use_config,
                        path=path,
                        ffmpeg_path=args.ffmpeg_path,
                        config_file=args.config_file,
                        only_video=args.only_video,
                        cookies=args.cookies,
                        remote=args.remote,
                        subtitles=args.subtitles,
                        subtitle_langs=args.subtitle_langs,
                        embed_subs=args.embed_subs,
                        auto_subs=args.auto_subs,
                        color=color,
                        ytdlp_args=args.ytdlp_args,
                    )
                )
            )

        elif args.command == "config":
            """Persist the download directory to the config file."""
            from fm_dlp_core.utils.config import ConfigParams, PathManager

            PathManager(ConfigParams(args.quiet, color, args.config_file)).set_path(
                args.path
            )

    except KeyboardInterrupt:
        return
