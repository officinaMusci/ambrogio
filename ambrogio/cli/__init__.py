import sys
import logging
import signal

from rich.logging import RichHandler

from ambrogio.environment import init_env
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.cli.prompt import Prompt


logger = logging.getLogger('ambrogio')
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
    Run Ambrogio via command-line tool
    """

    signal.signal(signal.SIGINT, interrupt_handler)
    
    conf = init_env()
    
    procedure_loader = ProcedureLoader(conf)
    procedure_list = procedure_loader.list()

    if len(procedure_list):
        procedure_name = Prompt.list(
            'Choose a procedure to run',
            procedure_list
        )

        procedure_loader.run(procedure_name)

    else:
        logger.warning(
            f"The {conf['settings']['procedure_module']}"
            ' module doesn\'t contain any Procedure class'
        )