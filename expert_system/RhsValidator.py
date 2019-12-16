from lark import Transformer
from lark import Tree

class RhsValidator(Transformer):
    """Class validates right hand side
       of rules.

       |,!,^ are forbidden in rhs
    """
    def expr_and(self, child):
        return child[0] and child[1]

    def expr_or(self, child):
        return False

    def expr_xor(self, child):
        return False

    def expr_neg(self, child):
        return False

    def val(self, child):
        return True
