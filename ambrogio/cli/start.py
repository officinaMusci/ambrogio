from threading import Thread

from ambrogio.cli.prompt import Prompt
from ambrogio.cli.dashboard import Dashboard
from ambrogio.environment import init_env
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.utils.threading import exit_event


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
            procedure_list
        )

        procedure = procedure_loader.load(procedure_name)
        procedure = procedure()

        dashboard = Dashboard(procedure)

        show_dashboard_thread = Thread(target=dashboard.show)
        show_dashboard_thread.start()

        try:
            procedure._execute()
        
        except Exception as e:
            exit_event.set()
            raise e

        show_dashboard_thread.join()


    else:
        print(
            f"The {config['settings']['procedure_module']}"
            ' module doesn\'t contain any Procedure class'
        )