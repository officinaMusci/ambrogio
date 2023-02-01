import os
import psutil
from threading import Thread
from time import sleep

from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

from ambrogio.cli.prompt import Prompt
from ambrogio.environment import init_env
from ambrogio.procedures import Procedure
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


def show_dashboard(procedure: Procedure):
    process = psutil.Process(os.getpid())
    timer = Timer()

    def get_performances():
        return {
            'elapsed_time': timer.elapsed_time,
            'memory': process.memory_info().rss,
            'cpu': process.cpu_percent(),
            'threads': process.num_threads()
        }

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

        performances = get_performances()

        max_memory, max_cpu, max_threads = 0, 0, 0
        for key, value in performances.items():
            if key == 'memory' and value > max_memory:
                max_memory = value
            elif key == 'cpu' and value > max_cpu:
                max_cpu = value
            elif key == 'threads' and value > max_threads:
                max_threads = value


        performance_table.add_row(
            performances['elapsed_time'],
            format_bytes(performances['memory']),
            f"{performances['cpu']:.2f} %",
            f"{performances['threads']}",
            end_section=True
        )

        performance_table.add_row(
            'Max',
            format_bytes(max_memory),
            f"{max_cpu:.2f} %",
            f"{max_threads}"
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
            Layout(name='performances', size=9),
            *procedure._additional_layouts
        )
        
        layout['procedure_status']['performances'].update(
            Panel(
                performance_table,
                title='Performances'
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