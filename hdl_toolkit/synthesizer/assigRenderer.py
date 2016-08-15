from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.statements import IfContainer, SwitchContainer
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthesizer.assigRendererContainers import DepContainer, IfTreeNode
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase 
from hdl_toolkit.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hdl_toolkit.synthesizer.rtlLevel.signalUtils.walkers import discoverEventDependency
from python_toolkit.arrayQuery import where
from hdl_toolkit.hdlObjects.types.enum import Enum


SWITCH_THRESHOLD = 2  # (max count of elsifs with eq on same variable)

def __renderStatements(statements, resultContainer):
    for st in statements:
        if isinstance(st, IfTreeNode):
            for o in _renderIfTree(st): 
                resultContainer.append(o)
        else:
            resultContainer.append(st)

def _renderIfTree(node):
    """
    Render tree of IfTreeNode objects to IfContainers, SwitchContainers etc.
    
    if number of elsifs is higher than SWITCH_THRESHOLD and all conditions are if format signal == value
    render this as switch statement
    """
    assert isinstance(node, IfTreeNode)   
    
    ifTrue = []
    __renderStatements(node.pos, ifTrue)
    
    elIfs = []
    ifFalse = []
    
    # extract elsifs
    elIfN = node
    while True:
        if len(elIfN.neg) == 1 and isinstance(elIfN.neg[0], IfTreeNode):
            # if only next if is in negative statements
            # this item is converted as elsif in this IfContainer
            elIfN = elIfN.neg[0]
            _ifTrue = []
            __renderStatements(elIfN.pos, _ifTrue)
            elIfs.append(([elIfN.cond,], _ifTrue))
        else:
            # render standard else
            __renderStatements(elIfN.neg, ifFalse)
            break
    
    # if threshold
    if len(elIfs) >= SWITCH_THRESHOLD:
        cases = []
        switchOn = None
        try:
            # detect if condition is in format signal == value 
            op = node.cond.singleDriver()
            if isinstance(op, Operator) and op.operator == AllOps.EQ:
                op0 = op.ops[0]
                op1 = op.ops[1]
                if isinstance(op0, RtlSignalBase) and isinstance(op1, Value):
                    switchOn = op0
                    cases.append((op1, ifTrue))
        except MultipleDriversExc:
            pass
        
        if switchOn is not None:
            canBeConvertedToSwitch = True
            for elIf in elIfs:
                try:
                    op = elIf[0][0].singleDriver()
                    if op.operator == AllOps.EQ:
                        op1 = op.ops[1]
                        if op.ops[0] is switchOn and isinstance(op1, Value):
                            cases.append((op1, elIf[1]))
                            continue
                    canBeConvertedToSwitch = False
                    break
                except MultipleDriversExc:
                    canBeConvertedToSwitch = False
            
            # if only last can not be part of the swicht case it can be default 
            if not canBeConvertedToSwitch and len(elIfs) == len(cases):
                default = elIfs[-1]
                ifFalse = [ IfContainer(default[0], default[1], ifFalse)]
                canBeConvertedToSwitch = True
                    
            if canBeConvertedToSwitch:
                t = switchOn._dtype
                # if nothing else and we have enum ad we used all the values
                if not ifFalse and isinstance(t, Enum) and len(t._allValues) == len(cases):
                    # convert last to default, because hdl languages usually need this
                    ifFalse = cases[-1][1]
                    cases = cases[:-1]
                    
                cases.append((None, ifFalse))
            
                yield SwitchContainer(switchOn, cases)
                raise StopIteration()
    
    yield IfContainer([node.cond], ifTrue, ifFalse, elIfs=elIfs)

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

def isEventDependent(cond):
    return bool(list(discoverEventDependency(cond)))
    
def countCondOccurrences(termMap):
    for cond, container in termMap.items():
        cnt = len(container.pos) + len(container.neg)
        yield (cond, cnt)

def sortCondsByMostImpact(countedConds):
    # id is used to make sorting more deterministic, but it is not optimal solution
    for c in sorted(countedConds, key=lambda x: (x[1], isEventDependent(x[0]), id(x[0])),
                     reverse=True):
        yield c[0]

def buildTermMapFromConditions(assignments):
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

def renderIfTree_afterCondSatisfied(assignments, globalCondOrder):
    top = []
    # there can be only one main condition ant this means 
    # only the most impact cond is taken
    # else no condition is taken and assignment is just statement at this level
    # in this step we are consuming assignment as statement
    termUsage = {}
    for a in assignments:
        # add assignments without cond as statements
        if len(a._unresolvedConds) == 0:
            top.append(a)
        else:
            # else register this to termap to resolve most impact condition
            for c in a._unresolvedConds:
                try:
                    termUsage[c[0]] += 1
                except KeyError:
                    termUsage[c[0]] = 1
                    
    # id is used to make sorting more deterministic, but it is not optimal solution
    topConds = sorted(termUsage.keys(),
                      key=lambda x: (termUsage[x], globalCondOrder.index(x), id(x)),
                      reverse=True)
    if len(topConds) == 0:
        return top 
    else:
        topCond = topConds[0]
        
        # remove resolved statements from unresolved container
        for a in top:
            assignments.remove(a)
            
        # create IfTreeNode for topCond
        topIf = splitIfTreeOnCond(assignments, topCond, topConds[1:])
        return [topIf]
    
def splitIfTreeOnCond(assignments, topCond, globalCondOrder):
    # in this step we are consuming unresolvedConds and building IfTreeNodes

    topPos = []
    topNeg = []
    for a in assignments:
        dependentOnTopCond = list(where(a._unresolvedConds, lambda cond: cond[0] is topCond))
        assert len(dependentOnTopCond) == 0 or len(dependentOnTopCond) == 1
        
        for _c in dependentOnTopCond:
            a._unresolvedConds.remove(_c)
            
            if _c[1]:
                topNeg.append(a)
            else:
                topPos.append(a)
                
    if not (len(assignments) == (len(topNeg) + len(topPos))):
        # it seems that there is some statement which is nod depended on topCond, but it should be 
        # filtered earlier
        raise AssertionError(("got assignments %s and topCond %s \n for neg resolved %s,\n" + 
                             " for pos resolved %s\n" + 
                             "something lost or duplicited in statement renderer") 
                             % (str(assignments), str(topCond), str(topNeg), str(topPos)))
    top = IfTreeNode(topCond)
    top.pos = renderIfTree_afterCondSatisfied(topPos, globalCondOrder)
    top.neg = renderIfTree_afterCondSatisfied(topNeg, globalCondOrder)
    return top


def renderIfTree(assignments):
    """
    Walk assignments and resolve if tree from conditions
    """
    # condSig:DepContainer

    
    # register assignments in tree of IfTreeNodes
    for a in assignments:
        # prepare base conds
        a._unresolvedConds = [ getBaseCond(c) for c in a.cond ]
    
    termMap = buildTermMapFromConditions(assignments)
    condOrder = list(sortCondsByMostImpact(countCondOccurrences(termMap)))
    
    
    if condOrder:
        # split assignments on most important condition
        topCond = condOrder[0]
        top = splitIfTreeOnCond(assignments, topCond, condOrder)
        
        yield from _renderIfTree(top)
    else:
        # none of assignments has condition no If or switch is needed
        yield from assignments
