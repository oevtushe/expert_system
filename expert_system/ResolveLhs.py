from lark import Transformer
from lark import Tree

class ResolveLhs(Transformer):
    """Execute operations in lhs using
       dfs
    """
    def transform(self, tree, facts):
        """transform(self, tree, facts)
           'tree' - tree to transform
           'facts' - dict to get info about
           facts from
        """
        self._facts = facts
        return Transformer.transform(self, tree)

    def expr_and(self, child):
        """expr_and -> child0 & child1
        """
        a = child[0]
        b = child[1]
        return a and b

    def expr_or(self, child):
        """expr_or -> child0 | child1
        """
        a = child[0]
        b = child[1]
        return a or b

    def expr_xor(self, child):
        """expr_xor -> child0 ^ child1
        """
        a = child[0]
        b = child[1]
        return a ^ b

    def expr_neg(self, child):
        """expr_neg -> !child
        """
        return not child[1]

    def val(self, child):
        """val -> value of a fact
        """
        return self._facts[child[0]]
