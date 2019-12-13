from lark import Transformer
from lark import Tree

class ResolveLhs(Transformer):

    def transform(self, tree, facts):
        self._facts = facts
        return Transformer.transform(self, tree)

    def expr_and(self, child):
        a = child[0]
        b = child[1]
        return a and b

    def expr_or(self, child):
        a = child[0]
        b = child[1]
        return a or b

    def expr_xor(self, child):
        a = child[0]
        b = child[1]
        return a ^ b

    def expr_neg(self, child):
        return not child[1]

    def val(self, child):
        return self._facts[child[0]]
