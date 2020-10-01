from typing import List, Optional, Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._structural import HdlModuleDec, HdlModuleDef,\
    HdlCompInst
from hwt.code import If
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT
from hwt.hdl.value import HValue
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mark_visibility_of_signals_and_check_drivers import\
    markVisibilityOfSignalsAndCheckDrivers
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.remove_unconnected_signals import removeUnconnectedSignals
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NO_NOPVAL
from hwt.synthesizer.rtlLevel.statements_to_HdlStatementBlocks import\
    statements_to_HdlStatementBlocks
from hdlConvertorAst.hdlAst._expr import HdlValueId
from hwt.doc_markers import internal
from hwt.serializer.utils import HdlStatement_sort_key, RtlSignal_sort_key


@internal
def prepareEntity(ent, name, templateUnit):
    ent.name = name
    ent.generics.sort(key=lambda x: x.hdl_name)
    ent.ports.sort(key=lambda x: x.name)
    # copy names
    if templateUnit is not None:
        # sort in python is stable, ports and generic were added in same order
        # templateUnit should have generic and ports sorted
        for gp, gch in zip(templateUnit._entity.generics, ent.generics):
            gch.hdl_name = gp.hdl_name
        for pp, pch in zip(templateUnit._entity.ports, ent.ports):
            pch.name = pp.name



class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar ~.parent: optional parent for debug and late component inspection
    :ivar ~.signals: set of all signals in this context
    :ivar ~.statements: list of all statements which are connected to signals in this context
    :ivar ~.subUnits: is set of all units in this context
    :type ~.interfaces: Dict[RtlSignal, DIRECTION]
    :ivar ~.interfaces: initialized in create_HdlModuleDef
    :type ~.ent: HdlModuleDec
    :ivar ~.ent: initialized in create_HdlModuleDec
    :type ~.arch: HdlModuleDef
    :ivar ~.arch: initialized in create_HdlModuleDef
    :ivar ~.hdl_objs: The list of HDL objects which were produced by this instance
        usually contains HdlModudeleDef but may contain imports/globals etc.
    """

    def __init__(self, parent: Optional["Unit"]=None):
        self.parent = parent
        self.signals = set()
        self.statements = set()
        self.subUnits = set()
        self.interfaces = {}
        self.hdl_objs = []
        self.ent = None
        self.arch = None
        self._port_items = []

    def _try_cast_any_to_HdlType(self, v, dtype):
        if isinstance(v, RtlSignal):
            assert v._const, \
                "Initial value of register has to be constant"
            return v._auto_cast(dtype)
        elif isinstance(v, HValue):
            return v._auto_cast(dtype)
        elif isinstance(v, InterfaceBase):
            return v._sig
        else:
            return dtype.from_py(v)

        return None

    def sig(self, name, dtype=BIT, clk=None, syncRst=None,
            def_val=None, nop_val=NO_NOPVAL) -> Union[RtlSignal, RtlSyncSignal]:
        """
        Create new signal in this context

        :param clk: clk signal, if specified signal is synthesized
            as SyncSignal
        :param syncRst: synchronous reset signal
        :param def_val: default value used for reset and intialization
        :param nop_val: value used a a driver if signal is not driven by any driver
        """
        _def_val = self._try_cast_any_to_HdlType(def_val, dtype)
        if nop_val is not NO_NOPVAL:
            nop_val = self._try_cast_any_to_HdlType(nop_val, dtype)

        if clk is not None:
            s = RtlSyncSignal(self, name, dtype, _def_val, nop_val)
            if syncRst is not None and def_val is None:
                raise SigLvlConfErr(
                    "Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                       RtlSignal.__call__(s, _def_val)
                       ).Else(
                    RtlSignal.__call__(s, s.next)
                )
            else:
                r = [RtlSignal.__call__(s, s.next)]

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
                    "Signal %s has reset but has no clk" % name)
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
        removeUnconnectedSignals(self)
        markVisibilityOfSignalsAndCheckDrivers(self.signals, self.interfaces)

        for proc in target_platform.beforeHdlArchGeneration:
            proc(self)

        ns = store_manager.name_scope
        mdef = HdlModuleDef()
        mdef.dec = self.ent
        mdef.module_name = HdlValueId(self.ent.name, obj=self.ent)
        mdef.name = "rtl"

        processes = sorted(self.statements, key=HdlStatement_sort_key)
        processes = sorted(statements_to_HdlStatementBlocks(processes), key=HdlStatement_sort_key)

        # add signals, variables etc. in architecture
        for s in sorted((s for s in self.signals
                        if not s.hidden and
                        s not in self.interfaces.keys()),
                        key=RtlSignal_sort_key):
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
