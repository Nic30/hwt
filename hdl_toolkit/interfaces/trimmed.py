from hdl_toolkit.interfaces.std import Handshaked


class TrimmedHs(Handshaked):
    _NAME_SEPARATOR = ""
    def _declr(self):
        super()._declr()
        self.data._alternativeNames.append("")
        self.vld._alternativeNames.append("_vld")
        self.rd._alternativeNames.extend(["_rd", "_ack"])