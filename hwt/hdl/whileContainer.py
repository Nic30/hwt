from hwt.hdl.statements import HdlStatement, seqEvalCond
from hwt.doc_markers import internal


class WhileContainer(HdlStatement):
    """
    Structural container of while statement for hdl rendering
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    @internal
    def seqEval(self):
        while seqEvalCond(self.cond):
            for s in self.body:
                s.seqEval()
