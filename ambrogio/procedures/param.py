from dataclasses import dataclass
from typing import TypeVar, Union, Optional, Any
from pathlib import Path

from ambrogio.cli.prompt import Prompt


types = (bool, int, float, str, Path)
ProcedureParamType = TypeVar('ProcedureParamType', *types)


@dataclass
class ProcedureParam:
    """
    A procedure parameter.
    """

    name: str
    type: ProcedureParamType
    value: Optional[ProcedureParamType] = None
    required: bool = True

    def __post_init__(self):
        if self.type not in types:
            raise TypeError(
                f"Parameter {self.name} must be of type {', '.join(types)}"
            )

        if self.value != None and not self._check_type(self.value, self.type):
            raise TypeError(
                f"Parameter {self.name} must be of type {self.type.__name__}"
            )

    def from_prompt(self):
        """
        Prompt the user to enter a value for this parameter.
        """
        
        if self.type == bool:
            self.value = Prompt.confirm(
                f"Set {self.name} to True?",
                default = self.value
            )

        elif self.type == Path:
            self.value = Prompt.path(
                f"Enter a path for {self.name}",
                default = self.value
            )

        else:
            value = Prompt.text(
                f"Enter value for {self.name} ({self.type.__name__})",
                default = self.value,
                validate = lambda _, x: self._check_type(x, self.type)
            )

            self.value = self.type(value)
            
    def _check_type(
        self,
        value: Any,
        type_: Optional[ProcedureParamType] = None
    ) -> bool:
        """
        Check whether the given value is of the correct type.
        """

        type_ = type_ or self.type

        return type_ in (bool, int, float, str, Path) and isinstance(value, type_)

    def __repr__(self):
        return f"<ProcedureParam {self.name} ({self.type.__name__})>"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return (
            self.name == other.name
            and self.type == other.type
            and self.value == other.value
        )

    def __hash__(self):
        return hash((self.name, self.type, self.value))
    
    def __call__(self, value: Any):
        if not isinstance(value, self.type):
            raise TypeError(
                f"Parameter {self.name} must be of type {self.type.__name__}"
            )
        
        return value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        return instance.__dict__.get(self.name, self.value)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = self(value)
