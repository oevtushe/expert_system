import lark
import SimplifyTree
import logging
from ResolveLhs import ResolveLhs
import Validator
from collections import defaultdict

# if i met recursion, say it's recursion
class ExpertSystem:
    def __init__(self, inp):
        logging.basicConfig(level=logging.DEBUG)
        self._lk = lark.Lark.open('grammar.lark')
        interm = self._lk.parse(inp)
        smpl = SimplifyTree.SimplifyTree()
        self._tree = smpl.transform(interm)
        self._facts = defaultdict(lambda: False)
        self._questions = list()
        self._rules = list(self._tree.find_data('rule'))
        self._rl = ResolveLhs()
        self._validator = Validator.Validator()
        def_tree = list(self._tree.find_data('defines'))[0]
        for v in def_tree.children:
            self._facts[v.value] = True
        qes_tree = list(self._tree.find_data('questions'))[0]
        for v in qes_tree.children:
            self._questions.append(v.value)
        logging.debug(f'facts: {self._facts}')
        logging.debug(f'questions: {self._questions}')

    def resolve(self):
        stack = self._check_rules(self._questions)
        if stack:
            for rset in reversed(stack):
                res = False
                for r in rset:
                    res = self._rl.transform(r.children[0], self._facts)
                    if res:
                        break
                for rhv in list(r.children[2].find_data('val')):
                    if not self._facts[rhv.children[0]]:
                        self._facts[rhv.children[0]] = res
                        logging.debug(f'set {rhv.children[0]} to {res}')
        for q in self._questions:
            print(f'{q} is {self._facts[q]}')

    def _get_rules_with_rhs(self, val):
        res = set()
        for rule in self._rules:
            if any(x.children[0] == val for x in list(rule.children[2].find_data('val'))):
                logging.debug(f'found {val} in {rule}')
                res.add(rule)
        return res
        
    def _vars(self, rule, side):
        if side == 'l':
            idx = 0
        elif side == 'r':
            idx = 2
        for x in list(rule.children[idx].find_data('val')):
            yield x.children[0].value

    def _check_rules_rhs(self, rules):
        for r in rules:
            res = self._validator.transform(r.children[2])
            if not res:
                return False
        return True
            

    def _check_rules(self, q):
        lst = [] + q
        stack = []
        stacked_rules = set()
        for var in lst:
            rset = self._get_rules_with_rhs(var)
            if not rset:
                print(f'{var} there\'s no rule that resolves it, set it as False')
                continue
            if not self._check_rules_rhs(rset):
                print(f'{var} is set as False, due to invalid rule for it')
                continue
            diff = rset.difference(stacked_rules)
            if diff:
                stack.append(diff)
                stacked_rules.update(rset)
                for r in rset:
                    for v in self._vars(r, 'l'):
                        if not v in self._facts:
                            logging.debug(f'{v} is not resolved, queue for resolving')
                            lst.append(v)
                        else:
                            logging.debug(f'{v} is known')
            else:
                logging.debug(f'Stack already has a rule to resolve {var}')
        logging.debug(f'stack: {stack}')
        return stack

