import sys
from typing import Any, TextIO


def echo(text: Any, file: TextIO = sys.stdout):
    """Print message to file.

    :param text: message to print
    :param file: file to print(default: stdout)
    :return: None
    """
    file.write(text)
    file.flush
