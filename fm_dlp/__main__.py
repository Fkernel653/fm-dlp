from fm_dlp.cli import main

try:
    main()
except KeyboardInterrupt:
    import sys

    sys.exit(0)
