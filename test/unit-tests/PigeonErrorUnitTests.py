import unittest
import io
import sys
from ut_pigeon import PigeonError #Note - ut_pigeon is a copy of pigeon.py and is created by tests.ps1

'''
Tests the PigeonError class from pigeon.py
'''
class PigeonErrorTests(unittest.TestCase):

    def setUp(self):
        self.Capture = io.StringIO()
        sys.stdout = self.Capture

    def test_PigeonError_Exit_and_Message(self):
        error = PigeonError("TestError", 1, "Error")
        with self.assertRaises(SystemExit):
            error.ExitWithMessage()
        self.assertEqual("TestError: Error\n", self.Capture.getvalue())

    def tearDown(self):
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
