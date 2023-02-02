from typing import List, Any

from rich.layout import Layout

from ambrogio.procedures import Procedure


class BasicProcedure(Procedure):
    """
    Class for Ambrogio basic procedures.
    """

    def __init__(self):
        super().__init__()

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

    @property
    def _additional_layouts(self) -> List[Layout]:
        """
        Additional layouts to be added to Ambrogio dashboard.

        :return: A list of layouts.
        """

        return []