from ambrogio.procedures.loader import ProcedureLoader
from ambrogio.utils.project import create_procedure
from . import AmbrogioTestCase


class TestCreateProcedure(AmbrogioTestCase):
    
    def test_create(self):
        procedure_loader = ProcedureLoader(self.config)

        procedures = procedure_loader.list()
        self.assertEqual(len(procedures), 0)

        create_procedure(
            'Test procedure',
            'basic',
            self.project_path
        )

        procedure_loader._load_all_procedures()

        procedures = procedure_loader.list()
        self.assertEqual(len(procedures), 1)

        self.assertRaises(FileExistsError, lambda: create_procedure(
            'Test procedure',
            'basic',
            self.project_path
        ))

        create_procedure(
            'Test procedure 2',
            'basic',
            self.project_path
        )

        procedure_loader._load_all_procedures()

        procedures = procedure_loader.list()
        self.assertEqual(len(procedures), 2)