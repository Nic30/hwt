from hwt.pyUtils.uniqList import UniqList


class SensitivityCtx(UniqList):
    """
    :ivar contains_ev_dependency: True if this contains event dependent
        sensitivity
    """

    def __init__(self, initSeq=None):
        UniqList.__init__(self, initSeq=initSeq)
        self.contains_ev_dependency = False

    def clear(self):
        UniqList.clear(self)
        self.contains_ev_dependency = False
