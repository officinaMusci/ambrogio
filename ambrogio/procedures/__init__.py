class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

    def __init__(self):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
    
    def _execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}._execute callback is not defined'
        )