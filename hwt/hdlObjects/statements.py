
def seqEvalCond(cond):
    _cond = True
    for c in cond:
        _cond = _cond and bool(c.staticEval().val)

    return _cond


class CodeStatement():
    """
    Base class for code statements
    """

    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, DebugTmpVarStack
        tmpVars = DebugTmpVarStack()
        ctx = VhdlSerializer.getBaseContext()
        ctx.createTmpVarFn = tmpVars.createTmpVarFn

        s = getattr(VhdlSerializer, self.__class__.__name__)(self, ctx)
        return "%s%s" % (tmpVars.serialize(), s)


class IfContainer(CodeStatement):
    """
    Structural container of if statement for hdl rendering
    """
    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[]):
        """
        :param cond: list of conditions for this if
        :param ifTrue: list of statements which should be active if cond. is met
        :param elIfs: list of tuples (list of conditions, list of statements)
        :param ifFalse: list of statements which should be active if cond.
            and any other cond. in elIfs is met
        """
        self.cond = cond
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse

    def seqEval(self):
        if seqEvalCond(self.cond):
            for s in self.ifTrue:
                s.seqEval()
        else:
            for c in self.elIfs:
                if seqEvalCond(c[0]):
                    for s in c[1]:
                        s.seqEval()
                    return

            for s in self.ifFalse:
                s.seqEval()


class SwitchContainer(CodeStatement):
    """
    Structural container for switch statement for hdl rendering
    """
    def __init__(self, switchOn, cases, default=[]):
        self.switchOn = switchOn
        self.cases = cases
        self.default = default

    def seqEval(self):
        raise NotImplementedError()


class WhileContainer(CodeStatement):
    """
    Structural container of while statement for hdl rendering
    """
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def seqEval(self):
        while seqEvalCond(self.cond):
            for s in self.body:
                s.seqEval()


class WaitStm(CodeStatement):
    """
    Structural container of wait statemnet for hdl rendering
    """
    def __init__(self, waitForWhat):
        self.isTimeWait = isinstance(waitForWhat, int)
        self.waitForWhat = waitForWhat
