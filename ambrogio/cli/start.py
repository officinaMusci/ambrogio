from threading import Thread
from time import sleep

from ambrogio.cli.prompt import Prompt
from ambrogio.cli.dashboard import Dashboard
from ambrogio.environment import init_env
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.utils.project import create_procedure
from ambrogio.utils.threading import exit_event


def prompt_create_procedure(config):
    """
    Prompt the user for a procedure name and type.
    """

    procedure_name = Prompt.text('Type the procedure name')
    procedure_type = Prompt.list('Select the procedure type', [
        ('Basic procedure', 'basic'),
        ('Step procedure', 'step')
    ])

    if procedure_name and procedure_type:
        create_procedure(procedure_name, procedure_type)

        print(
            f"Procedure '{procedure_name}' created successfully"
            f" in '{config['settings']['procedure_module']}' module"
        )


def start():
    """
    Prompt the user for a procedure to start a procedure with
    live performances monitoring.
    """
    config = init_env()
            
    procedure_loader = ProcedureLoader(config)
    procedure_list = procedure_loader.list()

    if len(procedure_list):
        procedure_name = Prompt.list(
            'Choose a procedure to run',
            [*procedure_list, ('Create a new procedure', None)]
        )

        if not procedure_name:
            prompt_create_procedure(config)

        else:
            procedure = procedure_loader.load(procedure_name)

            procedure_needs_params = procedure._check_params(False)
            if not procedure_needs_params:
                procedure_needs_params = Prompt.confirm(
                    'Do you want to change the default parameters?'
                )
            
            if procedure_needs_params:
                procedure._prompt_params()
            
            procedure = procedure(config)

            dashboard = Dashboard(procedure)

            show_dashboard_thread = Thread(target=dashboard.show)
            show_dashboard_thread.start()

            try:
                procedure._execute()
            
            except Exception as e:
                exit_event.set()
                sleep(1)
                raise e

            show_dashboard_thread.join()


    else:
        print(
            f"The '{config['settings']['procedure_module']}'"
            ' module doesn\'t contain any Procedure class'
        )

        create = Prompt.confirm('Do you want to create a new procedure?')

        if create:
            prompt_create_procedure(config)