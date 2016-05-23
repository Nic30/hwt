from hdl_toolkit.synthetisator.rtlLevel.codeOp import IfContainer, \
    SwitchContainer
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal, MultipleDriversExc
from hdl_toolkit.hdlObjects.value import Value

SWITCH_THRENDSHOOD = 2  # (max count of elsifs with eq on same variable)

class DepContainer():
    def __init__(self):
        self.pos = set()  # if cond
        self.neg = set()  # if not cond
        
    def __repr__(self):
        return "<DepContainer pos:%s, neg:%s>" % (repr(self.pos), repr(self.neg))

class IfTreeNode():
    """
    @ivar posSt: statements which will happen if condition is met
    @ival pos: dict condition : IfTreeNode object
    
    @ivar negSt: statements which will happen if condition is not met
    @ival neg: dict condition : IfTreeNode object
    
    """
    def __init__(self):
        self.posSt = []
        self.pos = {}
        self.negSt = []
        self.neg = {}

def __renderIfTree(statements, subIfs, resultContainer):
    for st in statements:
        resultContainer.append(st)
    for k, v in subIfs.items():
        for o in _renderIfTree(k, v): 
            resultContainer.append(o)



def _renderIfTree(cond, node):
    """
    Render tree of IfTreeNode objects to IfContainers, SwitchContainers etc.
    
    if in negSt is nothing and only single item is in neg
    this item is converted as elsif in this IfContainer
   
    if number of elsifs is higher than SWITCH_THRENDSHOOD and all conditions are if format signal == value
    render this as switch statement
   
    """
            
    ifTrue = []
    __renderIfTree(node.posSt, node.pos, ifTrue)
    
    elIfs = []
    ifFalse = []
    
    
    elIfN = node
    while True:
        if len(elIfN.negSt) == 0 and len(elIfN.neg) == 1:
            key, elIfN = list(elIfN.neg.items())[0]
            _ifTrue = []
            __renderIfTree(elIfN.posSt, elIfN.pos, _ifTrue)
            elIfs.append((key, _ifTrue))
        else:
            __renderIfTree(elIfN.negSt, elIfN.neg, ifFalse)
            break
    
    #__renderIfTree(node.negSt, node.neg, ifFalse)
    if len(elIfs) >= SWITCH_THRENDSHOOD:
        cases = []
        switchOn = None
        try:
            op = cond.singleDriver()
            if op.operator == AllOps.EQ:
                op0 = op.ops[0]
                op1 = op.ops[1]
                if isinstance(op0, Signal) and isinstance(op1, Value):
                    switchOn = op0
                    cases.append((op1, ifTrue))
        except MultipleDriversExc:
            pass
        
        if switchOn is not None:
            canBeConvertedToSwitch = True
            for elIf in elIfs:
                try:
                    op = elIf[0].singleDriver()
                    if op.operator == AllOps.EQ:
                        op1 = op.ops[1]
                        if op.ops[0] is switchOn and isinstance(op1, Value):
                            cases.append((op1, elIf[1]))
                        else:
                            canBeConvertedToSwitch = False
                            break
                except MultipleDriversExc:
                    canBeConvertedToSwitch = False
                    
            if canBeConvertedToSwitch:
                cases.append((None, ifFalse))
            
                yield SwitchContainer(switchOn, cases)
                raise StopIteration()
    
    yield IfContainer([cond], ifTrue, ifFalse, elIfs=elIfs)




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
        if d.operator == AllOps.NOT:
            c = d.ops[0]
            isNegated = True
    return (c, isNegated)


def countCondOccurrences(termMap):
    """inf means it is event dependent cond and it should be used 
    as highest priority cond"""
    for cond, container in termMap.items():
        drivers = None
        try:
            drivers = cond.drivers
        except AttributeError:
            pass
        
        if drivers is not None and len(drivers) == 1 \
           and list(drivers)[0].operator == AllOps.RISING_EDGE:
            cnt = float('inf')
        else:
            cnt = len(container.pos) + len(container.neg)
        yield (cond, cnt)

def sortCondsByMostImpact(countedConds):
    for c in sorted(countedConds, key=lambda x: x[1]):
        yield c[0]
        
def renderIfTree(assigments):
    termMap = {}

    def insertToMap(condSig, assigment, isNegated):
        try:
            cont = termMap[condSig]
        except KeyError:
            cont = DepContainer()
            termMap[condSig] = cont
        if isNegated:
            cont.neg.add(assigment)
        else:
            cont.pos.add(assigment)
    def registerToMap(assigment):
        for c in assigment.cond:
            realC, isNegated = getBaseCond(c)
            insertToMap(realC, assigment, isNegated)
    # resolve main hierarchy of conditions
    for a in assigments:
        registerToMap(a)
    
    condOrder = list(sortCondsByMostImpact(countCondOccurrences(termMap)))

    top = IfTreeNode()
    
    def toTree():
        """register assignments in tree of IfTreeNodes"""
        for a in assigments:
            _top = top.pos
            topNode = top
            # build cond path in node tree
            realCond = [ getBaseCond(c) for c in a.cond ]
            sortedCond = sorted(realCond,
                                key=lambda x: condOrder.index(x[0]),
                                reverse=True)
            isNegated = False

            # walk cond path in node tree
            for c, isNegated in sortedCond:
                try:
                    _top = _top[c]
                except KeyError:
                    t = IfTreeNode()
                    _top[c] = t
                    _top = t
                    
                topNode = _top
                if isNegated:
                    _top = _top.neg
                else:
                    _top = _top.pos
                    
            # register this assigment at the end of cond path        
            if isNegated:
                topNode.negSt.append(a)
            else:
                topNode.posSt.append(a)
    toTree()


        
    if condOrder:
        for k, v in top.pos.items():
            yield from _renderIfTree(k, v)
    else:
        # none of assignments has condition
        yield from assigments
