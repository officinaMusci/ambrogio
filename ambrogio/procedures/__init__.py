from typing import Optional, List, Any
from configparser import ConfigParser

from rich.panel import Panel

from ambrogio.environment import get_closest_ini
from ambrogio.procedures.param import ProcedureParam


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str
    params: List[ProcedureParam] = []

    config: Optional[ConfigParser] = None

    _finished: bool = False

    def __init__(self, config: Optional[ConfigParser] = None):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        
        self._check_params()
        
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
    
    @classmethod
    def get_param(cls, name: str) -> Optional[ProcedureParam]:
        """
        Get a parameter by name.
        """

        for param in cls.params:
            if param.name == name:
                return param
        
        return None
    
    @classmethod
    def _prompt_params(cls):
        """
        Prompt the user to enter values for all parameters.
        """

        for param in cls.params:
            param.from_prompt()

    @classmethod
    def _check_params(cls):
        """
        Check whether all parameters have been set.
        """

        for param in cls.params:
            if param.required and param.value is None:
                raise ValueError(
                    f"Parameter {param.name} is required but has not been set"
                )
            
            if param.value and not param._check_type(param.value):
                raise TypeError(
                    f"Parameter {param.name} must be of type {param.type.__name__}"
                )
            
        param_names = [param.name for param in cls.params]

        if len(param_names) != len(set(param_names)):
            raise ValueError(
                    f"Parameter {param.name} is defined more than once"
            )