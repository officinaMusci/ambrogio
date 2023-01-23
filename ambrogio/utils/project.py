from pathlib import Path
import configparser


def create_project(project_name: str, project_path: str = './'):
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