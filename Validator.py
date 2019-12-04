from lark import Transformer
from lark import Tree

class InvalidRhs(Exception):
    pass

class Validator(Transformer):
    def expr_and(self, child):
        return child[0]

    def expr_or(self, child):
        return False

    def expr_xor(self, child):
        return False

    def expr_neg(self, child):
        return False

    def factor(self, child):
        return True
