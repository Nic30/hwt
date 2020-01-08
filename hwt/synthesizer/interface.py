from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION, INTF_DIRECTION
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.interfaceUtils.directionFns import \
    InterfaceDirectionFns
from hwt.synthesizer.interfaceLevel.interfaceUtils.implDependent import\
    InterfaceceImplDependentFns
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.propDeclrCollector import\
    PropDeclrCollector
from hwt.synthesizer.vectorUtils import fitTo


def _default_param_updater(self, myP, parentPval):
    myP.set_value(parentPval)


class Interface(InterfaceBase, InterfaceceImplDependentFns,
                PropDeclrCollector, InterfaceDirectionFns):
    """
    Base class for all interfaces in interface synthesizer

    :cvar _NAME_SEPARATOR: separator for nested interface names
    :ivar _params: [] of parameter
    :ivar _interfaces: [] sub interfaces
    :ivar _name: name assigned during synthesis
    :ivar _parent: parent object (Unit or Interface instance)
    :ivar _isExtern: If true synthesizer sets it as external port of unit
    :ivar _associatedClk: clock Signal (interface) associated with
        this interface if is none simulation agent try to search it on parent
    :ivar _associatedRst: rst(_n) Signal (interface) associated
        with this interface if is none simulation agent try to search
        it on parent

    :note: only interfaces without _interfaces have

    :ivar _sig: rtl level signal instance
    :ivar _sigInside: _sig after toRtl conversion is made
        (after toRtl conversion _sig is signal for parent unit
        and _sigInside is signal in original unit, this separates process
        of translating units)
    :ivar _boundedEntityPort: entityPort for which was this interface created
    :ivar _boundedSigLvlUnit: RTL unit for which was this interface created


    Agenda of direction

    :ivar _masterDir: specifies which direction has this interface at master
    :ivar _direction: means actual direction of this interface resolved
        by its drivers
    :ivar _ctx: rtl netlist context of all signals and params
        on this interface after interface is registered on parent _ctx
        is merged

    Agenda of simulations

    :ivar _ag: agent object connected to this interface
        (initialized only before simultion)
    """

    _NAME_SEPARATOR = "_"

    def __init__(self, masterDir=DIRECTION.OUT,
                 loadConfig=True):
        """
        This constructor is called when constructing new interface,
        it is usually done manually while creating Unit or
        automatically while extracting interfaces from UnitWithSoure

        :param masterDir: direction which this interface should have for master
        :param multiplyedBy: this can be instance of integer or Param,
            this mean the interface is array of the interfaces
            where multiplyedBy is the size
        :param loadConfig: do load config in __init__
        """
        self._setAttrListener = None
        self._associatedClk = None
        self._associatedRst = None
        self._parent = None

        super().__init__()
        self._masterDir = masterDir
        # Interface is instanciated inside of Unit first,
        # master direction actually means slave from outside view
        self._direction = INTF_DIRECTION.UNKNOWN

        self._ctx = None

        if loadConfig:
            self._loadConfig()

        # flags for better design error detection
        self._isExtern = False
        self._isAccessible = True
        self._ag = None

    def _m(self):
        """
        Note that this interface will be master

        :return: self
        """
        assert not hasattr(self, "_interfaces") or not self._interfaces, \
            "Too late to change direction of interface"
        self._direction = DIRECTION.asIntfDirection(DIRECTION.opposite(self._masterDir))

        return self

    def __call__(self, other):
        """
        :attention: it is not call of function it is operator of assignment
        """
        assert self._direction != INTF_DIRECTION.MASTER
        return self._connectTo(other)

    @internal
    def _loadDeclarations(self):
        """
        load declaratoins from _declr method
        This function is called first for parent and then for children
        """
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None

        for i in self._interfaces:
            i._isExtern = self._isExtern
            i._loadDeclarations()

        if self._isExtern:
            # direction from inside of unit (reverset compared to outside direction)
            if self._direction == INTF_DIRECTION.UNKNOWN:
                self._direction = INTF_DIRECTION.MASTER
            self._setDirectionsLikeIn(self._direction)

    @internal
    def _clean(self, rmConnetions=True, lockNonExternal=True):
        """
        Remove all signals from this interface (used after unit is synthesized
        and its parent is connecting its interface to this unit)
        """

        if self._interfaces:
            for i in self._interfaces:
                i._clean(rmConnetions=rmConnetions,
                         lockNonExternal=lockNonExternal)
        else:
            self._sigInside = self._sig
            del self._sig

        if lockNonExternal and not self._isExtern:
            self._isAccessible = False  # [TODO] mv to signal lock

    @internal
    def _connectToIter(self, master, exclude=None, fit=False):
        if exclude and (self in exclude or master in exclude):
            return

        if self._interfaces:
            for ifc in self._interfaces:
                if exclude and ifc in exclude:
                    continue

                mIfc = getattr(master, ifc._name)
                if exclude and mIfc in exclude:
                    continue

                if mIfc._masterDir == DIRECTION.OUT:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection %r <= %r" % (ifc, mIfc))

                    yield from ifc._connectTo(mIfc,
                                              exclude=exclude,
                                              fit=fit)
                else:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection %r <= %r" % (mIfc, ifc))

                    yield from mIfc._connectTo(ifc,
                                               exclude=exclude,
                                               fit=fit)
        else:
            dstSig = toHVal(self)
            srcSig = toHVal(master)

            if fit:
                srcSig = fitTo(srcSig, dstSig)

            yield dstSig(srcSig)

    @internal
    def _signalsForInterface(self, context, prefix='', typeTransform=None):
        """
        generate _sig for each interface which has no subinterface
        if already has _sig return it instead

        :param context: instance of RtlNetlist where signals should be created
        :param prefix: name prefix for created signals
        :param typeTransform: optional function (type) returns modified type
            for signal
        """
        sigs = []
        if self._interfaces:
            for intf in self._interfaces:
                sigs.extend(
                    intf._signalsForInterface(context, prefix,
                                              typeTransform=typeTransform))
        else:
            if hasattr(self, '_sig'):
                sigs = [self._sig]
            else:
                t = self._dtype
                if typeTransform is not None:
                    t = typeTransform(t)

                s = context.sig(prefix + self._getPhysicalName(), t)
                s._interface = self
                self._sig = s

                if hasattr(self, '_boundedEntityPort'):
                    self._boundedEntityPort.connectSig(self._sig)
                sigs = [s]

        return sigs

    def _getPhysicalName(self):
        """Get name in HDL """
        if hasattr(self, "_boundedEntityPort"):
            return self._boundedEntityPort.name
        else:
            return self._getFullName().replace('.', self._NAME_SEPARATOR)

    def _getFullName(self):
        """get all name hierarchy separated by '.' """
        return HObjList._getFullName(self)

    def _updateParamsFrom(self, otherObj, updater=_default_param_updater,
                          exclude=None, prefix=""):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        PropDeclrCollector._updateParamsFrom(
            self, otherObj, updater, exclude, prefix)

    def _bit_length(self):
        """Sum of all width of interfaces in this interface"""
        try:
            interfaces = self._interfaces
        except AttributeError:
            interfaces = None

        if interfaces is None:
            # not loaded interface
            _intf = self.__copy__()
            _intf._loadDeclarations()
            interfaces = _intf._interfaces

        if interfaces:
            w = 0
            for i in interfaces:
                w += i._bit_length()
            return w
        else:
            return self._dtype.bit_length()

    def _connectTo(self, master, exclude=None, fit=False):
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        return list(self._connectToIter(master, exclude, fit))

    def __repr__(self):
        s = [self.__class__.__name__]
        s.append("name=%s" % self._getFullName())
        if hasattr(self, '_width'):
            s.append("_width=%s" % str(self._width))
        if hasattr(self, '_masterDir'):
            s.append("_masterDir=%s" % str(self._masterDir))
        return "<%s>" % (', '.join(s))
