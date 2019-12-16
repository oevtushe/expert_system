import unittest
import lark
from expert_system.ExpertSystem import _MyGraph

class TestMyGraph(unittest.TestCase):
    def test_add_child(self):
        mt = _MyGraph(None)
        child = _MyGraph('child')
        mt.add_child(child)
        self.assertEqual(mt.num_childs(), 1)

    def test_find_with_recursion(self):
        mt = _MyGraph(None)
        r1 = lark.Tree('val', '1')
        r2 = lark.Tree('val', '2')
        r3 = lark.Tree('val', '3')
        r4 = lark.Tree('val', '4')
        child1 = _MyGraph(r1)
        child2 = _MyGraph(r2)
        child3 = _MyGraph(r4)
        child1.add_child(child2)
        child1.add_child(child3)
        child2.add_child(child1)
        mt.add_child(child1)
        self.assertEqual(mt.find(r3), None)
        self.assertEqual(mt.find(r4), child3)

    def test_find_simple(self):
        mt = _MyGraph(None)
        r1 = lark.Tree('val', '1')
        r2 = lark.Tree('val', '2')
        r3 = lark.Tree('val', '3')
        r4 = lark.Tree('val', '4')
        r5 = lark.Tree('val', '5')
        r6 = lark.Tree('val', '6')
        child1 = _MyGraph(r1)
        child2 = _MyGraph(r2)
        child3 = _MyGraph(r3)
        child4 = _MyGraph(r4)
        child5 = _MyGraph(r5)
        child6 = _MyGraph(r6)

        mt.add_child(child1)
        child1.add_child(child2)
        child2.add_child(child3)
        child3.add_child(child4)
        child2.add_child(child5)
        child5.add_child(child6)
        self.assertEqual(mt.find(r6), child6)
        self.assertEqual(mt.find(r5), child5)
        self.assertEqual(mt.find(None), mt)

    def test_visitdfs_simple(self):
        mt = _MyGraph(None)
        r1 = lark.Tree('val', '1')
        r2 = lark.Tree('val', '2')
        r3 = lark.Tree('val', '3')
        r4 = lark.Tree('val', '4')
        r5 = lark.Tree('val', '5')
        r6 = lark.Tree('val', '6')
        child1 = _MyGraph(r1)
        child2 = _MyGraph(r2)
        child3 = _MyGraph(r3)
        child4 = _MyGraph(r4)
        child5 = _MyGraph(r5)
        child6 = _MyGraph(r6)

        mt.add_child(child1)
        child1.add_child(child2)
        child2.add_child(child3)
        child3.add_child(child4)
        child2.add_child(child5)
        child5.add_child(child6)
        order = [child4, child3, child6, child5, child2, child1]
        def visitor(rule):
            self.assertEqual(order.pop(0).get_rule(), rule)
        mt.visit_dfs(visitor)

    def test_visitdfs_recursion(self):
        mt = _MyGraph(None)
        r1 = lark.Tree('val', '1')
        r2 = lark.Tree('val', '2')
        r3 = lark.Tree('val', '3')
        r4 = lark.Tree('val', '4')
        child1 = _MyGraph(r1)
        child2 = _MyGraph(r2)
        child3 = _MyGraph(r4)
        child1.add_child(child2)
        child1.add_child(child3)
        child2.add_child(child1)
        mt.add_child(child1)
        order = [child2, child3, child1]
        def visitor(rule):
            self.assertEqual(order.pop(0).get_rule(), rule)
        mt.visit_dfs(visitor)
