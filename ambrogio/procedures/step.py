from typing import List, Optional, Callable, Any
from threading import Thread
import logging

from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn

from ambrogio.procedures import Procedure
from ambrogio.utils.threading import exit_event, wait_resume


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
            TextColumn('[progress.description]{task.description}'),
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

        self.logger.info(f"Executing '{self.name}' procedure...")

        self.set_up()

        if not self.total_steps:
            raise ValueError('No steps added to the procedure')

        for step in self._steps:
            self._current_step += 1

            if step['parallel']:
                parallel_step = Thread(
                    target=self._execute_step,
                    args=(step,)
                )
                
                self.logger.debug(f"Starting parallel step '{step['name']}'...")
                parallel_step.start()
                self._parallel_steps.append(parallel_step)

            else:
                self._join_parallel_steps()

                wait_resume()
                if not exit_event.is_set():
                    self._execute_step(step)

        wait_resume()
        if not exit_event.is_set():
            self._join_parallel_steps()
        
            self._finished = True

            self.tear_down()

            self.logger.info(f"Procedure '{self.name}' executed successfully")

    def set_up(self):
        """
        Method called before the execution of the procedure.
        Procedure steps can be added here.
        """

        pass

    def tear_down(self):
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
        add_after: Optional[str] = None,
        params: Optional[dict] = None,
    ):
        """
        Add a step to the procedure.

        :param function: The function to be executed.
        :param name: The name of the step.
        :param parallel: If the step can be executed in a separate thread.
        :param blocking: If the step can block the execution of the procedure.
        :param add_after: The name of the step after which the step will be added.
        :param params: The parameters to be passed to the function.

        :raises ValueError: If the function is not callable.
        """

        if name is None:
            name = function.__name__

        self.logger.debug(f"Adding step '{name}' to procedure '{self.name}'")

        step = {
            'function': function,
            'name': name,
            'parallel': parallel,
            'blocking': blocking,
            'params': params or {}
        }

        if add_after:
            has_been_added = False
            for i, step in enumerate(self._steps):
                if step['name'] == add_after:
                    self._steps.insert(i + 1, step)
                    has_been_added = True
                    break
            
            if not has_been_added:
                raise ValueError(f"Step '{add_after}' not found")

        else:
            self._steps.append(step)

    def _execute_step(self, step: dict):
        """
        Execute a step.

        If the step is blocking and it raises an exception the procedure
        execution will be stopped and the exit event will be set.

        :param step: The step to execute.

        :raises Exception: If the step raises an exception.
        """

        self.logger.debug(f"Executing step '{step['name']}'...")

        try:
            step['function'](**step['params'])
            self._completed_steps += 1

            self.logger.debug(f"Step '{step['name']}' executed successfully")

        except Exception as e:
            self.logger.error(f"Step '{step['name']}' raised an exception: {e}")
            self._failed_steps += 1

            if step['blocking']:
                self.logger.error('Stopping procedure execution')
                exit_event.set()
                raise e

    def _join_parallel_steps(self):
        """
        Join the parallel steps.
        """

        self.logger.debug('Joining parallel steps...')

        for step in self._parallel_steps:
            if step.is_alive():
                step.join()