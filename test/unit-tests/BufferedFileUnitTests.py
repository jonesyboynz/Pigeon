import unittest
import os
from TestBuffer import TestBuffer
from ut_pigeon import BufferedFile, PigeonError #Note - ut_pigeon is a copy of pigeon.py and is created by tests.ps1

'''
Tests the BufferedFile class from pigeon.py
'''
class BufferedFileTests(unittest.TestCase):

    def test_BufferedFile_Constructor_Read(self):
        CreateTestFile("test/unit-tests/test1.test-output")
        buffer = BufferedFile("test/unit-tests/test1.test-output", False, 1000)
        self.assertEqual(buffer.Filename, "test/unit-tests/test1.test-output")
        self.assertEqual(buffer.EndOfFile, False)
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)

    def test_BufferedFile_Constructor_Write(self):
        buffer = BufferedFile("test/unit-tests/test2.test-output", True, 1000)
        self.assertEqual(buffer.Filename, "test/unit-tests/test2.test-output")
        self.assertEqual(buffer.EndOfFile, False)
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)

    def test_BufferedFile_Constructor_Read_File_Missing(self):
        self.assertRaises(FileNotFoundError, lambda: BufferedFile("test/unit-tests/testMissing.test-output", False, 1000))

    def test_BufferedFile_Write(self):
        buffer = BufferedFile("test/unit-tests/test3.test-output", True, 1000)
        byteData = bytes([ord("0") for i in range(0, 2000)])
        for b in byteData:
            buffer.Write(b)
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)
        data = GetFileData("test/unit-tests/test3.test-output")
        self.assertEqual(2000, len(data))
        self.assertEqual("".join(["0" for i in range(0, 2000)]), data)

    def test_BufferedFile_Write_String(self):
        buffer = BufferedFile("test/unit-tests/test4.test-output", True, 1000)
        buffer.WriteStr("Hello World")
        buffer.Close()
        self.assertEqual(buffer.EndOfFile, True)
        data = GetFileData("test/unit-tests/test4.test-output")
        self.assertEqual("Hello World", data)

    def test_BufferedFile_Read(self):
        CreateTestFile("test/unit-tests/test5.test-output", "0123456789")
        buffer = BufferedFile("test/unit-tests/test5.test-output", False, 2)
        for i in range(0, 10):
            self.assertEqual(i + 48, buffer.Read())
        buffer.Close()

    def test_BufferedFile_Read_Past_EOF(self):
        CreateTestFile("test/unit-tests/test6.test-output", "0")
        buffer = BufferedFile("test/unit-tests/test6.test-output", False, 2)
        self.assertEqual(48, buffer.Read())
        self.assertEqual(buffer.EndOfFile, False)
        self.assertIsNone(buffer.Read())
        self.assertEqual(buffer.EndOfFile, True)

def CreateTestFile(filename, data=""):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(data)

def GetFileData(filename):
    with open(filename, "r") as f:
        return f.read()

if __name__ == '__main__':
    unittest.main()
