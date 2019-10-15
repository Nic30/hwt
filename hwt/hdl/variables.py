from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.hdlObject import HdlObject
from hwt.doc_markers import internal


class SignalItem(HdlObject):
    """
    basic hdl signal used to design circuits
    """

    def __init__(self, name, dtype, defVal=None, virtualOnly=False):
        """
        :param name: name for better orientation in netlists
            (used only in serialization)
        :param dtype: data type of this signal
        :param defVal: value for initialization
        :param virtualOnly: flag indicates that this assignments is only
            virtual and should not be added into
            netlist, because it is only for internal notation
        """
        self.name = name
        self._dtype = dtype
        self.virtualOnly = virtualOnly
        if defVal is None:
            defVal = dtype.from_py(None)
        self.defVal = defVal
        self._setDefValue()

    @internal
    def _setDefValue(self):
        v = self.defVal
        if isinstance(v, RtlSignalBase):
            v = v.staticEval()

        self._val = v.__copy__()
        self._oldVal = self._val.__copy__()
        self._oldVal.vld_mask = 0
