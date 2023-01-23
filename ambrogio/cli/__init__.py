import sys
import signal

from ambrogio.environment import init_env
from ambrogio.utils.project import create_project
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.cli.prompt import Prompt


def _interrupt_handler():
    """
    On KeyboardInterrupt, ask the user to confirm interrupting the program.
    """

    confirm = Prompt.confirm(
        'Are you sure you want to interrupt the program?',
        default=True
    )

    if confirm:
        sys.exit(0)


def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


available_commands = {
    'init': 'Create new project',
    'start': 'Start the project'
}


def execute(argv = None):
    """
    Run Ambrogio via command-line tool.
    """
    
    signal.signal(signal.SIGINT, _interrupt_handler)

    if argv is None:
        argv = sys.argv

    command_name = _pop_command_name(argv)

    # Create a new project
    if command_name == 'init':
        project_name = Prompt.text('Type the project name')
        create_project(project_name)

    # Run a procedure
    elif command_name == 'start':
        config = init_env()
        procedure_module = config['settings']['procedure_module']
            
        procedure_loader = ProcedureLoader(procedure_module)
        procedure_list = procedure_loader.list()

        if len(procedure_list):
            procedure_name = Prompt.list(
                'Choose a procedure to run',
                procedure_list
            )

            procedure_loader.run(procedure_name)

        else:
            print(
                f"The {procedure_module}"
                ' module doesn\'t contain any Procedure class'
            )

    elif not command_name:
        print("Usage:")
        print("  ambrogio <command>\n")
        print("Available commands:")

        for name, description in available_commands.items():
            print(f"  {name:<13} {description}")
    
    else:
        print(f"Unknown command: {command_name}\n")
        print('Use \"ambrogio\" to see available commands')