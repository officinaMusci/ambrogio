import os
import psutil
from threading import Thread
from datetime import datetime
from time import sleep

from rich.live import Live
from rich.table import Table

from ambrogio.cli.prompt import Prompt
from ambrogio.environment import init_env
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.utils.threading import exit_event, pause_event
from ambrogio.utils.memory import format_bytes


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

        show_performances_thread = Thread(
            target=show_performances,
            args=(procedure_name,)
        )
        
        show_performances_thread.start()

        try:
            procedure_loader.run(procedure_name)
        
        except Exception as e:
            exit_event.set()
            raise e

        show_performances_thread.join()


    else:
        print(
            f"The {config['settings']['procedure_module']}"
            ' module doesn\'t contain any Procedure class'
        )


def show_performances(procedure_name):
    process = psutil.Process(os.getpid())

    def generate_table():
        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('Elapsed time', justify='right', style='cyan')
        table.add_column('Memory', justify='right', style='magenta')
        table.add_column('CPU', justify='right', style='green')

        table.add_row(
            f"{datetime.now().timestamp() - process.create_time():.2f}",
            format_bytes(process.memory_info().rss),
            f"{process.cpu_percent():.2f} %"
        )

        return table

    with Live(generate_table(), refresh_per_second=10) as live:
        while not exit_event.is_set() and not pause_event.is_set():
            live.update(generate_table())
            sleep(.1)


