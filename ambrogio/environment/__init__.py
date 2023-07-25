import os
import sys
from typing import Union, Optional
from pathlib import Path
from configparser import ConfigParser
import logging


config_base = {
    'settings': {
        'procedure_module': 'procedures',
        'log_level': 'NOTSET'
    }
}


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

    :param path: The path to start searching from.
    :param prev_path: The previous path to avoid infinite recursion.

    :return: The path to the closest ambrogio.ini file.

    :raises MissingConfigFileError: If no ambrogio.ini file is found.
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

    :return: The Ambrogio project configuration.

    :raises MissingConfigFileError: If no ambrogio.ini file is found.
    """

    ini_path = get_closest_ini()

    if ini_path:
        config = ConfigParser()
        config.read(ini_path)

        if config:
            # If the config has missing sections or options, fill them with
            # the default values
            for section in config_base:
                if section not in config:
                    logging.warning(
                        f"Section {section} not found in {ini_path}."
                        ' Using default values.'
                    )
                    config[section] = {}
                
                for option in config_base[section]:
                    if option not in config[section]:
                        logging.warning(
                            f"Option {option} not found in {ini_path}."
                            ' Using default value.'
                        )
                        config[section][option] = config_base[section][option]

            # Add the project path to the Python path
            project_path = str(Path(ini_path).parent)
            if project_path not in sys.path:
                sys.path.append(project_path)

            return config
    
    raise MissingConfigFileError