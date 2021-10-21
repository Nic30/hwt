from copy import copy
from typing import Dict, Optional, Union, List, Generator

from hdlConvertorAst.translate.common.name_scope import NameScope
from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION, INTF_DIRECTION
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue
from hwt.synthesizer.exceptions import IntfLvlConfErr, InterfaceStructureErr
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.interfaceUtils.directionFns import \
    InterfaceDirectionFns
from hwt.synthesizer.interfaceLevel.interfaceUtils.implDependent import\
    InterfaceceImplDependentFns
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.propDeclrCollector import\
    PropDeclrCollector
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal
from hwt.synthesizer.vectorUtils import fitTo


def _default_param_updater(self, myP, parentPval):
    myP.set_value(parentPval)


class Interface(InterfaceBase, InterfaceceImplDependentFns,
                PropDeclrCollector, InterfaceDirectionFns):
    """
    Base class for all interfaces in interface synthesizer

    :cvar _NAME_SEPARATOR: separator for nested interface names
    :ivar ~._params: [] of parameter
    :ivar ~._interfaces: [] sub interfaces
    :ivar ~._name: name assigned during synthesis
    :ivar ~._parent: parent object (Unit or Interface instance)
    :ivar ~._isExtern: If true synthesizer sets it as external port of unit
    :ivar ~._associatedClk: clock Signal (interface) associated with
        this interface if is none simulation agent try to search it on parent
    :ivar ~._associatedRst: rst(_n) Signal (interface) associated
        with this interface if is none simulation agent try to search
        it on parent

    :note: only interfaces without _interfaces have

    :ivar ~._boundedSigLvlUnit: RTL unit for which was this interface created


    Agenda of directions and HDL

    :ivar ~._masterDir: specifies which direction has this interface at master
    :ivar ~._direction: means actual direction of this interface resolved
        by its drivers
    :ivar ~._ctx: rtl netlist context of all signals and params
        on this interface after interface is registered on parent _ctx
        is merged
    :ivar ~._hdl_port: a HdlPortItem instance available once the unit is synthesized

    Agenda of simulations

    :ivar ~._ag: agent object connected to this interface
        (initialized only before simultion)
    """

    _NAME_SEPARATOR = "_"

    def __init__(self, masterDir=DIRECTION.OUT,
                 hdl_name:Optional[Union[str, Dict[str, str]]]=None,
                 loadConfig=True):
        """
        This constructor is called when constructing new interface,
        it is usually done manually while creating :class:`hwt.synthesizer.unit.Unit` or
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
        self._name = None

        super().__init__()
        self._masterDir = masterDir
        # Interface is instantiated inside of :class:`hwt.synthesizer.unit.Unit` first,
        # master direction actually means slave from outside view
        self._direction = INTF_DIRECTION.UNKNOWN

        self._ctx = None

        if loadConfig:
            self._loadConfig()

        # flags for better design error detection
        self._isExtern = False
        self._ag = None
        self._hdl_port = None
        self._hdl_name_override = hdl_name

    def _m(self):
        """
        Note that this interface will be master

        :return: self
        """
        assert not hasattr(self, "_interfaces") or not self._interfaces, \
            "Too late to change direction of interface"
        self._direction = DIRECTION.asIntfDirection(DIRECTION.opposite(self._masterDir))

        return self

    def __call__(self, other, exclude=None, fit=False) -> List[HdlAssignmentContainer]:
        """
        :attention: it is not call of function it is operator of assignment
        """
        assert self._direction != INTF_DIRECTION.MASTER
        try:
            return self._connectTo(other, exclude, fit)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

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
            i._loadDeclarations()
            i._setAsExtern(self._isExtern)

        if self._isExtern:
            # direction from inside of unit (reverset compared to outside direction)
            if self._direction == INTF_DIRECTION.UNKNOWN:
                self._direction = INTF_DIRECTION.MASTER
            self._setDirectionsLikeIn(self._direction)

    @internal
    def _clean(self, lockNonExternal=True):
        """
        Remove all signals from this interface (used after unit is synthesized
        and its parent is connecting its interface to this unit)
        """

        if self._interfaces:
            for i in self._interfaces:
                i._clean(lockNonExternal=lockNonExternal)

    def _connectTo(self, master, exclude=None, fit=False) -> List[HdlAssignmentContainer]:
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        return list(self._connectToIter(master, exclude, fit))

    @internal
    def _connectToIter(self, master, exclude, fit) -> Generator[HdlAssignmentContainer, None, None]:
        if exclude and (self in exclude or master in exclude):
            return

        if self._interfaces:
            seen_master_intfs = []
            for ifc in self._interfaces:
                if exclude and ifc in exclude:
                    mIfc = getattr(master, ifc._name, None)
                    if mIfc is not None:
                        seen_master_intfs.append(mIfc)
                    continue
                if master is None:
                    mIfc = ifc._dtype.from_py(None)
                else:
                    try:
                        mIfc = getattr(master, ifc._name)
                    except AttributeError:
                        raise IntfLvlConfErr("Invalid interface structure", ifc, "<=", master, "src missing", ifc._name)

                seen_master_intfs.append(mIfc)
                if exclude and mIfc in exclude:
                    continue

                if isinstance(mIfc, HValue):
                    # HStruct values
                    if (ifc._masterDir in (DIRECTION.OUT, DIRECTION.INOUT) and ifc._direction == INTF_DIRECTION.MASTER) or\
                        (ifc._masterDir == DIRECTION.IN and ifc._direction == INTF_DIRECTION.SLAVE):
                        raise IntfLvlConfErr(
                            "Invalid connection", ifc, "<=", mIfc)
                    yield from ifc._connectToIter(mIfc,
                                                  exclude,
                                                  fit)
                elif mIfc._masterDir == DIRECTION.OUT:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection", ifc, "<=", mIfc)

                    yield from ifc._connectToIter(mIfc,
                                                  exclude,
                                                  fit)
                else:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection", mIfc, "<=", ifc)

                    yield from mIfc._connectToIter(ifc,
                                                   exclude,
                                                   fit)
            if master is None:
                master_intf_cnt = len(self._interfaces)
            elif isinstance(master, HValue):
                master_intf_cnt = len(master._dtype.fields)
            else:
                master_intf_cnt = len(master._interfaces)

            if len(seen_master_intfs) != master_intf_cnt:
                if exclude:
                    # there is a possiblity that the master interface was excluded,
                    # but we did not see it as the interface of the same name was not present on self
                    for ifc in self._interfaces:
                        if ifc in exclude or ifc not in seen_master_intfs:
                            continue
                        else:
                            # ifc is an interface which is extra on master and is missing an equivalent on slave
                            raise InterfaceStructureErr(self, master, exclude)
                else:
                    raise InterfaceStructureErr(self, master, exclude)
        else:
            if not isinstance(master, HValue) and master._interfaces:
                raise InterfaceStructureErr(self, master, exclude)

            dstSig = toHVal(self)
            srcSig = toHVal(master)

            if fit:
                srcSig = fitTo(srcSig, dstSig)

            yield dstSig(srcSig)

    @internal
    def _signalsForInterface(self,
                             ctx: RtlNetlist,
                             res: Optional[Dict[RtlSignal, DIRECTION]],
                             name_scope: Optional[NameScope],
                             prefix='', typeTransform=None,
                             reverse_dir=False):
        """
        Generate RtlSignal _sig and HdlPortInstance _hdl_port
        for each interface which has no subinterface

        :note: if already has _sig return use it instead

        :param ctx: instance of RtlNetlist where signals should be created
        :param res: output dictionary where result should be stored
        :param prefix: name prefix for created signals
        :param name_scope: name scope used to check collisions on port names
            if this a current top (every component is checked
            when it is seen first time)
        :param typeTransform: optional function (type) returns modified type
            for signal
        """
        if self._interfaces:
            for intf in self._interfaces:
                intf._signalsForInterface(ctx, res, name_scope,
                                          prefix=prefix,
                                          typeTransform=typeTransform,
                                          reverse_dir=reverse_dir)
        else:
            assert self._sig is None, self
            t = self._dtype
            if typeTransform is not None:
                t = typeTransform(t)

            hdl_name = prefix + self._getHdlName()

            s = ctx.sig(hdl_name, t)
            s._interface = self
            self._sig = s

            if self._isExtern:
                d = INTF_DIRECTION.asDirection(self._direction)
                u = ctx.parent
                if reverse_dir:
                    d = DIRECTION.opposite(d)
                    assert self._hdl_port is None, (
                        "Now creating a hdl interface for top"
                        " it but seems that it was already created")

                if res is not None:
                    res[s] = d

                if reverse_dir:
                    pi = portItemfromSignal(s, u, d)
                    # port of current top component
                    s.name = name_scope.checked_name(s.name, s)
                    pi.connectInternSig(s)
                    ctx.ent.ports.append(pi)
                else:
                    pi = self._hdl_port
                    # port of some subcomponent which names were already checked
                    pi.connectOuterSig(s)

                self._hdl_port = pi

    def _getHdlName(self) -> str:
        """Get name in HDL """
        return HObjList._getHdlName(self)

    def _getFullName(self) -> str:
        """get all name hierarchy separated by '.' """
        return HObjList._getFullName(self)

    def _updateParamsFrom(self, otherObj, updater=_default_param_updater,
                          exclude=None, prefix=""):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        PropDeclrCollector._updateParamsFrom(
            self, otherObj, updater, exclude, prefix)
        return self

    def _bit_length(self) -> int:
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

    def __repr__(self) -> str:
        s = [self.__class__.__name__]
        s.append("name=%s" % self._getFullName())
        if hasattr(self, '_width'):
            s.append("_width=%s" % str(self._width))
        if hasattr(self, '_masterDir'):
            s.append("_masterDir=%s" % str(self._masterDir))
        return "<%s>" % (', '.join(s))
