from itertools import groupby
from hwt.synthesizer.codeOps import c


class FsmBuilder(object):
    def __init__(self, fsmReg, transitions):
        self.st = fsmReg
        self.transitions = transitions
        
    def build(self):
        states = self.st._dtype._allValues
        transitions = groupby(self.transitions, lambda x : x[0]) 
        cases = []
        for s in states:
            try:
                trans = transitions[s]
            except KeyError:
                cases.append(c(self.st, self.st))
                continue
            # compute closure of all transitions and in this closures stabilize st
            # collect all conds from all assignments
            # if set is empty no need to add closure
            # 