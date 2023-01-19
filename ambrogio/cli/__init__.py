import logging
import sys
import os
import signal
from functools import partial

from rich.logging import RichHandler
from rich.prompt import Prompt

from ambrogio.procedures.loader import ProcedureLoader


logger = logging.getLogger()
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.setLevel('DEBUG')


def interrupt_handler(signum, frame, ask=True):
    print('\n')

    logger.warning(f'Handling signal {signum} ({signal.Signals(signum).name}).')

    if ask:
        signal.signal(signal.SIGINT, partial(interrupt_handler, ask=False))
        logger.info('To confirm interrupt, press ctrl-c again.')
        return

    sys.exit(0)


def execute():
    signal.signal(signal.SIGINT, interrupt_handler)
    sys.path.append(os.getcwd())
    
    procedure_loader = ProcedureLoader()

    procedure_name = Prompt.ask(
        'Choose a procedure to run',
        choices=procedure_loader.list()
    )

    procedure_loader.run(procedure_name)