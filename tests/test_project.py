import unittest

from ambrogio.utils.project import create_procedure
from ambrogio.environment import NestedProjectError

from . import AmbrogioTestCase, create_test_project


class TestProject(AmbrogioTestCase):
    """
    Test the project creation.
    """

    def test_nested_project(self):
        """
        Test the creation of a project inside another project.
        """

        self.assertRaises(
            NestedProjectError,
            lambda: create_test_project(
                'test_project',
                self.project_path
            )
        )

    def test_create_procedures(self):
        """
        Test the creation of procedures.
        """
        
        procedures = self.procedure_loader.list()
        self.assertEqual(len(procedures), 0)

        create_procedure(
            'Test procedure',
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        procedures = self.procedure_loader.list()
        self.assertEqual(len(procedures), 1)

        self.assertRaises(
            FileExistsError,
            lambda: create_procedure(
              'Test procedure',
              'basic',
              self.project_path
          )
        )


if __name__ == '__main__':
    unittest.main()