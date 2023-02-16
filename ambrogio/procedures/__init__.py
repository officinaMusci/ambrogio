import os
from typing import Optional, List, Union
from pathlib import Path
from datetime import datetime

from rich.layout import Layout


class Procedure:
    """
    Base class for Ambrogio procedures.
    All procedures must inherit from this class.
    """

    name: str

    _project_path: Path

    _logs: List[dict] = []
    _log_dir: Path
    _log_file: Path

    _finished: bool = False

    def __init__(self, project_path: Union[str, os.PathLike] = '.'):
        if not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")

        self._project_path = Path(project_path)

        self._log_dir = self._get_log_dir()
        self._log_dir.mkdir(parents=True, exist_ok=True)
        
        self._log_file = self._get_log_file()
        self._log_file.touch(exist_ok=True)

    @property
    def project_path(self) -> Path:
        """
        The project path.
        """

        return self._project_path

    @property
    def logs(self) -> List[dict]:
        """
        The procedure logs.
        """

        return self._logs

    @property
    def finished(self) -> bool:
        """
        Whether the procedure has finished.
        """

        return self._finished
    
    def _execute(self):
        raise NotImplementedError(
            f'{self.__class__.__name__}._execute callback is not defined'
        )

    @property
    def _additional_layouts(self) -> List[Layout]:
        """
        Additional layouts to be added to Ambrogio dashboard.

        :return: A list of layouts.
        """
        
        return []

    def _get_log_dir(self) -> Path:
        """
        Get the directory where the procedure log file will be stored.

        :return: The log directory.
        """
        
        return self._project_path / 'logs'

    def _get_log_file(self) -> Path:
        """
        Get the procedure log file.

        :return: The log file.
        """

        snake_case_name = '_'.join(
            s.lower() for s in self.name.split(' ')
        )
        
        return self._log_dir / f'{snake_case_name}.log'

    def log(self, message: str, level: str = 'INFO'):
        """
        Store a message in the procedure log list and write it to the log file.

        :param message: The message to log.
        :param level: The log level.
        """
        
        time = datetime.now()
        
        self._logs.append({
            'time': time,
            'message': message,
            'level': level
        })
        
        # Write the log to the log file in a new line
        with open(self._log_file, 'a') as log_file:
            log_file.write(f'{time} [{level}] {message}\n')