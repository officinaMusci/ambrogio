import logging

from rich.logging import RichHandler
from rich import traceback

from ambrogio.cli import execute


# Set up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level='NOTSET',
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks = True)]
)
traceback.install(show_locals = True)


# Run the CLI
if __name__ == "__main__":
    execute()