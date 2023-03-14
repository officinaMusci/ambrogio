import sys
import signal
import logging

from ambrogio.cli.start import start
from ambrogio.cli.prompt import Prompt
from ambrogio.environment import get_closest_ini
from ambrogio.utils.project import create_project
from ambrogio.utils.threading import exit_event

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


def _interrupt_handler(*args):
    """
    On KeyboardInterrupt, ask the user to confirm interrupting the program.
    """

    confirm = Prompt.confirm(
        'Are you sure you want to interrupt the program?',
        default=True
    )

    if confirm:
        exit_event.set()

        print('Interrupting program...')
        
        sys.exit(0)


def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


available_commands = {
    'init': 'Create a new project',
    'create': 'Create a new procedure',
    'start': 'Start the project'
}


def execute():
    """
    Run Ambrogio via command-line interface.
    """
    
    signal.signal(signal.SIGINT, _interrupt_handler)

    if not get_closest_ini('.'):
        create = Prompt.confirm('No Ambrogio project found. Do you want to create one?')

        # Create a new project
        if create:
            project_name = Prompt.text('Type the project name')
            if project_name:
                create_project(project_name)

    else:
        start()