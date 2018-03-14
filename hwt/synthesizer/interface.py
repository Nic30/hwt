from hwt.hdl.constants import DIRECTION, INTF_DIRECTION
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.array import InterfaceArray
from hwt.synthesizer.interfaceLevel.interfaceUtils.directionFns import \
    InterfaceDirectionFns
from hwt.synthesizer.interfaceLevel.interfaceUtils.implDependent import\
    InterfaceceImplDependentFns
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.propDeclrCollector import\
    PropDeclrCollector
from hwt.synthesizer.param import Param
from hwt.synthesizer.vectorUtils import fitTo


def _defaultUpdater(self, onParentName, p):
    self._replaceParam(onParentName, p)


class Interface(InterfaceBase, InterfaceceImplDependentFns, InterfaceArray,
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

    def __init__(self, masterDir=DIRECTION.OUT, asArraySize=None,
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
        if asArraySize is not None:
            asArraySize = toHVal(asArraySize)
            assert int(asArraySize) > 0
            self._widthMultiplier = asArraySize
        else:
            self._widthMultiplier = None

        self._asArraySize = asArraySize

        self._masterDir = masterDir
        self._direction = INTF_DIRECTION.UNKNOWN

        self._ctx = None

        if loadConfig:
            self._loadConfig()

        # flags for better design error detection
        self._isExtern = False
        self._isAccessible = True
        self._dirLocked = False
        self._ag = None

    def __call__(self, other):
        """
        :attention: it is not call of function it is operator of assignment
        """
        return self._connectTo(other)

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
            # inherit _asArraySize and update dtype on physical interfaces
            w = i._widthMultiplier
            if self._widthMultiplier is not None:
                if w is None:
                    w = self._widthMultiplier
                else:
                    w = w * self._widthMultiplier

            i._widthMultiplier = w
            i._isExtern = self._isExtern
            i._loadDeclarations()

        # apply multiplier at dtype of signals
        if not self._interfaces and self._widthMultiplier is not None:
            self._injectMultiplerToDtype()

        if self._isInterfaceArray():
            self._initArrayItems()

        for p in self._params:
            p.setReadOnly()

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

        self._dirLocked = False
        if lockNonExternal and not self._isExtern:
            self._isAccessible = False  # [TODO] mv to signal lock

        if self._isInterfaceArray():
            for e in self._arrayElemCache:
                e._clean(rmConnetions=rmConnetions,
                         lockNonExternal=lockNonExternal)

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

        if self._asArraySize is not None:
            for elemIntf in self._arrayElemCache:
                elemIntf._signalsForInterface(context)
                # they are not in sigs because they are not main signals

        return sigs

    def _getPhysicalName(self):
        """Get name in HDL """
        if hasattr(self, "_boundedEntityPort"):
            return self._boundedEntityPort.name
        else:
            return self._getFullName().replace('.', self._NAME_SEPARATOR)

    def _getFullName(self):
        """get all name hierarchy separated by '.' """
        name = ""
        tmp = self
        while isinstance(tmp, InterfaceBase):
            if hasattr(tmp, "_name"):
                n = tmp._name
            else:
                n = ''
            if name == '':
                name = n
            else:
                name = n + '.' + name
            if hasattr(tmp, "_parent"):
                tmp = tmp._parent
            else:
                tmp = None
        return name

    def _replaceParam(self, pName, newP):
        """
        Replace parameter on this interface (in configuration stage)

        :ivar pName: actual name of param on me
        :ivar newP: new Param instance by which should be old replaced
        """
        p = getattr(self, pName)
        i = self._params.index(p)
        assert i > -1
        self._params[i] = newP
        del p._scopes[self]  # remove reference from old param
        newP._registerScope(pName, self)
        setattr(self, pName, newP)

    def _updateParamsFrom(self, otherObj, updater=_defaultUpdater,
                          exclude=None):
        """
        update all parameters which are defined on self from otherObj

        :param exclude: iterable of parameter on other object
            which should be excluded
        """
        excluded = set()
        if exclude is not None:
            exclude = set(exclude)

        for parentP in otherObj._params:
            if exclude and parentP in exclude:
                excluded.add(parentP)
                continue
            _, onParentName = parentP._scopes[otherObj]
            try:
                myP = getattr(self, onParentName)
                if not isinstance(myP, Param):
                    continue
            except AttributeError:
                continue

            updater(self, onParentName, parentP)

        if exclude is not None:
            assert excluded == exclude

    def _bit_length(self):
        """Sum of all width of interfaces in this interface"""
        try:
            interfaces = self._interfaces
        except AttributeError:
            interfaces = None

        if interfaces is None:
            # not loaded interface
            _intf = self._clone()
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
