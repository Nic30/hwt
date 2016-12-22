from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.synthesizer.rtlLevel.signalUtils.walkers import discoverEventDependency

class DepContainer():
    def __init__(self):
        self.pos = set()  # if cond
        self.neg = set()  # if not cond
        
    def __repr__(self):
        return "<DepContainer pos:%s, neg:%s>" % (repr(self.pos), repr(self.neg))

def getBaseCond(c):
    """
    if is negated return original cond and negated flag
    """
    isNegated = False
    drivers = []
    try:
        drivers = c.drivers
    except AttributeError:
        pass
    if len(drivers) == 1:
        d = list(c.drivers)[0]
        if isinstance(d, Operator) and d.operator == AllOps.NOT:
            c = d.ops[0]
            isNegated = True
    return (c, isNegated)

    
def buildTermMapFromConditions(assignments):
    """
    Generate dict condition:DepContainer
    for each condition term in conditions of assignments
    """
    termMap = {}
    
    def insertToMap(condSig, assigment, isNegated):
        try:
            cont = termMap[condSig]
        except KeyError:
            cont = DepContainer()
            termMap[condSig] = cont
        
        if isNegated:
            c = cont.neg
        else:
            c = cont.pos
        c.add(assigment)
    
    def registerToMap(assigment):
        # walk all assignments and register them in term map
        # cond is set of term in conjunctive form
        for realC, isNegated in assigment._unresolvedConds:
            insertToMap(realC, assigment, isNegated)
            
    # resolve main hierarchy of conditions
    for a in assignments:
        registerToMap(a)
    
    return termMap

def countCondOccurrences(termMap):
    for cond, container in termMap.items():
        cnt = len(container.pos) + len(container.neg)
        maxStmId = 0
        for c in [container.pos, container.neg]:
            maxStmId = max([maxStmId, *map(lambda x: x._instId, c)]) 
        yield TermUsageRecord(cond, cnt, maxStmId)

def sortCondsByMostImpact(countedConds):
    for c in sorted(countedConds,
                    key=lambda x: (x.usedCnt, x.isEventDependent, x.maxStmId, x.term._instId),
                     reverse=True):
        yield c.term

class TermUsageRecord(object):
    def __init__(self, term, usedCnt, maxStmId):
        self.term = term
        self.usedCnt = usedCnt
        self.isEventDependent = any(discoverEventDependency(term))
        self.maxStmId = maxStmId
    
    
def extractCondTermOrder(assignments):
            # register assignments in tree of IfTreeNodes
    for a in assignments:
        # prepare base conds
        a._unresolvedConds = [ getBaseCond(c) for c in a.cond ]
    
    termMap = buildTermMapFromConditions(assignments)
    cntTerms = countCondOccurrences(termMap)
    yield from sortCondsByMostImpact(cntTerms)

class TermResolveReport():
    def __init__(self, usageCnt, maxStmId):
        self.usageCnt = usageCnt
        self.maxStmId = maxStmId

    

def extractCondTermOrderNonResolved(assignments, globalCondOrder):
    """
    Extract condition order from non resolved condition terms in assignments
    """
    termUsage = {}
    resolved = [] 
    
    for a in assignments:
        # add assignments without cond as statements
        if len(a._unresolvedConds) == 0:
            resolved.append(a)
        else:
            # else register this to termap to resolve most impact condition
            for c in a._unresolvedConds:
                try:
                    r = termUsage[c[0]]
                except KeyError:
                    r = TermResolveReport(0, 0)
                    termUsage[c[0]] = r
                finally:
                    r.usageCnt += 1
                    r.maxStmId = max(a._instId, r.maxStmId)

    def trrSortKey(term):
        termResRep = termUsage[term] 
        return (termResRep.usageCnt, globalCondOrder.index(term), termResRep.maxStmId)
                    
    # id is used to make sorting more deterministic, but it is not optimal solution
    condOrder = sorted(termUsage.keys(),
                      key=trrSortKey,
                      reverse=True)
    return resolved, condOrder