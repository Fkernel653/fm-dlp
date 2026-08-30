import sys

from fm_dlp.cli import main

try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
