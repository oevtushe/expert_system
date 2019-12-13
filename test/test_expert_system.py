import unittest
from expert_system.ExpertSystem import ExpertSystem 
from test.TestParser import TestParser
import glob

class TestExpertSystem(unittest.TestCase):
    #TODO: there's also runtime errors that should be checked
    #      for example negation in conclusion
    def test_under_folder(self):
        self._es = ExpertSystem()
        for fname in glob.glob('test/tests_es/*.txt'):
            with self.subTest(fname=fname):
                with open(fname) as f:
                    content = f.read()
                for t, p, n in TestParser.parse(content):
                    res = self._es.resolve(t)
                    ln = 0
                    if p:
                        ln += len(p)
                    if n:
                        ln += len(n)
                    self.assertEqual(len(res), ln)
                    if p:
                        for fact in p:
                            self.assertTrue(fact in res)
                            with self.subTest(fact=fact, v=res[fact], exp=True):
                                self.assertEqual(res[fact], True)
                    if n:
                        for fact in n:
                            self.assertTrue(fact in res)
                            with self.subTest(fact=fact, v=res[fact], exp=False):
                                self.assertEqual(res[fact], False)
