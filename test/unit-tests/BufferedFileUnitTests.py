import unittest
import os
from TestBuffer import TestBuffer
from ut_pigeon import BufferedFile, PigeonError #Note - ut_pigeon is a copy of pigeon.py and is created by tests.ps1

'''
Tests the BufferedFile class from pigeon.py
'''
class BufferedFileTests(unittest.TestCase):

    def test_BufferedFile_Constructor_Read(self):
        CreateTestFile("test1.test-output")
        buffer = BufferedFile("test1.test-output", False, 1000)
        self.assertEqual(buffer.Filename, "test1.test-output")
        self.assertEqual(buffer.EndOfFile, False)
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)

    def test_BufferedFile_Constructor_Write(self):
        buffer = BufferedFile("test2.test-output", True, 1000)
        self.assertEqual(buffer.Filename, "test2.test-output")
        self.assertEqual(buffer.EndOfFile, False)
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)

    def test_BufferedFile_Constructor_Read_File_Missing(self):
        self.assertRaises(FileNotFoundError, lambda: BufferedFile("testMissing.test-output", False, 1000))

def CreateTestFile(filename, data=""):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(data)

if __name__ == '__main__':
    unittest.main()
