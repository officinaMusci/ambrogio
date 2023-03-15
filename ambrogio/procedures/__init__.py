from typing import List
from pathlib import Path

from rich.panel import Panel


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

    _logs: List[dict] = []
    _log_dir: Path
    _log_file: Path

    _finished: bool = False

    def __init__(self):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")

    @property
    def finished(self) -> bool:
        """
        Whether the procedure has finished.
        """

        return self._finished

    @property
    def _dashboard_widgets(self) -> List[Panel]:
        """
        Additional widgets to be added to Ambrogio dashboard.

        :return: A list of Rich panels.
        """
        
        return []
    
    def _execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}._execute callback is not defined'
        )