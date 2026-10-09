import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('launcher',Path(__file__).parents[1]/'launcher.py')
launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
class RegistryTests(unittest.TestCase):
    def check(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'cybOS').mkdir();(root/'cybOS/ecosystem.json').write_text(json.dumps({'repositories':rows}))
            return launcher.load_registry(root)
    def test_duplicate_and_traversal_are_rejected(self):
        for rows in [[{'name':'../escape'}],[{'name':'same'},{'name':'same'}]]:
            with self.assertRaises(ValueError):self.check(rows)
    def test_commands_are_argument_lists(self):
        with self.assertRaises(ValueError):self.check([{'name':'demo','test_command':'echo shell'}])
        self.assertEqual(len(self.check([{'name':'demo','test_command':['cargo','test']} ])),1)
if __name__=='__main__':unittest.main()
