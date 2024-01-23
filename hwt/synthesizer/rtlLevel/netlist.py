from typing import List, Optional, Union, Dict, Set

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId
from hdlConvertorAst.hdlAst._structural import HdlModuleDec, HdlModuleDef, \
    HdlCompInst
from hwt.code import If
from hwt.doc_markers import internal
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue
from hwt.serializer.utils import HdlStatement_sort_key, RtlSignal_sort_key
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NOT_SPECIFIED
from hwt.synthesizer.rtlLevel.rtlSyncSignal import RtlSyncSignal
from hwt.synthesizer.rtlLevel.statements_to_HdlStmCodeBlockContainers import statements_to_HdlStmCodeBlockContainers
from ipCorePackager.constants import DIRECTION


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar ~.parent: optional parent for debug and late component inspection
    :ivar ~.signals: set of all signals in this context
    :ivar ~.statements: list of all statements which are connected to signals in this context
    :ivar ~.subUnits: is set of all units in this context
    :ivar ~.interfaces: initialized in create_HdlModuleDef
    :ivar ~.ent: initialized in create_HdlModuleDec
    :ivar ~.arch: initialized in create_HdlModuleDef
    """

    def __init__(self, parent: Optional["Unit"]=None):
        self.parent = parent
        self.signals: Set[RtlSignal] = set()
        self.statements: Set[HdlStatement] = set()
        self.subUnits: Set["Unit"] = set()
        self.interfaces: Dict[RtlSignal, DIRECTION] = {}
        self.ent: Optional[HdlModuleDec] = None
        self.arch: Optional[HdlModuleDef] = None

    def sig(self, name: str, dtype=BIT, clk=None, syncRst=None,
            def_val=None, nop_val=NOT_SPECIFIED, nextSig=NOT_SPECIFIED) -> Union[RtlSignal, RtlSyncSignal]:
        """
        Create new signal in this context

        :param clk: clock signal, if specified signal is synthesized
            as RtlSyncSignal
        :param syncRst: synchronous reset signal
        :param def_val: a default value used for reset and initialization
        :param nop_val: a value which is used to drive the signal if there is no other drive
            (used to prevent latches and to specify default values for unconnected signals)
        :param nextSig: the signal which should be used as "next" signal for this register
            if is not specified the new signal is generated. (Next signal holds value which should be in register in next clk.)
        
        """
        _def_val = _try_cast_any_to_HValue(def_val, dtype, True)
        if nop_val is not NOT_SPECIFIED:
            nop_val = _try_cast_any_to_HValue(nop_val, dtype, False)

        if clk is not None:
            s = RtlSyncSignal(self, name, dtype,
                              _def_val if isinstance(_def_val, HValue) else dtype.from_py(None),
                              nop_val,
                              nextSig)
            if syncRst is not None and def_val is None:
                raise SigLvlConfErr(
                    "Probably forgotten default value on sync signal %s", name)
            # dst_resolve_fn is overridden because default assign would assign to the "next" signal
            if syncRst is not None:
                r = If(syncRst._isOn(),
                       s(_def_val, dst_resolve_fn=lambda x: x)
                    ).Else(
                       s(s.next, dst_resolve_fn=lambda x: x)
                    )
            else:
                r = [
                    s(s.next, dst_resolve_fn=lambda x: x)
                ]

            if isinstance(clk, (InterfaceBase, RtlSignal)):
                clk_trigger = clk._onRisingEdge()
            else:
                # has to be tuple of (clk_sig, AllOps.RISING/FALLING_EDGE)
                clk, clk_edge = clk
                if clk_edge is AllOps.RISING_EDGE:
                    clk_trigger = clk._onRisingEdge()
                elif clk_edge is AllOps.FALLING_EDGE:
                    clk_trigger = clk._onRisingEdge()
                else:
                    raise ValueError(
                        "Invalid clock edge specification", clk_edge)

            If(clk_trigger,
               r
            )
        else:
            if syncRst:
                raise SigLvlConfErr(
                    f"Signal {name:s} has reset but has no clk")
            if nextSig is not NOT_SPECIFIED:
                raise SigLvlConfErr(
                    f"Signal {name:s} has nextSig which is used for next register value, but has no clock and thus is not a register.")

            assert isinstance(_def_val, HValue) or (isinstance(_def_val, RtlSignal) and _def_val._const), (_def_val, "The default value needs to be constant")
            s = RtlSignal(self, name, dtype, def_val=_def_val, nop_val=nop_val)

        return s

    def create_HdlModuleDec(self, name: str,
                            store_manager: "StoreManager",
                            params: List[Param]):
        """
        Generate a module header (entity) for this module
        """
        self.ent = ent = HdlModuleDec()
        ent.name = store_manager.name_scope.checked_name(name, ent)
        ns = store_manager.hierarchy_push(ent)
        # create generics
        for p in sorted(params, key=lambda x: x._name):
            hdl_val = p.get_hdl_value()
            v = HdlIdDef()
            v.origin = p
            v.name = p.hdl_name = ns.checked_name(p._name, p)
            v.type = hdl_val._dtype
            v.value = hdl_val
            ent.params.append(v)

        return ent

    def create_HdlModuleDef(self,
                            target_platform: DummyPlatform,
                            store_manager: "StoreManager"):
        """
        Generate a module body (architecture) for this module

        * Resolve name collisions
        * Convert netlist representation to HdlProcesses
        * Remove unconnected
        * Mark visibility of signals
        """
        for proc in target_platform.beforeHdlArchGeneration:
            proc(self)

        ns = store_manager.name_scope
        mdef = HdlModuleDef()
        mdef.dec = self.ent
        mdef.module_name = HdlValueId(self.ent.name, obj=self.ent)
        mdef.name = "rtl"

        processes = sorted(self.statements, key=HdlStatement_sort_key)
        processes = sorted(statements_to_HdlStmCodeBlockContainers(processes), key=HdlStatement_sort_key)

        # add signals, variables, etc. in architecture
        for s in sorted((s for s in self.signals
                        if not s.hidden and
                        s not in self.interfaces.keys()),
                        key=RtlSignal_sort_key):
            s: RtlSignal
            assert s.ctx is self, ("RtlSignals in this context must know that they are in this context", s)
            v = HdlIdDef()
            v.origin = s
            s.name = v.name = ns.checked_name(s.name, s)
            v.type = s._dtype
            v.value = s.def_val
            v.is_const = s._const
            mdef.objs.append(v)

        for p in processes:
            p.name = ns.checked_name(p.name, p)
        mdef.objs.extend(processes)
        # instantiate subUnits in architecture
        for u in self.subUnits:
            ci = HdlCompInst()
            ci.origin = u
            ci.module_name = HdlValueId(u._ctx.ent.name, obj=u._ctx.ent)
            ci.name = HdlValueId(ns.checked_name(u._name + "_inst", ci), obj=u)
            e = u._ctx.ent

            ci.param_map.extend(e.params)
            ci.port_map.extend(e.ports)

            mdef.objs.append(ci)

        self.arch = mdef
        return mdef

    def getDebugScopeName(self):
        scope = []
        p = self.parent
        while p is not None:
            scope.append(p._name)
            try:
                p = p._parent
            except AttributeError:
                break

        return ".".join(reversed(scope))


@internal
def _try_cast_any_to_HValue(v, dtype: HdlType, require_const: bool):
    if isinstance(v, RtlSignal):
        assert not require_const or v._const, \
            "Initial value of signal has to be a constant"
        return v._auto_cast(dtype)
    elif isinstance(v, HValue):
        return v._auto_cast(dtype)
    elif isinstance(v, InterfaceBase):
        return v._sig
    else:
        return dtype.from_py(v)
