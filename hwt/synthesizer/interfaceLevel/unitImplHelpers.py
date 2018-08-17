from copy import copy
from itertools import chain

from hwt.hdl.constants import INTF_DIRECTION, DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.struct import HStruct
from hwt.pyUtils.arrayQuery import single
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces


def getClk(unit):
    try:
        return unit.clk
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find clock on unit %r" % (unit,))


def getRst(unit):
    try:
        return unit.rst
    except AttributeError:
        pass

    try:
        return unit.rst_n
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find clock on unit %r" % (unit,))


def getSignalName(sig):
    try:
        return sig._name
    except AttributeError:
        pass
    return sig.name


class UnitImplHelpers(object):
    def _reg(self, name, dtype=BIT, defVal=None, clk=None, rst=None):
        """
        Create register in this unit

        :param defVal: default value of this register,
            if this value is specified reset of this component is used
            (unit has to have single interface of class Rst or Rst_n)
        :param clk: optional clok signal specification
        :param rst: optional reset signal specification
        :note: rst/rst_n resolution is done from signal type,
            if it is negated type it is rst_n
        :note: if clk or rst is not specifid default signal
            from parent unit will be used
        """
        if clk is None:
            clk = getClk(self)

        if defVal is None:
            # if no value is specified reset is not required
            rst = None
        else:
            rst = getRst(self)._sig

        if isinstance(dtype, HStruct):
            if defVal is not None:
                raise NotImplementedError()
            container = dtype.fromPy(None)
            for f in dtype.fields:
                if f.name is not None:
                    r = self._reg("%s_%s" % (name, f.name), f.dtype)
                    setattr(container, f.name, r)

            return container

        return self._ctx.sig(name,
                             dtype=dtype,
                             clk=clk._sig,
                             syncRst=rst,
                             defVal=defVal)

    def _sig(self, name, dtype=BIT, defVal=None):
        """
        Create signal in this unit
        """
        if isinstance(dtype, HStruct):
            if defVal is not None:
                raise NotImplementedError()
            container = dtype.fromPy(None)
            for f in dtype.fields:
                if f.name is not None:
                    r = self._sig("%s_%s" % (name, f.name), f.dtype)
                    setattr(container, f.name, r)

            return container

        return self._ctx.sig(name, dtype=dtype, defVal=defVal)

    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for pi in self._entity.ports:
            pi.connectInternSig()
        for i in chain(self._interfaces, self._private_interfaces):
            i._clean()

    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        def lockTypeWidth(t):
            # [TODO] only read parameter instead of full evaluation
            # problem is that parametes should be theyr's values
            # (because this signals are for parent unit)
            if isinstance(t, Bits):
                t = copy(t)
                t.width = t.bit_length()
                return t
            else:
                return t

        for i in self._interfaces:
            if i._isExtern:
                i._signalsForInterface(context, prefix + i._NAME_SEPARATOR,
                                       typeTransform=lockTypeWidth)

    def _boundInterfacesToEntity(self, interfaces):
        externSignals = []
        inftToPortDict = {}

        for p in self._entity.ports:
            inftToPortDict[p._interface] = p

        for intf in self._interfaces:
            if intf._isExtern:
                for s in walkPhysInterfaces(intf):
                    externSignals.append(s)

        assert len(externSignals) == len(inftToPortDict.keys())

        for s in externSignals:
            self._boundIntfSignalToEntity(s, inftToPortDict)

    def _boundIntfSignalToEntity(self, interface, inftToPortDict):
        portItem = single(self._entity.ports,
                          lambda x: x._interface == interface)
        interface._boundedEntityPort = portItem
        d = INTF_DIRECTION.asDirection(interface._direction)

        if d == DIRECTION.INOUT:
            portItem.direction = DIRECTION.INOUT

        if portItem.direction != d:
            raise IntfLvlConfErr(
                ("Unit %s: Port %s does not have direction "
                 " defined by interface %s, is %s should be %s")
                % (self._name, portItem.name,
                   repr(interface), portItem.direction, d))

    def _shareParamsWithPrefix(self, obj, prefix, paramNames):
        for name in paramNames:
            lp = getattr(obj, name)
            p = getattr(self, prefix + name)
            lp.set(p)

    def _updateParamsFrom(self, parent, exclude=None):
        """
        update all parameters which are defined on self from otherObj

        :param exclude: iterable of parameter on parent object which should be excluded
        """
        excluded = set()
        if exclude is not None:
            exclude = set(exclude)
        if isinstance(parent, InterfaceProxy):
            parent = parent._origIntf

        for parentP in parent._params:
            if exclude and parentP in exclude:
                excluded.add(parentP)
                continue

            name = parentP._scopes[parent][1]
            try:
                p = getattr(self, name)
            except AttributeError:
                continue
            p.set(parentP)

        if exclude is not None:
            assert excluded == exclude
