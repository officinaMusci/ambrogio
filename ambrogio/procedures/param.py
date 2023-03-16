from dataclasses import dataclass
from typing import Union, Optional, Any

from ambrogio.cli.prompt import Prompt


@dataclass
class ProcedureParam:
    """
    A procedure parameter.
    """

    name: str
    type: Union[bool, int, float, str]
    value: Optional[Any] = None
    required: bool = False

    def __post_init__(self):
        if self.type not in (bool, int, float, str):
            raise TypeError(
                f"Parameter {self.name} must be of type bool, int, float or str"
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
            self._value = Prompt.confirm(
                f"Enter value for {self.name}",
                default=self.value
            )

        else:
            while not value or not self._check_type(value):
                value = Prompt.text(
                    f"Enter value for {self.name}",
                    default=self.value
                )

            self.value = self.type(value)
            
    def _check_type(
        self,
        value: Any,
        type_: Optional[Union[bool, int, float, str]] = None
    ) -> bool:
        """
        Check whether the given value is of the correct type.
        """

        type_ = type_ or self.type

        return type_ in (bool, int, float, str) and isinstance(value, type_)

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
