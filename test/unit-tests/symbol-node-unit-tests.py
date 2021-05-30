import unittest
from TestBuffer import TestBuffer
from ut_pigeon import SymbolNode, PigeonError

class SymbolNodeTests(unittest.TestCase):

    def test_SymbolNode_Constructor(self):
        node = SymbolNode('c')
        self.assertEqual(node.Char, 'c')
        self.assertIsNone(node.Byte)

    def test_SymbolNode_Single_Extend(self):
        node = SymbolNode('c')
        node.Extend("at", 26)
        self.assertEqual(str(node), "c->(a->(t->B26))")

    def test_SymbolNode_Double_Extend(self):
        node = SymbolNode('b')
        node.Extend("at", 19)
        node.Extend("ad", 21)
        self.assertEqual(str(node), "b->(a->(t->B19,d->B21))")

    def test_SymbolNode_Bad_Extend(self):
        node = SymbolNode('b')
        node.Extend("at", 19)
        self.assertRaises(PigeonError, lambda: node.Extend("at", 21))

    def test_SymbolNode_Decode(self):
        buffer = TestBuffer([ord(x) for x in "b1b2"])
        node = SymbolNode('z')
        node.Extend("b1", 1)
        node.Extend("b2", 2)
        self.assertEqual(node.Decode(buffer), (1, 3))
        self.assertEqual(node.Decode(buffer), (2, 3))

    def test_SymbolNode_Missing_Byte_Decode(self):
        buffer = TestBuffer([ord(x) for x in "abc"])
        node = SymbolNode('z')
        node.Extend("abc", None)
        self.assertRaises(PigeonError, lambda: node.Decode(buffer))

    def test_SymbolNode_No_Decoding(self):
        buffer = TestBuffer([ord(x) for x in "b3"])
        node = SymbolNode('z')
        node.Extend("b1", 1)
        node.Extend("b2", 2)
        self.assertRaises(PigeonError, lambda: node.Decode(buffer))

if __name__ == '__main__':
    unittest.main()
