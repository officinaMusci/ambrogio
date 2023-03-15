from typing import Optional, List
from pathlib import Path
from configparser import ConfigParser

from rich.panel import Panel

from ambrogio.environment import get_closest_ini


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

    config: Optional[ConfigParser] = None

    _finished: bool = False

    def __init__(self, config: Optional[ConfigParser] = None):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        
        if not config:
            ini_path = get_closest_ini()
            
            if ini_path:
                config = ConfigParser()
                config.read(ini_path)
        
        self.config = config

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