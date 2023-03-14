import unittest

from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestStepProcedure(AmbrogioTestCase):
    """
    Test the step procedure.
    """

    counters = {
        'normals': 0,
        'parallels': 0,
        'errors': 0
    }

    def increment_normals(self):
        self.counters['normals'] += 1

    def increment_parallels(self):
        self.counters['parallels'] += 1

    def raise_error(self):
        self.counters['errors'] += 1
        raise Exception('Test error')

    def check_normals(self, count):
        self.assertEqual(self.counters['normals'], count)

    def check_parallels(self, count):
        self.assertEqual(self.counters['parallels'], count)

    def check_errors(self, count):
        self.assertEqual(self.counters['errors'], count)

    def test_step_procedure(self):
        """
        Test the step procedure.
        """

        name = 'Step procedure'
        
        create_procedure(
            name,
            'step',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        procedure = self.procedure_loader.load(name)()
        
        procedure.add_step(self.increment_normals)
        procedure.add_step(self.check_normals, count = 1)

        procedure.add_step(self.raise_error, blocking = False)
        procedure.add_step(self.check_errors, count = 1)
        
        procedure.add_step(self.increment_parallels, parallel = True)
        procedure.add_step(self.increment_parallels, parallel = True)
        procedure.add_step(self.increment_parallels, parallel = True)
        procedure.add_step(self.check_parallels, count = 3)

        procedure.add_step(self.increment_normals)
        procedure.add_step(self.check_normals, count = 2)

        procedure.add_step(self.raise_error, blocking = True)

        try:
            procedure._execute()
            raise Exception('Procedure did not raise an error')
        
        except Exception as e:
            if str(e) == 'Test error':
                self.check_normals(2)
                self.check_parallels(3)
                self.check_errors(2)

                self.assertEqual(procedure.completed_steps, 9) # Includes checks
                self.assertEqual(procedure.failed_steps, 2)

            else:
                raise e


if __name__ == '__main__':
    unittest.main()