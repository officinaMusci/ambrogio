import unittest
import os
from typing import Optional
from tempfile import TemporaryDirectory
from pathlib import Path

from ambrogio.utils.project import create_project
from ambrogio.environment import init_env


def create_test_project(
        project_name: str = 'test_project',
        test_path: Optional[Path] = None
    ):
    prev_cwd = os.getcwd()

    test_directory = None
    if not test_path:
        test_directory = TemporaryDirectory()
        test_path = Path(test_directory.name)
        os.chdir(test_path.resolve())

    create_project(project_name, test_path)
    
    project_path: Path = test_path / project_name
    os.chdir(project_path.resolve())

    config = init_env()
    
    os.chdir(prev_cwd)

    return test_directory, project_path, config


class AmbrogioTestCase(unittest.TestCase):
  """
  Ambrogio specific test case. It creates an Ambrogio project
  in a temporary directory and activates it.
  """

  def setUp(self):
      (
          self.test_directory,
          self.project_path,
          self.config
      ) = create_test_project()
  
  def tearDown(self):
      self.test_directory.cleanup()