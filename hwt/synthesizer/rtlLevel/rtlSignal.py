from typing import Generator, Union

from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements import HdlStatement
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import Value
from hwt.hdl.variables import SignalItem
from hwt.pyUtils.uniqList import UniqList
from hwt.simulator.exceptions import SimException
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversErr,\
    NoDriverErr
from hwt.synthesizer.rtlLevel.signalUtils.ops import RtlSignalOps


class RtlSignal(RtlSignalBase, SignalItem, RtlSignalOps):
    """
    RtlSignal signal is container of connection
    between statements and operators

    :ivar _usedOps: dictionary of used operators which can be reused
    :ivar endpoints: UniqList of operators and statements
        for which this signal is driver.
    :ivar drivers: UniqList of operators and statements
        which can drive this signal.
    :ivar hiden: means that this signal is part of expression
        and should not be rendered
    :ivar processCrossing: means that this signal is crossing process boundary

    :cvar __instCntr: counter used for generating instance ids
    :ivar _instId: internally used only for intuitive sorting of statements
        in serialized code
    """
    __instCntr = 0

    def __init__(self, ctx, name, dtype, defaultVal=None, nopVal=None,
                 useNopVal=False):
        """
        :param ctx: context - RtlNetlist which is this signal part of
        :param name: name hint for this signal, if is None name
            is chosen automatically
        :param defaultVal: value which is used for reset and as default value
            in hdl
        :param useNopVal: use nopVal or ignore it
        :param nopVal: value which is used to fill up statements when no other
            value is assigned
        """

        if name is None:
            name = "sig_"
            self.hasGenericName = True
        else:
            self.hasGenericName = False

        assert isinstance(dtype, HdlType)
        super(RtlSignal, self).__init__(name, dtype, defaultVal)
        self.ctx = ctx

        if ctx:
            # params does not have any context on created
            # and it is assigned after param is bounded to unit or interface
            ctx.signals.add(self)

        # set can not be used because hash of items are changing
        self.endpoints = UniqList()
        self.drivers = UniqList()
        self._usedOps = {}
        self.hidden = True
        self._instId = RtlSignal._nextInstId()

        self._nopVal = nopVal
        self._useNopVal = useNopVal
        self._const = False

    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i

    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
            if isinstance(self.defaultVal, RtlSignal):
                self._val = self.defaultVal._val.staticEval()
            else:
                if self._val.updateTime < 0:
                    # _val is invalid initialization value
                    self._val = self.defaultVal.clone()

        if not isinstance(self._val, Value):
            raise SimException(
                "Evaluation of signal returned not supported object (%r)"
                % (self._val, ))

        return self._val

    def singleDriver(self):
        """
        Returns a first driver if signal has only one driver.
        """
        # [TODO] no driver exception
        drv_cnt = len(self.drivers)
        if not drv_cnt:
            raise NoDriverErr(self)
        elif drv_cnt != 1:
            raise MultipleDriversErr(self)

        return self.drivers[0]

    def _walk_sensitivity(self, casualSensitivity: set, seen: set, ctx: SensitivityCtx)\
            -> Generator[Union["RtlSignal", "Operator"], None, None]:
        seen.add(self)

        if self._const:
            return

        if not self.hidden:
            casualSensitivity.add(self)
            return

        try:
            op = self.singleDriver()
        except (MultipleDriversErr, NoDriverErr):
            op = None

        if op is None or isinstance(op, HdlStatement):
            casualSensitivity.add(self)
            return

        op._walk_sensitivity(casualSensitivity, seen, ctx)

    def _walk_public_drivers(self, seen: set) -> Generator["RtlSignal", None, None]:
        seen.add(self)
        if not self.hidden:
            yield self
            return

        assert self.drivers, self
        for d in self.drivers:
            yield from d._walk_public_drivers(seen)
