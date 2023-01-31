from ambrogio.procedures import Procedure


class BasicProcedure(Procedure):
    """
    Class for Ambrogio basic procedures.
    """

    def __init__(self):
        super().__init__()

    def _execute(self):
        """
        Run the Process main thread
        """

        return self.execute()

    def execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}.execute callback is not defined'
        )