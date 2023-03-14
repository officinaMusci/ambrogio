from typing import List, Optional, Callable, Any
from threading import Thread
import logging

from rich.panel import Panel
from rich.table import Column
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn

from ambrogio.procedures import Procedure
from ambrogio.utils.threading import exit_event


class StepProcedure(Procedure):
    """
    Class for Ambrogio step procedures.
    """

    _steps: List[dict] = []
    _parallel_steps: List[Thread] = []
    _current_step: int = 0
    _completed_steps: int = 0
    _failed_steps: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def current_step(self) -> Optional[dict]:
        """
        The current step.
        """

        return (self._steps[self._current_step - 1]
            if self._current_step
            else None
        )

    @property
    def current_step_name(self) -> Optional[str]:
        """
        The name of the current step.
        """

        return self.current_step['name'] if self.current_step else None

    @property
    def total_steps(self) -> int:
        """
        The total number of steps.

        :return: The total number of steps.
        """

        return len(self._steps)

    @property
    def completed_steps(self) -> int:
        """
        The number of completed steps.

        :return: The number of completed steps.
        """

        return self._completed_steps

    @property
    def failed_steps(self) -> int:
        """
        The number of failed steps.

        :return: The number of failed steps.
        """

        return self._failed_steps

    @property
    def _dashboard_widgets(self) -> List[Panel]:
        """
        Additional widgets to be added to Ambrogio dashboard.

        :return: A list of Rich panels.
        """

        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            expand=True,
            auto_refresh=False
        )
        
        progress.add_task(
            'Steps',
            total=self.total_steps,
            completed=self.completed_steps,
            finished_style='green'
        )
        
        return [Panel(progress, title='Progress')]

    def _execute(self) -> Any:
        """
        Execute the procedure.
        """

        logging.info(f'Executing "{self.name}" procedure...')

        self.setUp()

        if not self.total_steps:
            raise ValueError('No steps added to the procedure')

        for step in self._steps:
            self._current_step += 1

            if step['parallel']:
                parallel_step = Thread(
                    target=self._execute_step,
                    args=(step,)
                )
                
                logging.debug(f'Starting parallel step "{step["name"]}"...')
                parallel_step.start()
                self._parallel_steps.append(parallel_step)

            else:
                self._join_parallel_steps()

                logging.debug(f'Executing step "{step["name"]}"...')
                self._execute_step(step)

            if exit_event.is_set():
                break

        self._join_parallel_steps()
        
        self._finished = True

        self.tearDown()

        logging.info(f'Procedure "{self.name}" executed successfully')

    def setUp(self):
        """
        Method called before the execution of the procedure.
        Procedure steps can be added here.
        """

        pass

    def tearDown(self):
        """
        Method called after the execution of the procedure.
        """

        pass

    def add_step(
        self,
        function: Callable,
        name: Optional[str] = None,
        parallel: bool = False,
        blocking: bool = True,
        *args,
        **kwargs
    ):
        """
        Add a step to the procedure.

        :param function: The function to be executed.
        :param name: The name of the step.
        :param parallel: If the step can be executed in a separate thread.
        :param blocking: If the step can block the execution of the procedure.
        :param args: The arguments to pass to the function.
        :param kwargs: The keyword arguments to pass to the function.

        :raises ValueError: If the function is not callable.
        """

        logging.debug(f'Adding step "{name}" to procedure "{self.name}"')

        if name is None:
            name = function.__name__

        self._steps.append({
            'function': function,
            'name': name,
            'parallel': parallel,
            'blocking': blocking,
            'args': args,
            'kwargs': kwargs
        })

    def _execute_step(self, step: dict):
        """
        Execute a step.

        If the step is blocking and it raises an exception the procedure
        execution will be stopped and the exit event will be set.

        :param step: The step to execute.

        :raises Exception: If the step raises an exception.
        """

        try:
            step['function'](*step['args'], **step['kwargs'])
            self._completed_steps += 1

        except Exception as e:
            logging.error(f'Step "{step["name"]}" raised an exception: {e}')
            self._failed_steps += 1

            if step['blocking']:
                logging.error('Stopping procedure execution')
                exit_event.set()
                raise e

    def _join_parallel_steps(self):
        """
        Join the parallel steps.
        """

        logging.debug('Joining parallel steps...')

        for step in self._parallel_steps:
            if step.is_alive():
                step.join()