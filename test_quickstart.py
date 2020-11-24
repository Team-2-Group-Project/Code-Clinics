import unittest
import quickstart
from unittest.mock import patch
import io
import sys

class Test_Quickstart(unittest.TestCase):


    @patch('sys.stdin',io.StringIO('John'))
    def test_user_name(self):
        text = io.StringIO()
        sys.stdout = text
        result1 = quickstart.user_name()
        self.assertEqual(result1,'John')

    @patch('sys.stdin',io.StringIO('C'))
    def test_which_role(self):
        text = io.StringIO()
        sys.stdout = text
        result1 = quickstart.which_role('John')
        self.assertEqual(result1,'c')

    def test_valid_command(self):
        result1 = quickstart.valid_command('create')
        result2 = quickstart.valid_command('createrds')
        self.assertEqual(result1,True)
        self.assertEqual(result2,False)


if __name__ == '__main__':
    unittest.main()
