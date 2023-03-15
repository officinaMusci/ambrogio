import os
from types import ModuleType
from typing import TypeVar, List, Type, Generator, Union
import inspect
from importlib import import_module
from pkgutil import iter_modules
from configparser import ConfigParser

from ambrogio.procedures import Procedure
from ambrogio.procedures.basic import BasicProcedure
from ambrogio.procedures.step import StepProcedure


ProcedureType = TypeVar('ProcedureType', BasicProcedure, StepProcedure)


def walk_modules(path: str) -> List[ModuleType]:
    """
    Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    :param path: The module path to load.

    :return: A list of modules.
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

    :param config: The project configuration.
    :param project_path: The path to the project.
    """

    def __init__(
        self,
        config: ConfigParser,
        project_path: Union[str, os.PathLike] = '.'
    ):
        self.config = config
        self._project_path = project_path

        self._procedures = {}
        self._load_all_procedures()

    def _load_procedures(self, module: ModuleType):
        """
        Load all procedures from the given module.

        :param module: The module to load procedures from.
        """

        for procedure in self.iter_procedure_classes(module):
            self._procedures[procedure.name] = procedure

    def _load_all_procedures(self):
        """
        Load all procedures from the project.

        :raises ImportError: If the procedure module cannot be imported.
        """
        
        try:
            modules = walk_modules(self.config['settings']['procedure_module'])
            
            for module in modules:
                self._load_procedures(module)
        
        except ImportError:
            raise
    
    def list(self) -> List[str]:
        """
        Return a list with the names of all procedures available in the project.

        :return: A list of procedure names.
        """

        return list(self._procedures.keys())

    def load(self, procedure_name: str) -> Type[ProcedureType]:
        """
        Return the Procedure class for the given procedure name.
        If the procedure name is not found, raise a KeyError.

        :param procedure_name: The name of the procedure to load.

        :raises KeyError: If the procedure name is not found.

        :return: The Procedure class.
        """

        try:
            return self._procedures[procedure_name]

        except KeyError:
            raise KeyError(f"Procedure not found: {procedure_name}")

    def run(self, procedure_name: str) -> ProcedureType:
        """
        Run the Procedure execute method for the given procedure name.
        If the procedure name is not found, raise a KeyError.

        :param procedure_name: The name of the procedure to run.

        :raises KeyError: If the procedure name is not found.

        :return: The Procedure instance.
        """

        procedure = self.load(procedure_name)()
        procedure._execute()

        return procedure

    @staticmethod
    def iter_procedure_classes(
        module: ModuleType
    ) -> Generator[Type[Procedure], None, None]:
        """
        Return an iterator over all procedure classes defined in the given
        module that can be instantiated (i.e. which have name)

        :param module: The module to iterate over.

        :raises TypeError: If the module is not a module.

        :return: An iterator over all procedure classes.
        """

        for obj in vars(module).values():
            if (
                inspect.isclass(obj)
                and issubclass(obj, Procedure)
                and obj.__module__ == module.__name__
                and getattr(obj, 'name', None)
            ):
                yield obj