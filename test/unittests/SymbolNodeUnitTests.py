import unittest
from pigeon import SymbolNode

class SymbolNodeTests(unittest.TestCase):

    def test_SymbolNodeConstructor(self):
        node = SymbolNode('c')
        self.assertEqual(node.Char, 'c')

if __name__ == '__main__':
    unittest.main()
