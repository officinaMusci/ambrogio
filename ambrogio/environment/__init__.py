import os
import sys
from typing import Union, Optional
from pathlib import Path
import configparser


class MissingIniFile(IOError):
    'Missing file called ambrogio.ini'
    pass


def closest_ini(
        path: Union[str, os.PathLike] = '.',
        prev_path: Optional[Union[str, os.PathLike]] = None
    ) -> str:
    """
    Return the path to the closest ambrogio.ini file by traversing the current
    directory and its parents
    """
    
    if prev_path is not None and str(path) == str(prev_path):
        return ''
    
    path = Path(path).resolve()
    ini_path = path / 'ambrogio.ini'

    if ini_path.exists():
        return str(ini_path)
    
    return closest_ini(path.parent, path)


def init_env() -> dict:
    """
    Initialize environment to use command-line tool from inside a project
    dir. This returns the Ambrogio project configuration and modifies the
    Python path to be able to locate the project module.
    """

    config = configparser.ConfigParser()
    ini_path = closest_ini()
    
    if ini_path:
        config.read(ini_path)
        
        project_dir = str(Path(ini_path).parent)

        if project_dir not in sys.path:
            sys.path.append(project_dir)

        return config
    
    raise MissingIniFile