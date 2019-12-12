import unittest
import glob
import lark

class TestGrammar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tests_path = 'tests_grammar/'
        cls._lark = lark.Lark.open('../grammar.lark')

    def test_valid_syntax(self):
        for fname in glob.glob(self._tests_path + 'valid/*.txt'):
            with self.subTest(fname=fname):
                with open(fname) as f:
                    content = f.read()
                self._lark.parse(content)


    def test_invalid_syntax(self):
        for fname in glob.glob(self._tests_path + 'invalid/*.txt'):
            with self.subTest(fname=fname):
                with open(fname) as f:
                    content = f.read()
                with self.assertRaises(Exception):
                    self._lark.parse(content)
