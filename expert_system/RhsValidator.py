from lark import Transformer
from lark import Tree

class RhsValidator(Transformer):
    """Class validates right hand side
       of rules.

       |,!,^ are forbidden in rhs
    """
    def expr_and(self, child):
        """expr_and -> true if both
           children are valid expressions

           expr_and in rhs are allowed
        """
        return child[0] and child[1]

    def expr_or(self, child):
        """expr_or -> always false
           not supported as rhs operation
           in this expert system
        """
        return False

    def expr_xor(self, child):
        """expr_xor -> always false
           not supported as rhs operation
           in this expert system
        """
        return False

    def expr_neg(self, child):
        """expr_neg -> always false
           not supported as rhs operation
           in this expert system
        """
        return False

    def val(self, child):
        """val -> always true
           values in rhs are allowed
        """
        return True
