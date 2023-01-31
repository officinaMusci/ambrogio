import inspect
from importlib import import_module
from pkgutil import iter_modules
from multiprocessing import Process

from ambrogio.procedures import Procedure


def walk_modules(path):
    """
    Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)

    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath

            if ispkg:
                mods += walk_modules(fullpath)

            else:
                submod = import_module(fullpath)
                mods.append(submod)
    
    return mods


class ProcedureLoader:
    """
    ProcedureLoader is a class which locates, loads and 
    runs procedures in a Ambrogio project.
    """

    def __init__(self, config: dict):
        self.config = config
        self._procedures = {}
        self._load_all_procedures()

    def _load_procedures(self, module: str):
        for procedure in self.iter_procedure_classes(module):
            self._procedures[procedure.name] = procedure

    def _load_all_procedures(self):
        try:
            for module in walk_modules(self.config['settings']['procedure_module']):
                self._load_procedures(module)
        
        except ImportError:
            raise
    
    def list(self):
        """
        Return a list with the names of all procedures available in the project.
        """

        return list(self._procedures.keys())

    def load(self, procedure_name: str) -> Procedure:
        """
        Return the Procedure class for the given procedure name.
        If the procedure name is not found, raise a KeyError.
        """

        try:
            return self._procedures[procedure_name]

        except KeyError:
            raise KeyError(f"Procedure not found: {procedure_name}")

    def run(self, procedure_name: str):
        """
        Run the Procedure execute method for the given procedure name.
        If the procedure name is not found, raise a KeyError.
        """

        procedure = self.load(procedure_name)
        procedure._execute()

    @staticmethod
    def iter_procedure_classes(module):
        """
        Return an iterator over all procedure classes defined in the given
        module that can be instantiated (i.e. which have name)
        """

        for obj in vars(module).values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, Procedure)
                and obj.__module__ == module.__name__
                and getattr(obj, 'name', None)
            ):
                yield obj