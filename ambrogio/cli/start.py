import os
import psutil
from threading import Thread
from inspect import getsource
from time import sleep

from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.syntax import Syntax
from rich.live import Live

from ambrogio.cli.prompt import Prompt
from ambrogio.environment import init_env
from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.utils.threading import check_events, exit_event
from ambrogio.utils.memory import format_bytes
from ambrogio.utils.time import Timer


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

        show_dashboard_thread = Thread(
            target=show_dashboard,
            args=(procedure,)
        )
        
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


def show_dashboard(procedure):
    process = psutil.Process(os.getpid())
    timer = Timer()

    def generate_dashboard():
        performance_table = Table(
            show_header=True,
            header_style='bold',
            expand=True   
        )
        
        performance_table.add_column('Elapsed time', justify='right')
        performance_table.add_column('Memory', justify='right')
        performance_table.add_column('CPU', justify='right', min_width=10)
        performance_table.add_column('Threads', justify='right')

        performance_table.add_row(
            timer.elapsed_time,
            format_bytes(process.memory_info().rss),
            f"{process.cpu_percent():.2f} %",
            f"{process.num_threads()}"
        )

        layout = Layout(name='root')

        layout.split(
            Layout(name='header', size=3),
            Layout(ratio=1, name='main')
        )

        layout['header'].update(
            Panel(
                f"Procedure: {procedure.name}",
                title='Ambrogio'
            )
        )
        
        layout['main'].split_row(
            Layout(name='procedure_status', ratio=1),
            Layout(name='console', ratio=2)
        )
        
        layout['procedure_status'].split_column(
            Layout(name='performances', size=7),
            Layout(name='progress', size=3),
            Layout(name='current_step_function', ratio=1)
        )
        
        layout['procedure_status']['performances'].update(
            Panel(
                performance_table,
                title='Performances'
            )
        )

        layout['procedure_status']['progress'].update(
            Panel(
                ProgressBar(
                    total=procedure.total_steps,
                    completed=procedure.completed_steps,
                    finished_style='green'
                ),
                title="Progress"
            )
        )

        layout['procedure_status']['current_step_function'].update(
            Panel(
                Syntax(
                    getsource(procedure.current_step['function'])
                        if procedure.current_step
                        else '',
                    'python',
                    line_numbers=True
                ),
                title='Current step function'
            )
        )

        layout['main']['console'].update(
            Panel(
                '',
                title='Console'
            )
        )

        return layout

    with Live(generate_dashboard(), refresh_per_second=10) as live:
        while not procedure.finished and check_events():
            live.update(generate_dashboard())
            sleep(.1)