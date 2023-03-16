import unittest

from ambrogio.procedures.param import ProcedureParam
from ambrogio.procedures.basic import BasicProcedure
from ambrogio.utils.project import create_procedure

from . import AmbrogioTestCase


class TestProcedureParams(AmbrogioTestCase):
    """
    Test procedure parameters.
    """
        
    def test_procedure_params(self):
        """
        Test procedure parameters.
        """

        name = 'Test params procedure'
        
        create_procedure(
            name,
            'basic',
            self.project_path
        )

        self.procedure_loader._load_all_procedures()

        procedure: BasicProcedure = self.procedure_loader.load(name)
        
        procedure.params = [
            ProcedureParam('strParam', str, value = 'test'),
            ProcedureParam('intParam', int, value = 1),
            ProcedureParam('floatParam', float, value = 1.0),
            ProcedureParam('boolParam', bool, value = True),
            ProcedureParam('listParam', list, value = [1, 2, 3]),
            ProcedureParam('dictParam', dict, value = {'a': 1, 'b': 2}),
            ProcedureParam('tupleParam', tuple, value = (1, 2, 3)),
            ProcedureParam('setParam', set, value = {1, 2, 3}),

            ProcedureParam('required', str, value = 'test', required = True),
            ProcedureParam('missing_required', str, required = True),

            ProcedureParam('doubleParam', str, value = 'test'),
            ProcedureParam('doubleParam', str, value = 'test')
        ]

        try:
            procedure(self.config)

        except Exception as e:
            self.assertEqual(
                e.args[0],
                'Parameter missing_required is required but has not been set'
            )

            procedure.params = [
                param for param in procedure.params
                if param.name != 'missing_required'
            ]

        try:
            procedure(self.config)

        except Exception as e:
            self.assertEqual(
                e.args[0],
                'Parameter doubleParam is defined more than once'
            )

            procedure.params = [
                param for param in procedure.params
                if param.name != 'doubleParam'
            ]

if __name__ == '__main__':
    unittest.main()