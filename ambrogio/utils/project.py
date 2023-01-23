from pathlib import Path
import configparser


def create_project(project_name: str, project_path: str = './'):
    """
    Create an Ambrogio project.
    """

    project_path = Path(project_path) / project_name
    project_path.mkdir()
    
    procedure_path = project_path / 'procedures'
    procedure_path.mkdir()

    config = configparser.ConfigParser()
    config['settings'] = {
        'procedure_module': 'procedures',
        'logging_level': 'INFO'
    }

    config_path = project_path / 'ambrogio.ini'

    with open(config_path.resolve(), 'x') as configfile:
        config.write(configfile)