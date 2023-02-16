import os
import psutil
from time import sleep

from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

from ambrogio.procedures import Procedure
from ambrogio.utils.memory import format_bytes
from ambrogio.utils.time import Timer
from ambrogio.utils.threading import check_events


class Dashboard():
    """
    Show a dashboard with live performances monitoring.

    :param procedure: The procedure to monitor.
    """

    _max_performances: dict = {
        'memory': 0,
        'cpu': 0,
        'threads': 0
    }
    _procedure: Procedure
    _process: psutil.Process
    _timer: Timer

    def __init__(self, procedure: Procedure):
        self._procedure = procedure

    @property
    def procedure(self):
        return self._procedure

    @property
    def max_performances(self):
        return self._max_performances

    def show(self):
        """
        Show the dashboard.
        """
        
        self._process = psutil.Process(os.getpid())
        self._timer = Timer()

        with Live(self._generate_dashboard(), refresh_per_second=10) as live:
            while not self.procedure.finished and check_events():
                live.update(self._generate_dashboard())
                sleep(.1)
            
            live.update(self._generate_dashboard())

    def _get_performances(self):
        """
        Get the performances of the current process.

        :return: A dict with the performances.
        """
        
        return {
            'memory': self._process.memory_info().rss,
            'cpu': self._process.cpu_percent(),
            'threads': self._process.num_threads()
        }

    def _generate_dashboard(self):
        """
        Generate the dashboard.

        :return: A rich.layout.Layout object.
        """

        performances = self._get_performances()
        
        for key, value in performances.items():
            if value > self.max_performances[key]:
                self.max_performances[key] = value
                
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
            self._timer.elapsed_time,
            format_bytes(performances['memory']),
            f"{performances['cpu']:.2f} %",
            f"{performances['threads']}",
            end_section=True
        )

        performance_table.add_row(
            'Max',
            format_bytes(self.max_performances['memory']),
            f"{self.max_performances['cpu']:.2f} %",
            f"{self.max_performances['threads']}"
        )

        layout = Layout(name='root')

        layout.split(
            Layout(name='header', size=3),
            Layout(ratio=1, name='main')
        )

        layout['header'].update(
            Panel(
                f"Procedure: {self.procedure.name}",
                title='Ambrogio'
            )
        )
        
        layout['main'].split_row(
            Layout(name='procedure_status', ratio=1),
            Layout(name='console', ratio=2)
        )
        
        layout['procedure_status'].split_column(
            Layout(name='performances', size=9),
            *self.procedure._additional_layouts
        )
        
        layout['procedure_status']['performances'].update(
            Panel(
                performance_table,
                title='Performances'
            )
        )

        procedure_logs = self.procedure.logs

        console_logs = Text()
        for log in procedure_logs:
            time = log['time']
            if '.' in time:
                time = time[:time.index('.') + 4]

            console_logs.append(f'{time} ', style='dim')

            level = log['level']
            if len(level) < len('CRITICAL'):
                level += ' ' * (len('CRITICAL') - len(level))

            console_logs.append(f' {level} | ', style='bold')
            console_logs.append(log['message'])
            console_logs.append('\n')


        layout['main']['console'].update(
            Panel(
                console_logs,
                title='Console'
            )
        )

        return layout