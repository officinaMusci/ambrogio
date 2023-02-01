import unittest

from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestBasicProcedure(AmbrogioTestCase):
    def test_basic_procedure(self):
        create_procedure(
            'Basic procedure',
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        self.procedure_loader.run('Basic procedure')


if __name__ == '__main__':
    unittest.main()