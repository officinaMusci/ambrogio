import os
from threading import Thread 
from time import sleep
from datetime import datetime
import psutil

import plotly.graph_objects as go

from ambrogio.procedures import Procedure


class BasicProcedure(Procedure):
    """
    Class for Ambrogio basic procedures.
    """

    def __init__(self):
        super().__init__()

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