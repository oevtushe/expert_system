import unittest
from test.TestParser import TestParser
from test.TestParser import TestParserError

class TestTestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tests_dir = 'test/testparser_tests/'

    @staticmethod
    def _read_tf(fpath):
        with open(fpath) as f:
            content = f.read()
        return content

    def test_no_spec_syntax(self):
        fname_in = self._tests_dir + 'test_no_spec_syntax.txt'
        i = 0
        for item in TestParser.parse(self._read_tf(fname_in)):
            i += 1
        self.assertEqual(i, 0)

    def test_neg_and_pos_exp(self):
        fname_in = self._tests_dir + 'test_neg_and_pos_exp_in.txt'
        fname_out = self._tests_dir + 'test_neg_and_pos_exp_out.txt'
        res = self._read_tf(fname_out)
        i = 0
        for item in TestParser.parse(self._read_tf(fname_in)):
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], 'S')
            self.assertEqual(item[2], 'K')
        self.assertEqual(i, 1)

    def test_pos_exp(self):
        fname_in = self._tests_dir + 'test_pos_exp_in.txt'
        fname_out = self._tests_dir + 'test_pos_exp_out.txt'
        res = self._read_tf(fname_out)
        i = 0
        for item in TestParser.parse(self._read_tf(fname_in)):
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], 'S')
            self.assertEqual(item[2], None)
        self.assertEqual(i, 1)

    def test_neg_exp(self):
        fname_in = self._tests_dir + 'test_neg_exp_in.txt'
        fname_out = self._tests_dir + 'test_neg_exp_out.txt'
        res = self._read_tf(fname_out)
        i = 0
        for item in TestParser.parse(self._read_tf(fname_in)):
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], None)
            self.assertEqual(item[2], 'S')
        self.assertEqual(i, 1)

    def test_no_exp(self):
        fname_in = self._tests_dir + 'test_no_exp.txt'
        i = 0
        with self.assertRaises(TestParserError):
            for m in TestParser.parse(self._read_tf(fname_in)):
                i += 1
                pass
        self.assertEqual(i, 0)

    def test_multiple_exp(self):
        fname_in = self._tests_dir + 'test_multiple_exp_in.txt'
        exp_text = []
        for i in range(0, 4):
            fname_out = self._tests_dir + 'test_multiple_exp_out'
            fname_out += str(i + 1) + '.txt'
            res = self._read_tf(fname_out)
            exp_text.append(res)
        exp_pos = [None, 'K', 'KM', 'K']
        exp_neg = ['S', 'M', 'I', 'MOI']

        for i, item in enumerate(TestParser.parse(self._read_tf(fname_in))):
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], exp_text[i])
            self.assertEqual(item[1], exp_pos[i])
            self.assertEqual(item[2], exp_neg[i])
        self.assertEqual(i, 3)
