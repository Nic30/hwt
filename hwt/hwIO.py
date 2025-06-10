from copy import copy
from typing import Optional, Union, Generator, Callable, Self

from hdlConvertorAst.translate.common.name_scope import NameScope
from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.const import HConst
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.types.bitsCastUtils import fitTo
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import HwIOBase
from hwt.synthesizer.exceptions import IntfLvlConfErr, InterfaceStructureErr
from hwt.synthesizer.interfaceLevel.directionFns import \
    HwIODirectionFns
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwtSimApi.agents.base import AgentBase
from ipCorePackager.constants import DIRECTION, INTF_DIRECTION


from hwt.synthesizer.interfaceLevel.implDependent import\
    HwIOImplDependentFns
from hwt.synthesizer.interfaceLevel.propDeclrCollector import\
    PropDeclrCollector


def _default_param_updater(self, myP, parentPval):
    myP.set_value(parentPval)


class HwIO(HwIOBase, HwIOImplDependentFns,
           PropDeclrCollector, HwIODirectionFns):
    """
    Base class for all interfaces in interface synthesizer

    :cvar _NAME_SEPARATOR: separator for nested interface names
    :ivar ~._hwParams: [] of parameter
    :ivar ~._hwIOs: [] sub interfaces
    :ivar ~._name: name assigned during synthesis
    :ivar ~._parent: parent object (HwModule or HwIO instance)
    :ivar ~._isExtern: If true synthesizer sets it as external port of unit
    :ivar ~._associatedClk: clock Signal (interface) associated with
        this interface if is none simulation agent try to search it on parent
    :ivar ~._associatedRst: rst(_n) Signal (interface) associated
        with this interface if is none simulation agent try to search
        it on parent

    :note: only interfaces without _hwIOs have

    :ivar ~._boundedSigLvlHwModule: RTL unit for which was this interface created


    Agenda of directions and HDL

    :ivar ~._masterDir: specifies which direction has this interface at master
    :ivar ~._direction: means actual direction of this interface resolved
        by its drivers
    :ivar ~._rtlCtx: RTL netlist context of all signals and params
        on this interface after interface is registered on parent _ctx
        is merged
    :ivar ~._hdlPort: a HdlPortItem instance available once the unit is synthesized

    Agenda of simulations

    :ivar ~._ag: agent object connected to this interface
        (initialized only before simulation)
    """

    _NAME_SEPARATOR = "_"

    def __init__(self, masterDir=DIRECTION.OUT,
                 hdlName:Optional[Union[str, dict[str, str]]]=None,
                 loadConfig=True):
        """
        This constructor is called when constructing new interface,
        it is usually done manually while creating :class:`hwt.hwModule.HwModule` or
        automatically while extracting interfaces from HwModuleWithSoure

        :param masterDir: direction which this interface should have for master
        :param loadConfig: do load config in __init__
        """
        self._setAttrListener: Optional[Callable[[str, object], None]] = None
        self._associatedClk: Optional[HwIO] = None
        self._associatedRst: Optional[HwIO] = None
        self._parent: Optional["HwModule"] = None
        self._name: Optional[str] = None

        super().__init__()
        self._masterDir: DIRECTION = masterDir
        # HwIO is instantiated inside of :class:`hwt.hwModule.HwModule` first,
        # master direction actually means slave from outside view
        self._direction: INTF_DIRECTION = INTF_DIRECTION.UNKNOWN
        self._rtlCtx: Optional[RtlNetlist] = None

        if loadConfig:
            self._loadConfig()

        # flags for better design error detection
        self._isExtern = False
        self._ag: Optional[AgentBase] = None
        self._hdlPort: Optional[HdlPortItem] = None
        self._hdlNameOverride = hdlName

    def _m(self) -> Self:
        """
        Note that this interface will be master

        :return: self
        """
        assert not hasattr(self, "_hwIOs") or not self._hwIOs, \
            "Too late to change direction of interface"
        self._direction = DIRECTION.asIntfDirection(DIRECTION.opposite(self._masterDir))

        return self

    def __call__(self, other, exclude=None, fit=False) -> list[HdlAssignmentContainer]:
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
    def _loadHwDeclarations(self):
        """
        load declarations from _declr method
        This function is called first for parent and then for children
        """
        if not hasattr(self, "_hwIOs"):
            self._hwIOs = []
        self._setAttrListener = self._declrCollector
        self.hwDeclr()
        self._setAttrListener = None

        for sHwIO in self._hwIOs:
            sHwIO._loadHwDeclarations()
            sHwIO._setAsExtern(self._isExtern)

        if self._isExtern:
            # direction from inside of unit (reverset compared to outside direction)
            if self._direction == INTF_DIRECTION.UNKNOWN:
                self._direction = INTF_DIRECTION.MASTER
            self._setDirectionsLikeIn(self._direction)

    @internal
    def _cleanRtlSignals(self, lockNonExternal=True):
        """
        Remove all signals from this interface (used after unit is synthesized
        and its parent is connecting its interface to this unit)
        """

        if self._hwIOs:
            for sHwIO in self._hwIOs:
                sHwIO._cleanRtlSignals(lockNonExternal=lockNonExternal)

    def _connectTo(self, master, exclude=None, fit=False) -> list[HdlAssignmentContainer]:
        """
        connect to another interface interface (on RTL level)
        works like self <= master in VHDL
        """
        return list(self._connectToIter(master, exclude, fit))

    @internal
    def _connectToIter(self, master, exclude, fit) -> Generator[HdlAssignmentContainer, None, None]:
        if exclude and (self in exclude or master in exclude):
            return

        if self._hwIOs:
            seenMasterHwIOs = []
            for hio in self._hwIOs:
                if exclude and hio in exclude:
                    mHwIO = getattr(master, hio._name, None)
                    if mHwIO is not None:
                        seenMasterHwIOs.append(mHwIO)
                    continue
                if master is None:
                    mHwIO = hio._dtype.from_py(None)
                else:
                    try:
                        mHwIO = getattr(master, hio._name)
                    except AttributeError:
                        raise IntfLvlConfErr("Invalid interface structure", hio, "<=", master, "src missing", hio._name)

                seenMasterHwIOs.append(mHwIO)
                if exclude and mHwIO in exclude:
                    continue

                if isinstance(mHwIO, HConst):
                    # HStruct values
                    if (hio._masterDir in (DIRECTION.OUT, DIRECTION.INOUT) and hio._direction == INTF_DIRECTION.MASTER) or\
                        (hio._masterDir == DIRECTION.IN and hio._direction == INTF_DIRECTION.SLAVE):
                        raise IntfLvlConfErr(
                            "Invalid connection", hio, "<=", mHwIO)
                    yield from hio._connectToIter(mHwIO,
                                                  exclude,
                                                  fit)
                elif mHwIO._masterDir == DIRECTION.OUT:
                    if hio._masterDir != mHwIO._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection", hio, "<=", mHwIO)

                    yield from hio._connectToIter(mHwIO,
                                                  exclude,
                                                  fit)
                else:
                    if hio._masterDir != mHwIO._masterDir:
                        raise IntfLvlConfErr(
                            "Invalid connection", mHwIO, "<=", hio)

                    yield from mHwIO._connectToIter(hio,
                                                   exclude,
                                                   fit)
            if master is None:
                masterHwIOCnt = len(self._hwIOs)
            elif isinstance(master, HConst):
                masterHwIOCnt = len(master._dtype.fields)
            else:
                masterHwIOCnt = len(master._hwIOs)

            if len(seenMasterHwIOs) != masterHwIOCnt:
                if exclude:
                    # there is a possibility that the master interface was excluded,
                    # but we did not see it as the interface of the same name was not present on self
                    for hio in self._hwIOs:
                        if hio in exclude or hio not in seenMasterHwIOs:
                            continue
                        else:
                            # hio is an interface which is extra on master and is missing an equivalent on slave
                            raise InterfaceStructureErr(self, master, exclude)
                else:
                    raise InterfaceStructureErr(self, master, exclude)
        else:
            if not isinstance(master, HConst) and master._hwIOs:
                raise InterfaceStructureErr(self, master, exclude)

            dstSig = toHVal(self)
            srcSig = toHVal(master)

            if fit:
                srcSig = fitTo(srcSig, dstSig)

            yield dstSig(srcSig)

    @internal
    def _signalsForHwIO(self,
                             ctx: RtlNetlist,
                             res: Optional[dict[RtlSignal, DIRECTION]],
                             name_scope: Optional[NameScope],
                             prefix='', typeTransform=None,
                             reverse_dir=False):
        """
        Generate RtlSignal _sig and HdlPortInstance _hdlPort
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
        if self._hwIOs:
            for hwIO in self._hwIOs:
                hwIO._signalsForHwIO(ctx, res, name_scope,
                                          prefix=prefix,
                                          typeTransform=typeTransform,
                                          reverse_dir=reverse_dir)
        else:
            assert self._sig is None, self
            t = self._dtype
            if typeTransform is not None:
                t = typeTransform(t)

            hdlName = prefix + self._getHdlName()

            s = ctx.sig(hdlName, t)
            s._hwIO = self
            self._sig = s

            if self._isExtern:
                d = INTF_DIRECTION.asDirection(self._direction)
                m = ctx.parent
                if reverse_dir:
                    d = DIRECTION.opposite(d)
                    assert self._hdlPort is None, (
                        "Now creating a hdl interface for top"
                        " it but seems that it was already created")

                if res is not None:
                    res[s] = d

                if reverse_dir:
                    pi = HdlPortItem.fromSignal(s, m, d)
                    # port of current top component
                    s._name = name_scope.checked_name(s._name, s)
                    pi.connectInternSig(s)
                    ctx.hwModDec.ports.append(pi)
                else:
                    pi = self._hdlPort
                    # port of some subcomponent which names were already checked
                    pi.connectOuterSig(s)

                self._hdlPort = pi

    def _getHdlName(self) -> str:
        """Get name in HDL """
        return HObjList._getHdlName(self)

    def _getFullName(self) -> str:
        """get all name hierarchy separated by '.' """
        return HObjList._getFullName(self)

    def _updateHwParamsFrom(self, otherObj, updater=_default_param_updater,
                          exclude:Optional[tuple[set[str], set[str]]]=None, prefix=""):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateHwParamsFrom`
        """
        PropDeclrCollector._updateHwParamsFrom(
            self, otherObj, updater, exclude, prefix)
        return self

    def _bit_length(self) -> int:
        """Sum of all width of hwIOs in this interface"""
        try:
            hwIOs = self._hwIOs
        except AttributeError:
            hwIOs = None

        if hwIOs is None:
            # not loaded interface
            _hwIO = self.__copy__()
            _hwIO._loadHwDeclarations()
            hwIOs = _hwIO._hwIOs

        if hwIOs:
            w = 0
            for hwIO in hwIOs:
                w += hwIO._bit_length()
            return w
        else:
            return self._dtype.bit_length()

    def __repr__(self) -> str:
        if hasattr(self, "_dtype"):
            t = f" {self._dtype}"
        else:
            t = ""


        if hasattr(self, '_width'):
            w = " _width=%s" % str(self._width)
        else:
            w = ""

        name = self._getFullName()
        return f"<{self.__class__.__name__} {name:s}{w:s}{t:s}>"
