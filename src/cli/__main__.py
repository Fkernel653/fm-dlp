try:
    from src.cli.cli import main

    main()
except KeyboardInterrupt:
    import sys

    sys.exit(0)
