import logging
import sys
import os
import signal

from rich.logging import RichHandler

from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.cli.prompt import Prompt


logger = logging.getLogger()
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.setLevel('DEBUG')


def interrupt_handler():
    """
    On KeyboardInterrupt, ask the user to confirm interrupting the program
    """

    confirm = Prompt.confirm(
        'Are you sure you want to interrupt the program?',
        default=True
    )

    if confirm:
        sys.exit(0)



def execute():
    """
    Run Ambrogio via command line
    """

    signal.signal(signal.SIGINT, interrupt_handler)
    sys.path.append(os.getcwd())
    
    procedure_loader = ProcedureLoader()

    procedure_name = Prompt.list(
        'Choose a procedure to run',
        choices=procedure_loader.list()
    )

    procedure_loader.run(procedure_name)