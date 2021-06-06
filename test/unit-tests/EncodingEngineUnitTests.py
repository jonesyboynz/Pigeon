import unittest
import os
from TestBuffer import TestBuffer
from ut_pigeon import EncodingEngine, PigeonError #Note - ut_pigeon is a copy of pigeon.py and is created by tests.ps1

'''
Tests the EncodingEngine class from pigeon.py
'''
class EncodingEngineTests(unittest.TestCase):

    #Setup
    def test_EncodingEngine_Constructor_and_build(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json"))
        self.assertIsNotNone(engine)
        builtEngine = engine.Build()
        self.assertEqual(engine, builtEngine)

    def test_EncodingEngine_Constructor_Header_and_MetadataSeperator(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        self.assertEqual(engine.Header, "!!!p1ge0n")
        self.assertEqual(engine.MetadataSeperator, ":")

    def test_EncodingEngine_Constructor_Missing_Header(self):
        self.assertRaises(PigeonError, lambda: EncodingEngine("""{"metadata-seperator": ":"}""").Build())

    def test_EncodingEngine_Constructor_Missing_Metadata_Seperator(self):
        self.assertRaises(PigeonError, lambda: EncodingEngine("""{"header": "!!!p1ge0n"}""").Build())

    #Encoding
    def test_EncodingEngine_Encode_Three_Bytes(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in "\x00\x00\x00"])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Encode(bufferIn, bufferOut, 10), 3)
        self.assertEqual("+z+z+z", "".join([chr(x) for x in bufferOut.BytesIn]))

    def test_EncodingEngine_Encode_Empty_File(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in ""])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Encode(bufferIn, bufferOut, 10), 0)
        self.assertEqual("", "".join([chr(x) for x in bufferOut.BytesIn]))

    def test_EncodingEngine_Encode_Hello_World(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in "Hello World"])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Encode(bufferIn, bufferOut, 10), 10)
        self.assertEqual(engine.Encode(bufferIn, bufferOut, 10), 1)
        self.assertEqual("iVOOL+33LIOW", "".join([chr(x) for x in bufferOut.BytesIn]))

    #Decoding
    def test_EncodingEngine_Decode_Metadata_Seek_At_Start(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in "!!!p1ge0n:1.0.0:file.txt:?r?r?r:"])
        self.assertEqual(("1.0.0", "file.txt"), engine.SeekMetadata(bufferIn))

    def test_EncodingEngine_Decode_Metadata_Seek_In_Middle(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        buffer = TestBuffer([ord(x) for x in "... and here is the file that you need to import:\n!!!p1ge0n:2.6.9:visa.png:?r?r?r:"])
        self.assertEqual(("2.6.9", "visa.png"), engine.SeekMetadata(buffer))

    def test_EncodingEngine_Decode_Metadata_Header_Missing(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        buffer = TestBuffer([ord(x) for x in "... and here is the file that you need to import:\n!!!p1DELETEDng:?r?r?r:"])
        self.assertRaises(PigeonError, lambda: engine.SeekMetadata(buffer))

    def test_EncodingEngine_Decode_Metadata_Body_Missing(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        buffer = TestBuffer([ord(x) for x in "... and here is the file that you need to import:\n!!!p1ge0n:DELETED?r?r?r:"])
        self.assertRaises(PigeonError, lambda: engine.SeekMetadata(buffer))

    def test_EncodingEngine_Decode_Empty_File(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in ":"])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Decode(bufferIn, bufferOut, 10), 1)
        self.assertEqual("", "".join([chr(x) for x in bufferOut.BytesIn]))

    def test_EncodingEngine_Decode_Three_Bytes(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in "?r?r?r:"])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Decode(bufferIn, bufferOut, 10), 7)
        self.assertEqual("\xFF\xFF\xFF", "".join([chr(x) for x in bufferOut.BytesIn]))

    def test_EncodingEngine_Decode_Hello_World(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferIn = TestBuffer([ord(x) for x in "iVOOL+33LIOW:"])
        bufferOut = TestBuffer([])
        self.assertEqual(engine.Decode(bufferIn, bufferOut, 10), 10)
        self.assertEqual(engine.Decode(bufferIn, bufferOut, 10), 3)
        self.assertEqual("Hello World", "".join([chr(x) for x in bufferOut.BytesIn]))

    #Encode then decode
    def test_EncodingEngine_Encode_And_Decode(self):
        engine = EncodingEngine(LoadJsonFromFile("test/unit-tests/basic.json")).Build()
        bufferInEncode = TestBuffer([ord(x) for x in "Encode then decode!"])
        bufferOutEncode = TestBuffer([])
        engine.Encode(bufferInEncode, bufferOutEncode, 100)
        bufferInDecode = TestBuffer(bufferOutEncode.BytesIn)
        bufferOutDecode = TestBuffer([])
        engine.Decode(bufferInDecode, bufferOutDecode, 100)
        self.assertEqual("Encode then decode!", "".join([chr(x) for x in bufferOutDecode.BytesIn]))

def LoadJsonFromFile(filename):
    if not os.path.exists(filename):
        raise AssertionError("{0} not found. Test failed!".format(filename))
    with open(filename, "r") as f:
        return f.read()

if __name__ == '__main__':
    unittest.main()
