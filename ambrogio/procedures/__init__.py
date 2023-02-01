from typing import Optional, List

from rich.layout import Layout


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

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
    
    def _execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}._execute callback is not defined'
        )

    @property
    def _additional_layouts(self) -> List[Layout]:
        """
        Additional layouts to be added to Ambrogio dashboard.
        """
        
        return []