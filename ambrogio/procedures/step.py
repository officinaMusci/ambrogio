from typing import List, Optional, Callable, Any
from threading import Thread
from inspect import getsource

from rich.layout import Layout
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.syntax import Syntax

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

    def _execute(self) -> Any:
        """
        Execute the procedure.
        """

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
                
                parallel_step.start()
                self._parallel_steps.append(parallel_step)

            else:
                self._join_parallel_steps()
                self._execute_step(step)

            if exit_event.is_set():
                break

        self._join_parallel_steps()
        
        self._finished = True

        self.tearDown()

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
            if step['blocking']:
                exit_event.set()

            raise e

    def _join_parallel_steps(self):
        """
        Join the parallel steps.
        """

        for step in self._parallel_steps:
            if step.is_alive():
                step.join()

    @property
    def _additional_layouts(self) -> List[Layout]:
        """
        Additional layouts to be added to Ambrogio command-line interface
        dashboard.

        :return: A list of layouts.
        """

        progress = Layout(name='progress', size=3)
        current_step_function = Layout(name='current_step_function', ratio=1)

        progress.update(
            Panel(
                ProgressBar(
                    total=self.total_steps,
                    completed=self.completed_steps,
                    finished_style='green'
                ),
                title="Progress"
            )
        )

        current_step_function.update(
            Panel(
                Syntax(
                    getsource(self.current_step['function'])
                        if self.current_step
                        else '',
                    'python',
                    line_numbers=True
                ),
                title='Current step function'
            )
        )
        
        return [
            progress,
            current_step_function
        ]