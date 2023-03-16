import unittest

from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestBasicProcedure(AmbrogioTestCase):
    """
    Test the basic procedure.
    """

    def test_basic_procedure(self):
        """
        Test the basic procedure.
        """

        name = 'Test basic procedure'
        
        create_procedure(
            name,
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        self.procedure_loader.run(name, False)


if __name__ == '__main__':
    unittest.main()