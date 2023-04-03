import os
from pathlib import Path
import signal
import logging

from rich.logging import RichHandler
from rich import traceback

from ambrogio.cli.start import start
from ambrogio.cli.prompt import Prompt, ask_for_interrupt
from ambrogio.environment import get_closest_ini
from ambrogio.utils.project import create_project


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks = True)]
)

traceback.install(show_locals = True)


available_commands = {
    'init': 'Create a new project',
    'create': 'Create a new procedure',
    'start': 'Start the project'
}


def execute():
    """
    Run Ambrogio via command-line interface.
    """
    
    signal.signal(signal.SIGINT, ask_for_interrupt)

    if not get_closest_ini('.'):
        create = Prompt.confirm('No Ambrogio project found. Do you want to create one?')

        if create:
            project_name = Prompt.text('Type the project name')
            
            if project_name:
                create_project(project_name)

                project_path: Path = Path('.') / project_name
                os.chdir(project_path.resolve())

                start()

    else:
        start()