import unittest

from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestProcedure(AmbrogioTestCase):
    
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

    def test_basic(self):
        create_procedure(
            'Basic procedure',
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        self.procedure_loader.run('Basic procedure')

    def test_step(self):
        create_procedure(
            'Step procedure',
            'step',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        self.procedure_loader.run('Step procedure')


if __name__ == '__main__':
    unittest.main()