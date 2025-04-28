from copy import copy
from natsort.natsort import natsorted
from typing import Optional, List, Dict, Tuple, Set, Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._structural import HdlCompInst, HdlModuleDec
from hwt.doc_markers import internal
from hwt.hdl.portItem import HdlPortItem
from hwt.mainBases import HwIOBase
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.hwModuleImplHelpers import HwModuleImplHelpers, \
    _default_param_updater
from hwt.synthesizer.interfaceLevel.propDeclrCollector import PropDeclrCollector
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from ipCorePackager.constants import DIRECTION


class HdlConstraintList(list):
    """
    Containers of hw design constraints
    """
    pass


class HwModule(PropDeclrCollector, HwModuleImplHelpers):
    """
    Objects of this class are representation of design in hwt HCL.
    This object is a container of the netlist with interfaces
    and internal hierarchical structure.

    :cvar ~._serializeDecision: function to decide if HDL object derived from
        this unit should be serialized or not, if None all is always serialized
    :cvar ~._PROTECTED_NAMES: set of names which can not be overridden
    :ivar ~._hwIOs: all public interfaces
    :type ~._hwIOs: List[HwIO]
    :ivar ~._private_hwIOs: all internal interfaces
        which are not accessible from outside of unit
    :type _private_hwIOs: List[HwIO]
    :ivar ~._subHwModules: all units defined on this object
    :type ~._subHwModules: List[HwModule]
    :ivar ~._hwParams: all params defined on this object
    :type ~._hwParams: List[HwParam]
    :ivar ~._constraints: additional HW specifications
    :ivar ~._parent: parent object
    :type ~._parent: Optional[HwModule]
    :ivar ~._lazy_loaded: container of RTL object which were lazy loaded
        in implementation phase (this object has to be returned
        from :func:`~._to_rtl` of parent before it it's own objects)
    :ivar ~._shared_component_with: Optional tuple of the other :class:`hwt.hwModule.HwModule` instance
        which produces an exactly same component in HDL and interface
        signal map current to shared and shared to current
    :type ~._shared_component_with: Optional[Tuple[HwModule,
        Dict[Interface, Interface],
        Dict[Interface, Interface]]]
    :attention: if :func:`~._shared_component_with` is not None the body
        of this instance is not generated at all
        and the component from :func:`~._shared_component_with` is used instead
    :ivar ~._target_platform: meta-informations about target platform
    :ivar ~._name: a name of this component
    :ivar ~._hdl_module_name: a name of HDL module for this component
        (vhdl entity name, Verilog module name)
    """

    _serializeDecision = None
    # properties which are used internally by this library
    _PROTECTED_NAMES = {
        "_PROTECTED_NAMES",
        "_name", "_hdl_module_name",
        "_hwIOs", "_private_hwIOs",
        "_units", "_hwParams", "_parent", "_constraints",
        "_lazy_loaded", "_rtlCtx", "_shared_component_with",
        "_target_platform", "_store_manager",
    }

    def __init__(self, hdlName:Optional[str]=None):
        self._parent: Optional[HwModule] = None
        self._name: Optional[str] = None
        self._shared_component_with = None
        self._hdl_module_name: Optional[str] = None
        assert hdlName is None or isinstance(hdlName, str), hdlName
        self._hdlNameOverride = hdlName
        self._lazy_loaded: List[Union[HwModule, HwIOBase]] = []
        self._rtlCtx = RtlNetlist(self)
        self._constraints = HdlConstraintList()
        self._loadConfig()

    @internal
    def _loadHwIODeclarations(self, hwIO: HwIOBase, isExtern: bool):
        hwIO._loadHwDeclarations()
        hwIO._setAsExtern(isExtern)

    @internal
    def _loadHwDeclarations(self):
        """
        Load all declarations from _decl() method, recursively
        for all interfaces/units.
        """
        if not hasattr(self, "_hwIOs"):
            self._hwIOs = []
        if not hasattr(self, "_private_hwIOs"):
            self._private_hwIOs = []
        if not hasattr(self, "_subHwModules"):
            self._subHwModules = []
        self._setAttrListener = self._declrCollector
        self.hwDeclr()
        self._setAttrListener = None
        for hio in self._hwIOs:
            self._loadHwIODeclarations(hio, True)

        # if I am a unit load subunits
        for u in self._subHwModules:
            u._loadHwDeclarations()

    @internal
    def _registerHwIOInHwImpl(self, hwIOName, hwIO):
        """
        Register interface in implementation phase
        """
        self._registerHwIO(hwIOName, hwIO, isPrivate=True)
        self._loadHwIODeclarations(hwIO, False)
        hwIO._signalsForHwIO(
            self._rtlCtx, None, self._store_manager.name_scope)

    def _getDefaultName(self) -> str:
        return self.__class__.__name__

    def _get_hdl_doc(self) -> Optional[str]:
        if self.__doc__ is not HwModule.__doc__:
            return self.__doc__

    @internal
    def _to_rtl(self, target_platform: DummyPlatform,
                store_manager: "StoreManager", add_param_asserts=True):
        """
        synthesize all subunits, make connections between them,
        build verilog like module/vhdl like entity and architecture for this unit
        """
        if self._hdl_module_name is None:
            if self._hdlNameOverride:
                self._hdl_module_name = self._hdlNameOverride
            else:
                self._hdl_module_name = self._getDefaultName()
        if self._name is None:
            self._name = self._getDefaultName()
        self._target_platform = target_platform
        self._store_manager = store_manager
        do_serialize_this, replacement = store_manager.filter.do_serialize(
            self)
        if replacement is not None:
            assert not do_serialize_this
            assert len(self._hwIOs) == len(replacement._hwIOs), \
                "No lazy loaded interfaces declared in hwImpl()"
            copy_HdlModuleDec(replacement, self)
            yield False, self
            self._cleanThisSubunitRtlSignals()
            self._subHwModules = None
            self._private_hwIOs = None
            hwIO_map_repl_to_self = sharedCompBuildHwIOMap(
                replacement, self)
            hwIO_map_self_to_repl = {
                v: k
                for k, v in hwIO_map_repl_to_self.items()}
            self._shared_component_with = replacement, \
                hwIO_map_self_to_repl, hwIO_map_repl_to_self
            return

        for proc in target_platform.beforeToRtl:
            proc(self)

        mdec = self._rtlCtx.create_HdlModuleDec(
            self._hdl_module_name, store_manager, self._hwParams)
        mdec.origin = self
        mdec.doc = self._get_hdl_doc()

        # prepare signals for interfaces
        for hwIO in self._hwIOs:
            if hwIO._isExtern:
                ei = self._rtlCtx.hwIOs
            else:
                ei = None
            # we are reversing direction because we are looking
            # at the interface from inside of component
            hwIO._signalsForHwIO(
                self._rtlCtx, ei,
                store_manager.name_scope, reverse_dir=True)
        store_manager.hierarchy_pop(mdec)

        if do_serialize_this:
            # prepare subunits
            for sm in self._subHwModules:
                yield from sm._to_rtl(target_platform, store_manager)

            # now every sub unit has a HdlModuleDec prepared
            for sm in self._subHwModules:
                subHwModuleName = sm._name
                sm._signalsForSubHwModuleEntity(self._rtlCtx, "sig_" + subHwModuleName)

            for proc in target_platform.beforeToRtlImpl:
                proc(self)

        try:
            store_manager.hierarchy_push(mdec)
            if do_serialize_this:
                self._loadImpl()
                yield from self._lazy_loaded

                if not self._rtlCtx.hwIOs:
                    raise IntfLvlConfErr(
                        "Can not find any external interface for unit %s"
                        "- unit without interfaces are not synthesisable"
                        % self._name)

            for proc in target_platform.afterToRtlImpl:
                proc(self)

            mdec.params[:] = natsorted(mdec.params, key=lambda x: x.name)
            mdec.ports[:] = natsorted(mdec.ports, key=lambda x: x.name)
            if do_serialize_this:
                # synthesize signal level context
                mdef = self._rtlCtx.create_HdlModuleDef(
                    target_platform, store_manager)
                mdef.origin = self

            for hwIO in self._hwIOs:
                if hwIO._isExtern:
                    # reverse because other components
                    # looks at this interface from the outside
                    hwIO._reverseDirection()

            if do_serialize_this:
                if add_param_asserts and self._hwParams:
                    mdef.objs.extend(store_manager.as_hdl_ast._as_hdl_HdlModuleDef_param_asserts(mdec))
                store_manager.write(mdef)

            yield True, self

            # after synthesis clean up interface so this :class:`hwt.hwModule.HwModule` object can be
            # used elsewhere
            self._cleanThisSubunitRtlSignals()
            if do_serialize_this:
                self._checkCompInstances()

            for proc in target_platform.afterToRtl:
                proc(self)
        finally:
            store_manager.hierarchy_pop(mdec)

    def _updateHwParamsFrom(self, otherObj: PropDeclrCollector,
                          updater=_default_param_updater,
                          exclude: Optional[Tuple[Set[str], Set[str]]]=None,
                          prefix=""):
        """
        :note: doc in
            :func:`hwt.synthesizer.interfaceLevel.propDeclCollector._updateHwParamsFrom`
        """
        return PropDeclrCollector._updateHwParamsFrom(self, otherObj,
                                                    updater, exclude, prefix)

    @internal
    def _checkCompInstances(self):
        cInstances = [o for o in self._rtlCtx.hwModDef.objs
                      if isinstance(o, HdlCompInst)]
        cInst_cnt = len(cInstances)
        unit_cnt = len(self._subHwModules)
        if cInst_cnt != unit_cnt:
            # resolve the error message
            inRtl = set(x.name for x in cInstances)
            inHwIO = set(x._name for x in self._subHwModules)
            cls_name = self.__class__.__name__
            if cInst_cnt > unit_cnt:
                diff = inRtl - inHwIO
                raise IntfLvlConfErr(
                    f"{cls_name:s}, {self._name:s}: unit(s) were found in HDL but were"
                    f" not registered {diff}")
            else:
                assert cInst_cnt < unit_cnt
                diff = inHwIO - inRtl
                raise IntfLvlConfErr(
                    f"{cls_name:s}, {self._name:s}: _to_rtl: unit(s) are missing in produced HDL {diff}")


def copy_HdlModuleDec_HwIO(orig_io: HwIOBase, new_io: HwIOBase,
                           ports: List[HdlPortItem], new_m: HwModule):
    new_io._direction = orig_io._direction
    if orig_io._hdlPort is not None:
        s = orig_io._sigInside
        assert s is not None, (
            "the component which shares a body with this component"
            " is actually some parent of this component")
        pi = copy(orig_io._hdlPort)
        pi.module = new_m
        ports.append(pi)
        d = pi.direction
        if d == DIRECTION.OUT:
            pi.dst = None
        elif d == DIRECTION.IN:
            pi.src = None
        else:
            raise NotImplementedError(d)
        new_io._hdlPort = pi
        new_io._sigInside = s
    else:
        for hwIO in orig_io._hwIOs:
            n_i = getattr(new_io, hwIO._name)
            copy_HdlModuleDec_HwIO(hwIO, n_i, ports, new_m)


def copy_HdlModuleDec(orig_m: HwModule, new_m: HwModule):
    assert not new_m._rtlCtx.statements
    assert not new_m._rtlCtx.hwIOs
    assert not new_m._rtlCtx.signals
    assert new_m._rtlCtx.hwModDec is None

    new_m._hdl_module_name = orig_m._hdl_module_name
    hwModDec = new_m._rtlCtx.hwModDec = copy(orig_m._rtlCtx.hwModDec)
    hwModDec: HdlModuleDec

    params = []
    param_by_name = {p._name: p for p in new_m._hwParams}
    for p in hwModDec.params:
        p: HdlIdDef
        new_p_def = copy(p)
        old_p = new_p_def.origin = param_by_name[p.origin._name]
        old_p._name = p.origin._name
        new_p_def.value = old_p.get_hdl_value()
        params.append(new_p_def)

    hwModDec.params = params

    hwModDec.ports = []
    for hwO, hwI in zip(orig_m._hwIOs, new_m._hwIOs):
        if hwO._isExtern:
            copy_HdlModuleDec_HwIO(hwO, hwI, hwModDec.ports, new_m)

    # params should be already sorted
    # hwModDec.params[:] = natsorted(hwModDec.params, key=lambda x: x.name)
    hwModDec.ports[:] = natsorted(hwModDec.ports, key=lambda x: x.name)


def _sharedCompBuildHwIOMapList(replacement: List[HwIOBase],
                                          substituted: List[HwIOBase],
                                          res: Dict[HwIOBase, HwIOBase]):
    assert len(replacement) == len(substituted)
    for r, s in zip(replacement, substituted):
        assert r._name == s._name, (r._name, s._name)
        res[r] = s
        if r._hwIOs:
            _sharedCompBuildHwIOMapList(
                r._hwIOs, s._hwIOs, res)


def sharedCompBuildHwIOMap(replacement_m: HwModule, substituted_m: HwModule):
    """
    Build a dictionary which maps
    interface of replacement_m to interface of substituted_m
    """
    res = {}
    _sharedCompBuildHwIOMapList(
        replacement_m._hwIOs, substituted_m._hwIOs, res)
    return res
