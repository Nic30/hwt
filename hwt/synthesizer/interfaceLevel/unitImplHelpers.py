from itertools import chain
from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.constants import INTF_DIRECTION, DIRECTION
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.struct import HStruct
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NO_NOPVAL


def getClk(unit):
    """
    Get clock signal from unit instance
    """
    try:
        return unit.clk
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find clock signal on unit %r" % (unit,))


def getRst(unit):
    """
    Get reset signal from unit instance
    """
    try:
        return unit.rst
    except AttributeError:
        pass

    try:
        return unit.rst_n
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find reset signal on unit %r" % (unit,))


def getSignalName(sig):
    """
    Name getter which works for RtlSignal and Interface instances as well
    """
    try:
        return sig._name
    except AttributeError:
        pass
    return sig.name


@internal
def _default_param_updater(self, myP, otherP_val):
    myP.set_value(otherP_val)


class UnitImplHelpers(object):

    def _reg(self, name, dtype=BIT, def_val=None, clk=None, rst=None) -> RtlSyncSignal:
        """
        Create RTL register in this unit

        :param def_val: default value of this register,
            if this value is specified reset signal of this component is used
            to generate a reset logic
        :param clk: optional clok signal specification, (signal or tuple(signal, edge type))
        :type clk: Union[RtlSignal, Interface, Tuple[Union[RtlSignal, Interface], AllOps.RISING/FALLING_EDGE]]
        :param rst: optional reset signal specification
        :note: rst/rst_n resolution is done from signal type,
            if it is negated type it is rst_n
        :note: if clk or rst is not specifid default signal
            from parent unit will be used
        """
        if clk is None:
            clk = getClk(self)

        if def_val is None:
            # if no value is specified reset is not required
            rst = None
        elif rst is None:
            rst = getRst(self)

        if isinstance(dtype, HStruct):
            container = dtype.from_py(None)
            for f in dtype.fields:
                if f.name is not None:
                    if def_val is None:
                        _def_val = None
                    else:
                        _def_val = def_val.get(f.name, None)
                    r = self._reg("%s_%s" % (name, f.name), f.dtype,
                                  def_val=_def_val)
                    setattr(container, f.name, r)

            return container

        return self._ctx.sig(name,
                             dtype=dtype,
                             clk=clk,
                             syncRst=rst,
                             def_val=def_val)

    def _sig(self, name, dtype=BIT, def_val=None, nop_val=NO_NOPVAL) -> RtlSignal:
        """
        Create signal in this unit
        """
        if isinstance(dtype, HStruct):
            if def_val is not None:
                raise NotImplementedError()
            if nop_val is not NO_NOPVAL:
                raise NotImplementedError()
            container = dtype.from_py(None)
            for f in dtype.fields:
                if f.name is not None:
                    r = self._sig("%s_%s" % (name, f.name), f.dtype)
                    setattr(container, f.name, r)

            return container

        return self._ctx.sig(name, dtype=dtype, def_val=def_val, nop_val=nop_val)

    @internal
    def _cleanAsSubunit(self):
        """
        Disconnect internal signals so unit can be reused by parent unit
        """
        for pi in self._entity.ports:
            pi.connectInternSig()
        for i in chain(self._interfaces, self._private_interfaces):
            i._clean()

    @internal
    def _signalsForMyEntity(self, context, prefix):
        """
        generate for all ports of subunit signals in this context
        """
        for i in self._interfaces:
            if i._isExtern:
                i._signalsForInterface(context, None, prefix + i._NAME_SEPARATOR)

    @internal
    def _boundInterfacesToEntity(self, interfaces, ports):
        externSignals = []
        inftToPortDict = {}

        for p in ports:
            inftToPortDict[p._interface] = p

        for intf in interfaces:
            if intf._isExtern:
                for s in walkPhysInterfaces(intf):
                    externSignals.append(s)

        assert len(externSignals) == len(inftToPortDict.keys())

        for s in externSignals:
            self._boundIntfSignalToEntity(s, inftToPortDict)

    @internal
    def _boundIntfSignalToEntity(self, interface, inftToPortDict):
        portItem = inftToPortDict[interface]
        interface._boundedEntityPort = portItem
