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