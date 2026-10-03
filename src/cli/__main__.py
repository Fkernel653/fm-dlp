try:
    from cli.cli import main

    main()
except KeyboardInterrupt:
    import sys

    sys.exit(0)
