from hdl_toolkit.interfaces.std import Ap_hs


class TrimmedAp_hs(Ap_hs):
    _NAME_SEPARATOR = ""
    def _declr(self):
        super()._declr()
        self.data._alternativeNames.append("")
        self.vld._alternativeNames.append("_vld")
        self.rd._alternativeNames.append("_rd")