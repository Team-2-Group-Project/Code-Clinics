import unittest
from unittest.mock import patch
import io, os
import sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS + "/")
import clinician.insert as insert


class Test_Insert(unittest.TestCase):

    text = io.StringIO()
    sys.stdout = text

    def test_valid_date(self):
        result1 = insert.valid_date('2020-11-20')
        result2 = insert.valid_date('2002020-123-200')
        self.assertEqual(result1,True)
        self.assertEqual(result2,False)

    def test_valid_time(self):
        result1 = insert.valid_time('12:05')
        result2 = insert.valid_time('132:102')
        self.assertEqual(result1,True)
        self.assertEqual(result2,False)

    def test_validate_params(self):
        result1 = insert.validate_params([])
        result2 = insert.validate_params(['','',''])
        result3 = insert.validate_params(['2020-13-20','14:30'])
        self.assertEqual(result1,('',''))
        self.assertEqual(result2,('',''))
        self.assertEqual(result3,('2020-13-20','14:30'))

    
    def test_meetings_setups(self):
        result1 = insert.meeting_setups([],'John')
        result2 = insert.meeting_setups(['TR5','Help'],'John')
        self.assertEqual(result1,('John','Open for anything'))
        self.assertEqual(result2,('TR5','Help'))


if __name__ == '__main__':
    unittest.main()
    
