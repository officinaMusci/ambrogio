import unittest

from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestStepProcedure(AmbrogioTestCase):
    def test_step_procedure(self):
        create_procedure(
            'Step procedure',
            'step',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        self.procedure_loader.run('Step procedure')


if __name__ == '__main__':
    unittest.main()