from typing import Optional, List
from configparser import ConfigParser
import logging

from rich.panel import Panel

from ambrogio.environment import get_closest_ini
from ambrogio.procedures.param import ProcedureParam
from ambrogio.cli.prompt import Prompt


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str
    params: List[ProcedureParam] = []

    config: Optional[ConfigParser] = None

    logger: logging.Logger
    prompt: Prompt = Prompt()

    _finished: bool = False

    def __init__(self, config: Optional[ConfigParser] = None):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        
        self.logger = logging.getLogger(self.name)
        
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
    def _check_params(cls, raise_error: bool = True) -> bool:
        """
        Check if all parameters are valid.
        """

        for param in cls.params:
            name = param.name
            type_name = param.type.__name__

            # Check if the parameter is required but has not been set
            if param.required and param.value is None:
                if raise_error:
                    raise ValueError(
                        f"Parameter {name} is required but has not been set"
                    )
                
                return False
            
            # Check if the parameter has a value but is not of the correct type
            if param.value and not param._check_type(param.value):
                if raise_error:
                    raise TypeError(
                        f"Parameter {name} must be of type {type_name}"
                    )
                
                return False
            
            # Check if the parameter has been defined more than once
            for other_param in cls.params:
                if other_param is param:
                    continue
                
                if other_param.name == name:
                    if raise_error:
                        raise ValueError(
                            f"Parameter {name} is defined more than once"
                        )
                    
                    return False
        
        return True