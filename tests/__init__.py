import unittest
import os
import tempfile
from pathlib import Path

from ambrogio.utils.project import create_project
from ambrogio.environment import init_env


class AmbrogioTestCase(unittest.TestCase):
  """
  Ambrogio specific test case. It creates an Ambrogio project
  in a temporary directory and activates it.
  """

  def setUp(self):
      prev_cwd = os.getcwd()

      self.project_directory = tempfile.TemporaryDirectory()
      create_project('test_project', self.project_directory.name)
      
      project_path = Path(self.project_directory.name) / 'test_project'
      os.chdir(project_path.resolve())

      self.config = init_env()
      
      os.chdir(prev_cwd)
  
  def tearDown(self):
     self.project_directory.cleanup()