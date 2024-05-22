from hwt.serializer.generic.tmpVarConstructor import TmpVarConstructor
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class TmpVarConstructorConstOnly(TmpVarConstructor):

    def finish_var_init(self, var: RtlSignal):
        hdl = self.extraVarsHdl
        as_hdl = self.toHdlAst.as_hdl_HdlSignalItem(var, declaration=True)
        hdl.append(as_hdl)

    def sort_hdl_declarations_first(self):
        pass  # always sorted
