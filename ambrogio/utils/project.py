import os
from typing import Union
from pathlib import Path
from configparser import ConfigParser
import string

from ambrogio import procedures
from ambrogio.environment import get_closest_ini, NestedProjectError


def create_project(
    project_name: str,
    dest_directory_path: Union[str, os.PathLike] = '.',
    procedure_module_name: str = 'procedures'
):
    """
    Create an Ambrogio project.

    :param project_name: The name of the project.
    :param dest_directory_path: The path to the directory where the project
    will be created.
    :param procedure_module_name: The name of the module where the procedures
    will be stored.

    :raises NestedProjectError: If the project is being created inside an
    existing Ambrogio project.
    """

    if get_closest_ini(dest_directory_path):
        raise NestedProjectError

    project_path: Path = Path(dest_directory_path) / project_name
    project_path.mkdir()

    config = ConfigParser()
    config['settings'] = {
        'procedure_module': procedure_module_name
    }

    config_path: Path = project_path / 'ambrogio.ini'

    with open(config_path.resolve(), 'x') as config_file:
        config.write(config_file)
        config_file.close()
    
    procedure_path: Path = project_path / procedure_module_name
    procedure_path.mkdir()

    procedure_init_path: Path = procedure_path / '__init__.py'

    with open(procedure_init_path.resolve(), 'x') as init_file:
        init_file.write(
            '# This package will contain the procedures of your Ambrogio project'
            '#'
            '# Please refer to the documentation for information on how to'
            '# create and manage your procedures.'
        )


def create_procedure(
    procedure_name: str,
    template_name:str = 'basic',
    project_path: Union[str, os.PathLike] = '.',
    procedure_module:str = 'procedures'
):
    """
    Create an Ambrogio procedure using a given template.

    :param procedure_name: The name of the procedure.
    :param template_name: The name of the template to use.
    :param project_path: The path to the project directory.
    :param procedure_module: The name of the module where the procedures
    will be stored.

    :raises FileExistsError: If the procedure already exists.
    """

    camel_case_name = ''.join(
        s.capitalize() for s in procedure_name.split(' ')
    )
    
    snake_case_name = '_'.join(
        s.lower() for s in procedure_name.split(' ')
    )
    
    templates_path: Path = Path(procedures.__file__).parent / 'templates'
    template_file_path: Path = templates_path / f'{template_name}.py.tmpl'

    new_procedure_path: Path = (
        Path(project_path)
        / procedure_module
        / f'{snake_case_name}.py'
    )

    if new_procedure_path.exists():
        raise FileExistsError
    
    text_vars = {
        'name': procedure_name,
        'classname': f'{camel_case_name}Procedure'
    }

    with open(template_file_path.resolve(), 'r') as template_file:
        procedure = template_file.read()
        procedure = string.Template(procedure).substitute(**text_vars)
        template_file.close()
    
        with open(new_procedure_path.resolve(), 'x') as procedure_file:
            procedure_file.write(procedure)
            procedure_file.close()