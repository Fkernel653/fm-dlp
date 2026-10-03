try:
    from fm_dlp.cli import main

    main()
except KeyboardInterrupt:
    import sys

    sys.exit(0)
