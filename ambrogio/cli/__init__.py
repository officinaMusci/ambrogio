import sys
import signal
import logging

from ambrogio.cli.start import start
from ambrogio.cli.prompt import Prompt
from ambrogio.utils.project import create_project, create_procedure
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


def execute(argv = None):
    """
    Run Ambrogio via command-line interface.
    """
    
    signal.signal(signal.SIGINT, _interrupt_handler)

    if argv is None:
        argv = sys.argv

    command_name = _pop_command_name(argv)

    # Create a new project
    if command_name == 'init':
        project_name = Prompt.text('Type the project name')
        if project_name:
            create_project(project_name)

    # Create a new procedure
    if command_name == 'create':
        procedure_name = Prompt.text('Type the procedure name')
        if procedure_name:
            create_procedure(procedure_name)

    # Start the project
    elif command_name == 'start':
        start()

    elif not command_name:
        print("Usage:")
        print("  ambrogio <command>\n")
        print("Available commands:")

        for name, description in available_commands.items():
            print(f"  {name:<13} {description}")
    
    else:
        print(f"Unknown command: {command_name}\n")
        print('Use \"ambrogio\" to see available commands')