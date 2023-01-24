import os
from typing import Union
from pathlib import Path
import configparser
import string

from ambrogio import procedures


def create_project(project_name: str, project_path: Union[str, os.PathLike] = '.'):
    """
    Create an Ambrogio project.
    """

    project_path: Path = Path(project_path) / project_name
    project_path.mkdir()

    config = configparser.ConfigParser()
    config['settings'] = {
        'procedure_module': 'procedures'
    }

    config_path: Path = project_path / 'ambrogio.ini'

    with open(config_path.resolve(), 'x') as config_file:
        config.write(config_file)
        config_file.close()
    
    procedure_path: Path = project_path / 'procedures'
    procedure_path.mkdir()

    procedure_init_path: Path = procedure_path / '__init__.py'

    with open(procedure_init_path.resolve(), 'x') as init_file:
        init_file.write(
            '# This package will contain the procedures of your Ambrogio project'
            '#'
            '# Please refer to the documentation for information on how to create and'
            '# manage your procedures.'
        )


def create_procedure(
        procedure_name: str,
        template_name:str = 'basic',
        project_path: Union[str, os.PathLike] = '.',
        procedure_module:str = 'procedures'
    ):
    """
    Create an Ambrogio procedure using a given template.
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