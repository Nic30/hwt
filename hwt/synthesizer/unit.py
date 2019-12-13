from hwt.doc_markers import internal
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkParams
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase
from hwt.synthesizer.interfaceLevel.propDeclrCollector import PropDeclrCollector
from hwt.synthesizer.interfaceLevel.unitImplHelpers import UnitImplHelpers, \
    _default_param_updater
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist


class Unit(UnitBase, PropDeclrCollector, UnitImplHelpers):
    """
    Container of the netlist with interfaces
    and internal hierarchical structure

    :cvar _serializeDecision: function to decide if Hdl object derived from
        this unit should be serialized or not, if None all is always serialized
    :cvar _PROTECTED_NAMES: set of names which can not be overridden
    :ivar _interfaces: all public interfaces
    :ivar _private_interfaces: all internal interfaces
        which are not accessible from outside of unit
    :ivar _units: all units defined on this obj
    :ivar _params: all params defined on this obj
    :ivar _parent: parent object (Unit instance)
    :ivar _lazyLoaded: container of rtl object which were lazy loaded
        in implementation phase (this object has to be returned
        from _toRtl of parent before it it's own objects)
    :ivar _targetPlatform: metainformations about target platform
    """

    _serializeDecision = None
    _PROTECTED_NAMES = set(["_PROTECTED_NAMES", "_interfaces",
                            "_units", "_params", "_parent",
                            "_lazyLoaded", "_ctx",
                            "_externInterf", "_targetPlatform"])

    def __init__(self):
        self._parent = None
        self._lazyLoaded = []
        self._ctx = RtlNetlist(self)

        self._loadConfig()

    @internal
    def _toRtl(self, targetPlatform: DummyPlatform):
        """
        synthesize all subunits, make connections between them,
        build entity and component for this unit
        """
        assert not self._wasSynthetised()

        self._targetPlatform = targetPlatform
        if not hasattr(self, "_name"):
            self._name = self._getDefaultName()

        for proc in targetPlatform.beforeToRtl:
            proc(self)

        self._ctx.params = self._buildParams()
        self._externInterf = []

        # prepare subunits
        for u in self._units:
            yield from u._toRtl(targetPlatform)

        for u in self._units:
            subUnitName = u._name
            u._signalsForMyEntity(self._ctx, "sig_" + subUnitName)

        # prepare signals for interfaces
        for i in self._interfaces:
            signals = i._signalsForInterface(self._ctx)
            if i._isExtern:
                self._externInterf.extend(signals)

        for proc in targetPlatform.beforeToRtlImpl:
            proc(self)
        self._loadMyImplementations()
        yield from self._lazyLoaded

        if not self._externInterf:
            raise IntfLvlConfErr(
                "Can not find any external interface for unit %s"
                "- unit without interfaces are not allowed"
                % self._name)

        for proc in targetPlatform.afterToRtlImpl:
            proc(self)

        yield from self._synthetiseContext(self._externInterf)
        self._checkArchCompInstances()

        for proc in targetPlatform.afterToRtl:
            proc(self)

    def _wasSynthetised(self):
        return self._ctx.synthesised

    @internal
    def _synthetiseContext(self, externInterf):
        # synthesize signal level context
        s = self._ctx.synthesize(
            self._name, externInterf, self._targetPlatform)
        self._entity = s[0]
        self._entity.__doc__ = self.__doc__
        self._entity.origin = self

        self._architecture = s[1]

        for intf in self._interfaces:
            if intf._isExtern:
                # reverse because other components
                # looks at this interface from outside
                intf._reverseDirection()

        # connect results of synthesized context to interfaces of this unit
        self._boundInterfacesToEntity(self._interfaces)
        yield from s

        # after synthesis clean up interface so this Unit object can be used elsewhere
        self._cleanAsSubunit()

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
        intf._signalsForInterface(self._ctx)

    @internal
    def _buildParams(self):
        # construct params for entity (generics)
        params = {}

        def addP(n: str, p: Param):
            if n in params:
                raise IntfLvlConfErr(
                    "Redefinition of generic/param '%s' while synthesis"
                    " old:%r, new:%r"
                    % (n, params[n], p))
            p.hdl_name = n
            params[n] = p

        def nameForNestedParam(p):
            n = ""
            node = p
            while node is not self:
                if n == "":
                    n = node._name
                else:
                    n = node._name + "_" + n
                node = node._parent

            return n

        # collect params of this unit
        discoveredParams = set()
        for p in self._params:
            discoveredParams.add(p)
            addP(p._name, p)

        # collect params from interfaces
        for intf in self._interfaces:
            for p in walkParams(intf, discoveredParams):
                n = nameForNestedParam(p)
                addP(n, p)

        return params

    def _getDefaultName(self):
        return self.__class__.__name__

    @internal
    def _checkArchCompInstances(self):
        cInstances = len(self._architecture.componentInstances)
        units = len(self._units)
        if cInstances != units:
            inRtl = set(
                map(lambda x: x.name, self._architecture.componentInstances))
            inIntf = set(map(lambda x: x._name + "_inst", self._units))
            if cInstances > units:
                raise IntfLvlConfErr(
                    "_toRtl unit(s) %s were found in rtl but were"
                    " not registered at %s"
                    % (str(inRtl - inIntf), self._name))
            elif cInstances < units:
                raise IntfLvlConfErr("_toRtl of %s: unit(s) %s were lost"
                                     % (self._name, str(inIntf - inRtl)))

    def _updateParamsFrom(self, otherObj,
                          updater=_default_param_updater,
                          exclude=None,
                          prefix=""):
        """
        :note: doc in
              :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        PropDeclrCollector._updateParamsFrom(self, otherObj,
                                             updater, exclude, prefix)
