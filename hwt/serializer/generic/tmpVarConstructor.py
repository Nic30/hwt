from typing import Optional, Union, Tuple

from hdlConvertorAst.hdlAst import HdlIdDef
from hdlConvertorAst.translate.common.name_scope import NameScope
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.const import HConst
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class TmpVarConstructor():

    def __init__(self, toHdlAst, name_scope: NameScope):
        self.toHdlAst = toHdlAst
        self.name_scope = name_scope
        self.extraVarsHdl = []
        self.cache = {}

    def create_var_cached(self, suggestedName: str, dtype: HdlType,
                       const=False,
                       def_val: Optional[Union[RtlSignalBase, HConst]]=None,
                       postponed_init=False,
                       extra_args=None) -> Tuple[bool, RtlSignal]:
        cache_k = (suggestedName, dtype, const, def_val, extra_args)
        try:
            return False, self.cache[cache_k]
        except KeyError:
            pass
        v = self.create_var(suggestedName, dtype, const=const, def_val=def_val, postponed_init=postponed_init)
        self.cache[cache_k] = v
        return True, v

    def create_var(self,
               suggestedName: str,
               dtype: HdlType,
               const=False,
               def_val: Optional[Union[RtlSignalBase, HConst]]=None,
               postponed_init=False) -> RtlSignal:
        # create a new tmp variable in current process
        s = RtlSignal(None, None, dtype, virtual_only=True)
        s._name = self.name_scope.checked_name(suggestedName, s)
        s.hidden = False
        s._const = const

        if def_val is not None:
            s.def_val = def_val
            if not (isinstance(def_val, RtlSignalBase) and not def_val._const):
                s._set_def_val()

        if not postponed_init:
            self.finish_var_init(s)

        return s

    def finish_var_init(self, var: RtlSignal):
        hdl = self.extraVarsHdl

        if isinstance(var.def_val, RtlSignalBase) or var.def_val.vld_mask:
            a = HdlAssignmentContainer(var.def_val, var, virtual_only=True)
            hdl.append(self.toHdlAst.as_hdl_HdlAssignmentContainer(a))
        else:
            assert var._const or var.drivers, (var, var.def_val)

        as_hdl = self.toHdlAst.as_hdl_HdlSignalItem(var, declaration=True)

        for d in var.drivers:
            hdl.append(self.toHdlAst.as_hdl(d))

        hdl.append(as_hdl)

    def sort_hdl_declarations_first(self):
        self.extraVarsHdl.sort(key=lambda x: not isinstance(x, HdlIdDef))


class NoTmpVars():

    def create_var_cached(self, suggestedName, dtype, *args, **kwargs):
        raise NotImplementedError(
            "Can not create a tmp variable (%s of type %r) in this code section" % (suggestedName, dtype))

    def create_cached(self, suggestedName, dtype, *args, **kwargs):
        raise NotImplementedError(
            "Can not create a tmp variable (%s of type %r) in this code section" % (suggestedName, dtype))

