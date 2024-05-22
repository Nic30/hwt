from hwt.doc_markers import internal
from hwt.pyUtils.setList import SetList


class SensitivityCtx(SetList):
    """
    Sensitivity list used for resolution of sensitivity for statement instances

    :ivar ~.contains_ev_dependency: True if this contains event dependent
        sensitivity
    """

    def __init__(self, initSeq=None):
        SetList.__init__(self, initSeq=initSeq)
        self.contains_ev_dependency = False

    @internal
    def extend(self, items):
        SetList.extend(self, items)
        if isinstance(items, SensitivityCtx):
            self.contains_ev_dependency |= items.contains_ev_dependency

    @internal
    def clear(self):
        SetList.clear(self)
        self.contains_ev_dependency = False
