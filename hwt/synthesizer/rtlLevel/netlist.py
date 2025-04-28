from typing import List, Optional, Union, Dict, Set, Type

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId
from hdlConvertorAst.hdlAst._structural import HdlModuleDec, HdlModuleDef, \
    HdlCompInst
from hwt.code import If
from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.hdlType import HdlType
from hwt.hwParam import HwParam
from hwt.mainBases import HwIOBase
from hwt.serializer.utils import HdlStatement_sort_key, RtlSignal_sort_key
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.rtlLevel.rtlNetlistPass import RtlNetlistPass
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, CREATE_NEXT_SIGNAL
from hwt.synthesizer.rtlLevel.statements_to_HdlStmCodeBlockContainers import statements_to_HdlStmCodeBlockContainers
from ipCorePackager.constants import DIRECTION


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar ~.parent: optional parent for debug and late component inspection
    :ivar ~.signals: set of all signals in this context
    :ivar ~.statements: list of all statements which are connected to signals in this context
    :ivar ~.subHwModules: is set of all units in this context
    :ivar ~.hwIOs: initialized in create_HdlModuleDef
    :ivar ~.hwModDec: initialized in create_HdlModuleDec
    :ivar ~.hwModDef: initialized in create_HdlModuleDef
    """

    def __init__(self, parent: Optional["HwModule"]=None):
        self.parent = parent
        self.signals: Set[RtlSignal] = set()
        self.statements: Set[HdlStatement] = set()
        self.subHwModules: Set["HwModule"] = set()
        self.hwIOs: Dict[RtlSignal, DIRECTION] = {}
        self.hwModDec: Optional[HdlModuleDec] = None
        self.hwModDef: Optional[HdlModuleDef] = None

    def sig(self, name: str, dtype=BIT, clk=None, syncRst=None,
            def_val=None, nop_val=NOT_SPECIFIED, nextSig=NOT_SPECIFIED) -> Union[RtlSignal, HwIOBase]:
        """
        Create new signal in this context

        :param clk: clock signal
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
        
        signalCls: Type[RtlSignal] = dtype.getRtlSignalCls()
        if clk is not None:
            if nextSig is not None and isinstance(nextSig, HwIOBase):
                nextSig = nextSig._sig
            s = signalCls(self, name, dtype,
                          _def_val if isinstance(_def_val, HConst) else dtype.from_py(None),
                          nop_val,
                          next_signal=CREATE_NEXT_SIGNAL if nextSig is NOT_SPECIFIED else nextSig)
            if syncRst is not None and def_val is None:
                raise SigLvlConfErr(
                    "Probably forgotten default value on sync signal %s", name)
            # dst_resolve_fn is overridden because default assign would assign to the "next" signal
            if syncRst is not None:
                r = If(syncRst._isOn(),
                       s(_def_val, dst_resolve_fn=lambda x: x)
                    ).Else(
                       s(s._rtlNextSig, dst_resolve_fn=lambda x: x)
                    )
            else:
                r = [
                    s(s._rtlNextSig, dst_resolve_fn=lambda x: x)
                ]

            if isinstance(clk, (HwIOBase, RtlSignal)):
                clk_trigger = clk._onRisingEdge()
            else:
                # has to be tuple of (clk_sig, HwtOps.RISING/FALLING_EDGE)
                clk, clk_edge = clk
                if clk_edge is HwtOps.RISING_EDGE:
                    clk_trigger = clk._onRisingEdge()
                elif clk_edge is HwtOps.FALLING_EDGE:
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

            assert isinstance(_def_val, HConst) or (isinstance(_def_val, RtlSignal) and _def_val._const), (_def_val, "The default value needs to be constant")
            s = signalCls(self, name, dtype, def_val=_def_val, nop_val=nop_val)

        return s

    def create_HdlModuleDec(self, name: str,
                            store_manager: "StoreManager",
                            params: List[HwParam]):
        """
        Generate a module header (entity) for this module
        """
        self.hwModDec = hwModDec = HdlModuleDec()
        hwModDec.name = store_manager.name_scope.checked_name(name, hwModDec)
        ns = store_manager.hierarchy_push(hwModDec)
        # create generics
        for p in sorted(params, key=lambda x: x._name):
            hdl_val = p.get_hdl_value()
            v = HdlIdDef()
            v.origin = p
            # sanitize param name
            v.name = p._name = ns.checked_name(p._name, p)
            v.type = hdl_val._dtype
            v.value = hdl_val
            hwModDec.params.append(v)

        return hwModDec

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
        for optPass in target_platform.beforeHdlArchGeneration:
            optPass: RtlNetlistPass
            optPass.runOnRtlNetlist(self)

        ns = store_manager.name_scope
        mdef = HdlModuleDef()
        mdef.dec = self.hwModDec
        mdef.module_name = HdlValueId(self.hwModDec.name, obj=self.hwModDec)
        mdef.name = "rtl"

        processes = sorted(self.statements, key=HdlStatement_sort_key)
        processes = sorted(statements_to_HdlStmCodeBlockContainers(processes), key=HdlStatement_sort_key)

        # add signals, variables, etc. in architecture
        for s in sorted((s for s in self.signals
                        if not s._isUnnamedExpr and
                        s not in self.hwIOs.keys()),
                        key=RtlSignal_sort_key):
            s: RtlSignal
            assert s._rtlCtx is self, ("RtlSignals in this context must know that they are in this context", s)
            v = HdlIdDef()
            v.origin = s
            v.name = s._name = ns.checked_name(s._name, s)
            v.type = s._dtype
            v.value = s.def_val
            v.is_const = s._const
            mdef.objs.append(v)

        for p in processes:
            p: HdlStmCodeBlockContainer
            p.name = ns.checked_name(p.name, p)

        mdef.objs.extend(processes)
        # instantiate subModules in architecture
        for sm in self.subHwModules:
            ci = HdlCompInst()
            ci.origin = sm
            ci.module_name = HdlValueId(sm._rtlCtx.hwModDec.name, obj=sm._rtlCtx.hwModDec)
            ci.name = HdlValueId(ns.checked_name(sm._name + "_inst", ci), obj=sm)
            hwModDec = sm._rtlCtx.hwModDec

            ci.param_map.extend(hwModDec.params)
            ci.port_map.extend(hwModDec.ports)

            mdef.objs.append(ci)

        self.hwModDef = mdef
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
    elif isinstance(v, HConst):
        return v._auto_cast(dtype)
    elif isinstance(v, HwIOBase):
        return v._sig
    else:
        return dtype.from_py(v)
