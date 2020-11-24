import unittest
import insert
from unittest.mock import patch
import io
import sys

class Test_Insert(unittest.TestCase):

    def test_valid_date(self):
        result1 = insert.valid_date('2020-11-20')
        result2 = insert.valid_date('2002020-123-200')
        self.assertEqual(result1,'2020-11-20')
        self.assertEqual(result2,'')

    def test_valid_time(self):
        result1 = insert.valid_time('12:05')
        result2 = insert.valid_time('132:102')
        self.assertEqual(result1,'12:05')
        self.assertEqual(result2,'')

    @patch('sys.stdin',io.StringIO('2020-11-207\n2020-15-36\n15:36\n2020-12-10\n25:26\n2020-12-10\n12:30'))
    def test_valid_date_checker(self):
        text = io.StringIO()
        sys.stdout = text
        result1 = insert.valid_date_checker()
        self.assertEqual(result1,('2020-12-10T12:30:00+02:00', '2020-12-10T13:00:00+02:00'))


if __name__ == '__main__':
    unittest.main()
