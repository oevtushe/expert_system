import lark
import SimplifyTree
import logging
from ResolveLhs import ResolveLhs
import Validator

# if i met recursion, say it's recursion
class ExpertSystem:
    def __init__(self, inp):
        logging.basicConfig(level=logging.DEBUG)
        self._lk = lark.Lark.open('grammar.lark')
        interm = self._lk.parse(inp)
        smpl = SimplifyTree.SimplifyTree()
        self._tree = smpl.transform(interm)
        self._facts = dict()
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
            for v, rlst in reversed(stack):
                res = False
                for r in rlst:
                    res = self._rl.transform(r.children[0], self._facts)
                    logging.debug(f'{v} resolved as {res} from rule {r}')
                    if res:
                        break
                for rhv in list(r.children[2].find_data('val')):
                    logging.debug(f'set {rhv.children[0]} to {res}')
                    if rhv.children[0] not in self._facts:
                        self._facts[rhv.children[0]] = res
        for q in self._questions:
            if q in self._facts:
                print(f'{q} is {self._facts[q]}')
            else:
                print(f'{q} is False by default')

    def _get_rules_with_rhs(self, val):
        res = set()
        for rule in self._rules:
            if any(x.children[0] == val for x in list(rule.children[2].find_data('val'))):
                logging.debug(f'found {val} in {rule}')
                res.add(rule)
        return res
        
    def _get_lhs_vars(self, rule):
        return [x.children[0].value for x in list(rule.children[0].find_data('val'))]

    def _check_rules_rhs(self, rules):
        for r in rules:
            res = self._validator.transform(r.children[2])
            if not res:
                return False
        return True
            

    def _check_rules(self, q):
        lst = [] + q
        stack = []
        for var in lst:
            rset = self._get_rules_with_rhs(var)
            if not rset:
                print(f'{var} there\'s no rule that resolves it, set it as False')
                self._facts[var] = False
                continue
            if not self._check_rules_rhs(rset):
                print(f'{var} is set as False, due to invalid rule for it')
                self._facts[var] = False
                continue
            if any(y.intersection(rset) for x,y in stack):
                print('recursion detected, ruleset is ill-formed exiting...')
                return None
            stack.append((var, rset))
            for r in rset:
                lhs = self._get_lhs_vars(r)
                for x in lhs:
                    if not x in self._facts:
                        logging.debug(f'{x} is not resolved, queue for resolving')
                        lst.append(x)
                    else:
                        logging.debug(f'{x} is known')
        logging.debug(f'stack: {stack}')
        return stack

