from lark import Transformer
from lark import Tree

class SimplifyTree(Transformer):
    """This class removes excessive nodes
    """
    def expr_and(self, child):
        if len(child) < 2:
            return child[0]
        return Tree('expr_and', child)

    def expr_or(self, child):
        if len(child) < 2:
            return child[0]
        return Tree('expr_or', child)

    def expr_xor(self, child):
        if len(child) < 2:
            return child[0]
        return Tree('expr_xor', child)

    #TODO: Two children for !, what ?
    def expr_neg(self, child):
        if len(child) < 2:
            return child[0]
        return Tree('expr_neg', child)

    def expr_eq(self, child):
        if len(child) < 2:
            return child[0]
        return Tree('expr_eq', child)

    def factor(self, child):
        return child[0]