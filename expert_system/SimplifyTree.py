from lark import Transformer
from lark import Tree

class SimplifyTree(Transformer):
    """This class removes excessive nodes
    """
    def expr_and(self, child):
        """Replaces expr_and node with
           inner one if there's

           Distinctive property is that
           the current node has only one child
        """
        if len(child) == 1:
            return child[0]
        return Tree('expr_and', child)

    def expr_or(self, child):
        """Same as expr_and
        """
        if len(child) == 1:
            return child[0]
        return Tree('expr_or', child)

    def expr_xor(self, child):
        """Same as expr_and
        """
        if len(child) == 1:
            return child[0]
        return Tree('expr_xor', child)

    def expr_neg(self, child):
        """Same as expr_and
        """
        if len(child) == 1:
            return child[0]
        return Tree('expr_neg', child)

    def expr_eq(self, child):
        """Same as expr_and
        """
        if len(child) == 1:
            return child[0]
        return Tree('expr_eq', child)

    def factor(self, child):
        """Factor node is totaly
           replaced by inner 'val'
        """
        return child[0]
