import lark
from expert_system.SimplifyTree import SimplifyTree
import logging
from expert_system.ResolveLhs import ResolveLhs
from expert_system.RhsValidator import RhsValidator
from collections import defaultdict

class _MyTree:
    def __init__(self, rule):
        self._rule = rule
        self._clst = []

    def add_child(self, child):
        self._clst.append(child)

    def find(self, rule):
        if rule == self._rule:
            return self
        for child in self._clst:
            return child.find(rule)
        return None

    def _visit_dfs(self, visited, fu):
        visited.add(self._rule)
        if self._rule:
            logging.debug(f'Visited:{self._rule.pretty()}')
        for child in self._clst:
            if not child._rule in visited:
                child._visit_dfs(visited, fu)
            else:
                logging.debug(f'Ignoring: {child._rule.pretty()}')
        if self._rule:
            fu(self._rule)

    def visit_dfs(self, fu):
        visited = set()
        self._visit_dfs(visited, fu)

class ExpertSystem:
    def __init__(self):
        logging.basicConfig()
        self._lk = lark.Lark.open('expert_system/grammar.lark')
        self._smpl = SimplifyTree()
        self._tree = None
        self._facts = defaultdict(lambda: False)
        self._questions = list()
        self._rl = ResolveLhs()
        self._validator = RhsValidator()

    def _parse_inp(self, inp):
        interm = self._lk.parse(inp)
        self._tree = self._smpl.transform(interm)
        def_tree = list(self._tree.find_data('defines'))[0]
        for v in def_tree.children:
            self._facts[v.value] = True
        qes_tree = list(self._tree.find_data('questions'))[0]
        for v in qes_tree.children:
            self._questions.append(v.value)
        logging.debug(f'facts: {self._facts}')
        logging.debug(f'questions: {self._questions}')

    def _reset(self):
        self._tree = None
        self._facts.clear()
        self._questions.clear()

    def _rule_solver(self, rule):
        res = self._rl.transform(rule.children[0], self._facts)
        for rhv in list(rule.children[2].find_data('val')):
            if not self._facts[rhv.children[0]]:
                self._facts[rhv.children[0]] = res
                logging.debug(f'set {rhv.children[0]} to {res}')

    def resolve(self, inp):
        self._parse_inp(inp)
        root = self._check_rules(self._questions)
        root.visit_dfs(logging.debug)
        root.visit_dfs(self._rule_solver)
        res = {q:self._facts[q] for q in self._questions}
        self._reset()
        return res

    def _get_rules_with_rhs(self, val):
        res = list()
        for rule in list(self._tree.find_data('rule')):
            if any(x.children[0] == val for x in list(rule.children[2].find_data('val'))):
                logging.debug(f'found {val} in {rule.pretty()}')
                res.append(rule)
        return res
        
    def _vars(self, rule, side):
        if side == 'l':
            idx = 0
        elif side == 'r':
            idx = 2
        for x in list(rule.children[idx].find_data('val')):
            yield x.children[0].value

    def _remove_unsupported(self, rules):
        to_del = []
        for r in rules:
            res = self._validator.transform(r.children[2])
            if not res:
                to_del.append(r)
        for x in to_del:
            logging.debug(f'Unsupported: {x.pretty()}')
            rules.remove(x)

    def _check_rules(self, qes):
        root = _MyTree(None)
        deplst = [_Dep(root, [q]) for q in qes]
        for dep in deplst:
            kiddo = dep.node
            for var in dep.flst:
                rlist = self._get_rules_with_rhs(var)
                if not rlist:
                    logging.debug(f'{var} there\'s no rule that resolves it, set it as False')
                    continue
                self._remove_unsupported(rlist)
                for r in rlist:
                    logging.debug(f'Looking for {r.pretty()} in {root}')
                    found = root.find(r)
                    if found:
                        logging.debug(f'rule {found._rule.pretty()} is already in the tree, linking')
                        kiddo.add_child(found)
                        continue
                    new_kiddo = _MyTree(r)
                    kiddo.add_child(new_kiddo)
                    logging.debug(f'Adding new kiddo: {new_kiddo}')
                    new_dep = (_Dep(new_kiddo, []))
                    for v in self._vars(r, 'l'):
                        if not v in self._facts:
                            logging.debug(f'{v} is not resolved, queue for resolving')
                            new_dep.flst.append(v)
                        else:
                            logging.debug(f'{v} is known')
                    if new_dep.flst:
                        deplst.append(new_dep)
        root.visit_dfs(logging.debug)
        return root

class _Dep:
    def __init__(self, node, flst):
        self.node = node
        self.flst = flst
