import os
import logging
from threading import Thread 
from time import sleep
from datetime import datetime
import psutil

from rich.logging import RichHandler
import plotly.graph_objects as go


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

    def __init__(self, logging_level:str = 'DEBUG'):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")

        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(RichHandler(rich_tracebacks=True))
        self.logger.setLevel(logging_level)

        self._stats = {
            'cpu': [],
            'memory': []
        }

    def _monitor(self, main_thread:Thread):
        """
        Keep track of the Process main thread performances
        """

        process = psutil.Process(os.getpid())

        while process.is_running() and main_thread.is_alive():
            with process.oneshot():
                now = datetime.now()

                cpu_percent = (now, process.cpu_percent())
                memory_percent = (now, process.memory_percent())

                self._stats['cpu'].append(cpu_percent)
                self._stats['memory'].append(memory_percent)

            sleep(.1)

        fig = go.Figure(
            data=[
                go.Scatter(
                    name=name,
                    x=[d[0] for d in dataset],
                    y=[d[1] for d in dataset],
                    mode='lines'
                )
                for name, dataset in self._stats.items()
            ],
            layout_title_text=f"\"{self.name}\" procedure performances"
        )
        fig.show()

    def _execute(self):
        """
        Run the Process main thread
        """

        execute_thread = Thread(target=self.execute)
        monitor_thread = Thread(target=self._monitor, args=(execute_thread,))

        execute_thread.start()
        monitor_thread.start()

        execute_thread.join()

    def execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}.execute callback is not defined'
        )