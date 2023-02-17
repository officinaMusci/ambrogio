from typing import List, Any

from rich.layout import Layout

from ambrogio.procedures import Procedure


class BasicProcedure(Procedure):
    """
    Class for Ambrogio basic procedures.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _execute(self) -> Any:
        """
        Execute the procedure.
        """

        result = self.execute()

        self._finished = True

        return result

    def execute(self) -> Any:
        """
        Execute the procedure.
        """
        
        raise NotImplementedError(
            f'{self.__class__.__name__}.execute callback is not defined'
        )