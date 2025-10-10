from copy import copy
from typing import Sequence, Optional, Union, Self

from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.types.structValBase import HStructConstBase
from hwt.hwIO import HwIO
from hwt.pyUtils.typingFuture import override
from hwt.synthesizer.typePath import TypePath
from hwtSimApi.agents.base import AgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION


class HwIOArray(HObjList[Optional[HwIO]], HwIO):
    """
    HwIO for array like interfaces, this object is mutable but
    for conviniece it is better to populate this in constructor
    or atleast before registration on parent object.
    """

    def __init__(self, items: Sequence[HwIO]=(), masterDir=DIRECTION.OUT,
                 hdlName:Optional[Union[str, dict[str, str]]]=None,
                 loadConfig=True):
        HObjList.__init__(self, items)
        HwIO.__init__(self, masterDir=masterDir, hdlName=hdlName, loadConfig=loadConfig)

    @override
    def hwDeclr(self):
        self._registerArray(None, self, TypePath())

    def __hash__(self):
        # :note: __hash__, __eq__ are overriden because HObjList by default is non hashable
        return id(self)

    def __eq__(self, other:object) -> bool:
        """
        HwIO is an unique object representig IO of the component that is only the same object should equal to self
        """
        return other is self

    def __copy__(self):
        c = self.__class__(copy(i) for i in self)
        if self:
            c._updateHwParamsFrom(self[0])
        return c

    @internal
    def _registerSubmodule(self, mName:str, submodule:"HwModule", onParentPropertyPath: TypePath):
        raise AssertionError(self, "should not have submodules", mName, submodule, onParentPropertyPath)

    def __call__(self, other: Self, exclude=None, fit=False):
        """
        () operator behaving as assignment operator
        """
        if not isinstance(other, (list, tuple)):
            raise TypeError(other)
        if len(self) != len(other):
            raise ValueError("Different number of interfaces in list",
                             len(self), len(other))

        statements = []
        for a, b in zip(self, other):
            stms = a(b, exclude=exclude, fit=fit)
            if isinstance(stms, HdlStatement):
                statements.append(stms)
            else:
                statements += stms

        return statements

    @override
    def _initSimAgent(self, sim: HdlSimulator):
        # rst = self._getAssociatedRst()
        self._ag = HwIOArrayAgent(sim, self)  # , (rst, rst._dtype.negated)


class HwIOArrayAgent(AgentBase):
    """
    Agent for HwIOArray

    :summary: only purpose is to instantiate agents for child interfaces
    """

    def __init__(self, sim: HdlSimulator, hwIO: HwIOArray):
        AgentBase.__init__(self, sim, hwIO)
        for subHwIO in hwIO._hwIOs:
            subHwIO._initSimAgent(sim)

    def set_data(self, d: Union[HStructConstBase, list]):
        hwIO = self.hwIO
        if d is None:
            for hio in hwIO._hwIOs:
                hio._ag.set_data(None)
        else:
            assert len(d) == len(hwIO._hwIOs), (d, hwIO._hwIOs)
            for v, hio in zip(d, hwIO._hwIOs):
                hio._ag.set_data(v)

    def get_data(self):
        hwIO = self.hwIO
        return tuple(hio._ag.get_data() for hio in hwIO._hwIOs)

    def getMonitors(self):
        for hio in self.hwIO._hwIOs:
            yield from hio._ag.getMonitors()

    def getDrivers(self):
        for hio in self.hwIO._hwIOs:
            yield from hio._ag.getDrivers()
