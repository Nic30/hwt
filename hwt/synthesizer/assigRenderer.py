from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.statements import IfContainer, SwitchContainer
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.value import Value
from hwt.synthesizer.assigRendererContainers import IfTreeNode
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase 
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.termUsageResolver import extractCondTermOrderNonResolved, extractCondTermOrder
from hwt.pyUtils.arrayQuery import where

# (max count of elsifs with eq on same variable)
SWITCH_THRESHOLD = 2  

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
    assert isinstance(node, IfTreeNode), node  
    
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
            elIfs.append(([elIfN.cond, ], _ifTrue))
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
                    if isinstance(op, Operator) and op.operator == AllOps.EQ:
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

def renderIfTree_afterCondSatisfied(assignments, globalCondOrder):
    # there can be only one main condition ant this means 
    # only the most impact cond is taken
    # else no condition is taken and assignment is just statement at this level
    # in this step we are consuming assignment as statement
    top, topConds = extractCondTermOrderNonResolved(assignments, globalCondOrder)

    if len(topConds) == 0:
        return top 
    else:
        topCond = topConds[0]
        
        # remove resolved statements from unresolved container
        for a in top:
            assignments.remove(a)
            
        # create IfTreeNode for topCond
        ifs = []
        topIf, notDependent = splitIfTreeOnCond(assignments, topCond, topConds[1:])
        ifs.append(topIf)
        if notDependent:
            _ifs = renderIfTree_afterCondSatisfied(notDependent, globalCondOrder)
            ifs.extend(_ifs)
            
        return ifs
    
def splitIfTreeOnCond(assignments, topCond, globalCondOrder):
    # in this step we are consuming unresolvedConds and building IfTreeNodes

    topPos = []
    topNeg = []
    notDependent = []
    for a in assignments:
        dependentOnTopCond = list(where(a._unresolvedConds, lambda cond: cond[0] is topCond))
        l = len(dependentOnTopCond)
        
        if l == 0:
            notDependent.append(a)
        elif l == 1:
            _c = dependentOnTopCond[0]
            a._unresolvedConds.remove(_c)
            
            if _c[1]:
                topNeg.append(a)
            else:
                topPos.append(a)
        else:
            raise NotImplementedError(
                ("There are multiple different assignments to same object(%r) with same condition (%r)" % (a.dst, topCond),
                dependentOnTopCond))     
    # if not (len(assignments) == (len(topNeg) + len(topPos))):
    #    # it seems that there is some statement which is nod depended on topCond, but it should be 
    #    # filtered earlier
    #    raise AssertionError(("got assignments %s and topCond %s \n for neg resolved %s,\n" + 
    #                         " for pos resolved %s\n" + 
    #                         "something lost or duplicited in statement renderer") 
    #                         % (str(assignments), str(topCond), str(topNeg), str(topPos)))
    if len(topPos) + len(topNeg) == 0:
        raise AssertionError("Something should be dependent")
    
    top = IfTreeNode(topCond)
    top.pos = renderIfTree_afterCondSatisfied(topPos, globalCondOrder)
    top.neg = renderIfTree_afterCondSatisfied(topNeg, globalCondOrder)
    return top, notDependent


def renderIfTree(assignments):
    """
    Walk assignments and resolve if tree from conditions
    """
    condOrder = list(extractCondTermOrder(assignments))
    
    if condOrder:
        # split assignments on most important condition
        topCond = condOrder[0]
        top, notDependent = splitIfTreeOnCond(assignments, topCond, condOrder)
        
        yield from _renderIfTree(top)
        if notDependent:
            yield from renderIfTree(notDependent)
    else:
        # none of assignments has condition no If or switch is needed
        yield from assignments
