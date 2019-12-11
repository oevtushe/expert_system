import unittest
import TestParser

class TestTestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tests_dir = 'testparser_tests/'

    def test_no_spec_syntax(self):
        fname_in = self._tests_dir + 'test_no_spec_syntax.txt'
        tp = TestParser.TestParser(file=fname_in)
        i = 0
        for item in tp.parse():
            i += 1
        self.assertEqual(i, 0)

    def test_neg_and_pos_exp(self):
        fname_in = self._tests_dir + 'test_neg_and_pos_exp_in.txt'
        fname_out = self._tests_dir + 'test_neg_and_pos_exp_out.txt'
        with open(fname_out) as f:
            res = f.read()
        tp = TestParser.TestParser(file=fname_in)
        i = 0
        for item in tp.parse():
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], 'S')
            self.assertEqual(item[2], 'K')
        self.assertEqual(i, 1)

    def test_pos_exp(self):
        fname_in = self._tests_dir + 'test_pos_exp_in.txt'
        fname_out = self._tests_dir + 'test_pos_exp_out.txt'
        with open(fname_out) as f:
            res = f.read()
        tp = TestParser.TestParser(file=fname_in)
        i = 0
        for item in tp.parse():
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], 'S')
            self.assertEqual(item[2], None)
        self.assertEqual(i, 1)

    def test_neg_exp(self):
        fname_in = self._tests_dir + 'test_neg_exp_in.txt'
        fname_out = self._tests_dir + 'test_neg_exp_out.txt'
        with open(fname_out) as f:
            res = f.read()
        tp = TestParser.TestParser(file=fname_in)
        i = 0
        for item in tp.parse():
            i += 1
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], res)
            self.assertEqual(item[1], None)
            self.assertEqual(item[2], 'S')
        self.assertEqual(i, 1)

    def test_no_exp(self):
        fname_in = self._tests_dir + 'test_no_exp.txt'
        tp = TestParser.TestParser(file=fname_in)
        i = 0
        with self.assertRaises(TestParser.TestParserError):
            for m in tp.parse():
                i += 1
                pass
        self.assertEqual(i, 0)

    def test_multiple_exp(self):
        fname_in = self._tests_dir + 'test_multiple_exp_in.txt'
        exp_text = []
        for i in range(0, 4):
            fname_out = self._tests_dir + 'test_multiple_exp_out'
            fname_out += str(i + 1) + '.txt'
            res = ''
            with open(fname_out) as f:
                res = f.read()
            exp_text.append(res)
        exp_pos = [None, 'K', 'KM', 'K']
        exp_neg = ['S', 'M', 'I', 'MOI']
        tp = TestParser.TestParser(file=fname_in)

        for i, item in enumerate(tp.parse()):
            self.assertEqual(len(item), 3)
            self.assertEqual(item[0], exp_text[i])
            self.assertEqual(item[1], exp_pos[i])
            self.assertEqual(item[2], exp_neg[i])
        self.assertEqual(i, 3)
