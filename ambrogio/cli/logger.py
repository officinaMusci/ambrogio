import logging

from rich.logging import RichHandler
from rich import traceback


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks = True)]
)

traceback.install(show_locals = True)

logger = logging.getLogger('Ambrogio')