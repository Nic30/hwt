from hwt.pyUtils.uniqList import UniqList
from hwt.doc_markers import internal


class SensitivityCtx(UniqList):
    """
    Sensitivity list used for resolution of sensitivity for statements and HdlStatementBlock instances

    :ivar ~.contains_ev_dependency: True if this contains event dependent
        sensitivity
    """

    def __init__(self, initSeq=None):
        UniqList.__init__(self, initSeq=initSeq)
        self.contains_ev_dependency = False

    @internal
    def extend(self, items):
        UniqList.extend(self, items)
        if isinstance(items, SensitivityCtx):
            self.contains_ev_dependency |= items.contains_ev_dependency

    @internal
    def clear(self):
        UniqList.clear(self)
        self.contains_ev_dependency = False
