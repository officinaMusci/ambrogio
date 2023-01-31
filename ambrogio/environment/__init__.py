import os
import sys
from typing import Union, Optional
from pathlib import Path
from configparser import ConfigParser


class MissingConfigFileError(FileNotFoundError):
    'Missing file called ambrogio.ini'
    pass


class NestedProjectError(Exception):
    'Can\'t create an Ambrogio project inside another one'
    pass


def get_closest_ini(
        path: Union[str, os.PathLike] = '.',
        prev_path: Optional[Union[str, os.PathLike]] = None
    ) -> str:
    """
    Return the path to the closest ambrogio.ini file by traversing the current
    directory and its parents.
    """
    
    if prev_path is not None and str(path) == str(prev_path):
        return ''
    
    path = Path(path).resolve()
    ini_path = path / 'ambrogio.ini'

    if ini_path.exists():
        return str(ini_path)
    
    return get_closest_ini(path.parent, path)


def init_env() -> ConfigParser:
    """
    Initialize environment to use command-line tool from inside a project
    dir. This returns the Ambrogio project configuration and modifies the
    Python path to be able to locate the project module.
    """

    ini_path = get_closest_ini()

    if ini_path:
        config = ConfigParser()
        config.read(ini_path)

        if config:
            project_path = str(Path(ini_path).parent)

            if project_path not in sys.path:
                sys.path.append(project_path)

            return config
    
    raise MissingConfigFileError