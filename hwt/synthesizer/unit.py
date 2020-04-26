from hwt.doc_markers import internal
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase, InterfaceBase
from hwt.synthesizer.interfaceLevel.propDeclrCollector import PropDeclrCollector
from hwt.synthesizer.interfaceLevel.unitImplHelpers import UnitImplHelpers, \
    _default_param_updater
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hdlConvertor.hdlAst._structural import HdlComponentInst
from typing import Optional, List
from copy import copy
from hwt.hdl.portItem import HdlPortItem
from ipCorePackager.constants import DIRECTION


# from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkParams
class Unit(UnitBase, PropDeclrCollector, UnitImplHelpers):
    """
    Container of the netlist with interfaces
    and internal hierarchical structure

    :cvar ~._serializeDecision: function to decide if Hdl object derived from
        this unit should be serialized or not, if None all is always serialized
    :cvar ~._PROTECTED_NAMES: set of names which can not be overridden
    :ivar ~._interfaces: all public interfaces
    :type ~._interfaces: List[Interface]
    :ivar ~._private_interfaces: all internal interfaces
        which are not accessible from outside of unit
    :type _private_interfaces: List[Interface]
    :ivar ~._units: all units defined on this obj
    :type ~._units: List[Unit] 
    :ivar ~._params: all params defined on this obj
    :type ~._params: List[Param]
    :ivar ~._constraints: additional HW specifications
    :ivar ~._parent: parent object
    :type ~._parent: Optional[Unit]
    :ivar ~._lazyLoaded: container of rtl object which were lazy loaded
        in implementation phase (this object has to be returned
        from _toRtl of parent before it it's own objects)
    :ivar ~._shared_component_with: the other Unit instance which produces
        an exactly same component in HDL
    :attention if _shared_component_with is not None the body of this instance
        is not generated at all
        and the _shared_component_with is used instead
    :ivar ~._target_platform: metainformations about target platform
    :ivar ~._name: a name of this component
    :ivar ~._hdl_module_name: a name of hdl module for this compoennt
        (vhdl entity name, verilog module name)
    """

    _serializeDecision = None
    # properties which are used internally by this library
    _PROTECTED_NAMES = set([
        "_PROTECTED_NAMES",
        "_name", "_hdl_module_name",
        "_interfaces", "_private_interfaces",
        "_units", "_params", "_parent", "_constraints",
        "_lazyLoaded", "_ctx", "_shared_component_with",
        "_target_platform", "_store_manager",
    ])

    def __init__(self):
        self._parent = None
        self._name = None
        self._shared_component_with = None
        self._hdl_module_name = None
        self._lazyLoaded = []
        self._ctx = RtlNetlist(self)
        self._constraints = []
        self._loadConfig()

    @internal
    def _loadInterface(self, i, isExtern):
        i._loadDeclarations()
        i._setAsExtern(isExtern)

    @internal
    def _loadDeclarations(self):
        """
        Load all declarations from _decl() method, recursively
        for all interfaces/units.
        """
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        if not hasattr(self, "_private_interfaces"):
            self._private_interfaces = []
        if not hasattr(self, "_units"):
            self._units = []
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None
        for i in self._interfaces:
            self._loadInterface(i, True)

        # if I am a unit load subunits
        for u in self._units:
            u._loadDeclarations()

    @internal
    def _registerIntfInImpl(self, iName, intf):
        """
        Register interface in implementation phase
        """
        self._registerInterface(iName, intf, isPrivate=True)
        self._loadInterface(intf, False)
        intf._signalsForInterface(self._ctx, None, self._store_manager.name_scope)

    def _getDefaultName(self) -> str:
        return self.__class__.__name__

    def _get_hdl_doc(self) -> Optional[str]:
        if self.__doc__ is not Unit.__doc__:
            return self.__doc__

    @internal
    def _toRtl(self, target_platform: DummyPlatform,
               store_manager: "StoreManager"):
        """
        synthesize all subunits, make connections between them,
        build entity and component for this unit
        """
        if self._hdl_module_name is None:
            self._hdl_module_name = self._getDefaultName()
        if self._name is None:
            self._name = self._getDefaultName()
        self._target_platform = target_platform
        self._store_manager = store_manager
        do_serialize_this, replacement = store_manager.filter.do_serialize(self)
        if replacement is not None:
            assert not do_serialize_this
            assert len(self._interfaces) == len(replacement._interfaces), \
                "No lazy loaded interfaces declared in _impl()"
            copy_HdlModuleDec(replacement, self)
            yield False, self
            self._cleanAsSubunit()
            self._units = None
            self._private_interfaces = None
            self._shared_component_with = replacement
            return

        for proc in target_platform.beforeToRtl:
            proc(self)

        mdec = self._ctx.create_HdlModuleDec(
            self._hdl_module_name, store_manager, self._params)
        mdec.origin = self
        mdec.doc = self._get_hdl_doc()

        # prepare signals for interfaces
        for i in self._interfaces:
            if i._isExtern:
                ei = self._ctx.interfaces
            else:
                ei = None
            # we are reversing direction because we are looking
            # at the interface from inside of component
            i._signalsForInterface(
                self._ctx, ei,
                store_manager.name_scope, reverse_dir=True)
        store_manager.hierarchy_pop(mdec)

        if do_serialize_this:
            # prepare subunits
            for u in self._units:
                yield from u._toRtl(target_platform, store_manager)

            # now every sub unit has a HdlModuleDec prepared
            for u in self._units:
                subUnitName = u._name
                u._signalsForSubUnitEntity(self._ctx, "sig_" + subUnitName)

            for proc in target_platform.beforeToRtlImpl:
                proc(self)

        store_manager.hierarchy_push(mdec)
        if do_serialize_this:
            self._loadImpl()
            yield from self._lazyLoaded

            if not self._ctx.interfaces:
                raise IntfLvlConfErr(
                    "Can not find any external interface for unit %s"
                    "- unit without interfaces are not synthetisable"
                    % self._name)

        for proc in target_platform.afterToRtlImpl:
            proc(self)

        mdec.params.sort(key=lambda x: x.name)
        mdec.ports.sort(key=lambda x: x.name)
        if do_serialize_this:
            # synthesize signal level context
            mdef = self._ctx.create_HdlModuleDef(target_platform, store_manager)
            mdef.origin = self
            for intf in self._interfaces:
                if intf._isExtern:
                    # reverse because other components
                    # looks at this interface from the outside
                    intf._reverseDirection()
            store_manager.write(mdef)
        yield True, self

        # after synthesis clean up interface so this Unit object can be used elsewhere
        self._cleanAsSubunit()
        if do_serialize_this:
            Unit_checkCompInstances(self)

        for proc in target_platform.afterToRtl:
            proc(self)
        store_manager.hierarchy_pop(mdec)

    def _updateParamsFrom(self, otherObj,
                          updater=_default_param_updater,
                          exclude=None,
                          prefix=""):
        """
        :note: doc in
            :func:`hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        PropDeclrCollector._updateParamsFrom(self, otherObj,
                                             updater, exclude, prefix)


@internal
def Unit_checkCompInstances(u: Unit):
    cInstances = [o for o in u._ctx.arch.objs
                  if isinstance(o, HdlComponentInst)]
    cInst_cnt = len(cInstances)
    unit_cnt = len(u._units)
    if cInst_cnt != unit_cnt:
        inRtl = set(x.name for x in cInstances)
        inIntf = set(x._name for x in u._units)
        if cInst_cnt > unit_cnt:
            raise IntfLvlConfErr(
                "%s, %s: unit(s) were found in HDL but were"
                " not registered %s" % (
                   u.__class__.__name__, u._name,
                   u._getstr(inRtl - inIntf)))
        elif cInst_cnt < unit_cnt:
            raise IntfLvlConfErr(
                "%s, %s: _toRtl: unit(s) are missing in produced HDL %s" % (
                    u._name, u.__class__.__name__,
                    str(inIntf - inRtl)))


def copy_HdlModuleDec_interface(orig_i: InterfaceBase, new_i: InterfaceBase,
                                ports: List[HdlPortItem], new_u: Unit):
    new_i._direction = orig_i._direction
    if orig_i._hdl_port is not None:
        s = orig_i._sigInside
        pi = copy(orig_i._hdl_port)
        pi.unit = new_u
        ports.append(pi)
        d = pi.direction
        if d == DIRECTION.OUT:
            pi.dst = None
        elif d == DIRECTION.IN:
            pi.src = None
        else:
            raise NotImplementedError(d)
        new_i._hdl_port = pi
        new_i._sigInside = s
    else:
        for i in orig_i._interfaces:
            n_i = getattr(new_i, i._name)
            copy_HdlModuleDec_interface(i, n_i, ports, new_u)


def copy_HdlModuleDec(orig_u: Unit, new_u: Unit):
    assert not new_u._ctx.statements
    assert not new_u._ctx.interfaces
    assert not new_u._ctx.signals
    assert new_u._ctx.ent is None

    new_u._hdl_module_name = orig_u._hdl_module_name
    e = new_u._ctx.ent = copy(orig_u._ctx.ent)

    params = []
    param_by_name = {p._name: p for p in new_u._params}
    for p in e.params:
        new_p_def = copy(p)
        old_p = new_p_def.origin = param_by_name[p.origin._name]
        old_p.hdl_name = p.origin.hdl_name
        new_p_def.value = old_p.get_hdl_value()
        params.append(new_p_def)
    e.params = params

    e.ports = []
    for oi, ni in zip(orig_u._interfaces, new_u._interfaces):
        if oi._isExtern:
            copy_HdlModuleDec_interface(oi, ni, e.ports, new_u)

    # params should be already sorted
    # e.params.sort(key=lambda x: x.name)
    e.ports.sort(key=lambda x: x.name)
