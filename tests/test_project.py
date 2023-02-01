import unittest

from ambrogio.utils.project import create_procedure
from ambrogio.environment import NestedProjectError

from . import AmbrogioTestCase, create_test_project


class TestNestedProject(AmbrogioTestCase):
    def test_create_nested(self):
        self.assertRaises(
            NestedProjectError,
            lambda: create_test_project(
                'test_project',
                self.project_path
            )
        )

    def test_create(self):
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

        create_procedure(
            'Test procedure 2',
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        procedures = self.procedure_loader.list()
        self.assertEqual(len(procedures), 2)


if __name__ == '__main__':
    unittest.main()