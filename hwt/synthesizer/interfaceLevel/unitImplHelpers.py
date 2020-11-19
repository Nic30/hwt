from itertools import chain

from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.struct import HStruct
from hwt.interfaces.structIntf import HdlTypeToIntf
from hwt.synthesizer.interfaceLevel.getDefaultClkRts import getClk, getRst
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NO_NOPVAL
from hwt.synthesizer.rtlLevel.rtlSyncSignal import RtlSyncSignal
from hwt.interfaces.std import Signal
from typing import Union, Optional, Tuple
from hwt.hdl.types.hdlType import HdlType
from mesonbuild.cmake.client import SignalBase
from hwt.hdl.operatorDefs import OpDefinition
from hwt.synthesizer.typePath import TypePath


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


@internal
def _flatten_map(prefix: TypePath, d: Union[None, dict, list, tuple], res: dict):
    if d is None:
        return
    elif isinstance(d, dict):
        kv_it = d.items()
    elif isinstance(d, (list, tuple)):
        kv_it = enumerate(d)
    else:
        raise NotImplementedError(d)
    
    for k, v in kv_it:
        if isinstance(v, (dict, list, tuple)):
            _flatten_map(prefix / k, v, res)
        else:
            res[prefix / k] = v


class UnitImplHelpers(UnitBase):

    def _reg(self, name: str,
             dtype: HdlType=BIT,
             def_val: Union[int, None, dict, list]=None,
             clk: Union[SignalBase, None, Tuple[SignalBase, OpDefinition]]=None,
             rst: Optional[SignalBase]=None) -> RtlSyncSignal:
        """
        Create RTL FF register in this unit

        :param def_val: s default value of this register,
            if this value is specified reset signal of this component is used
            to generate a reset logic
        :param clk: optional clock signal specification,
            (signal or tuple(signal, edge type (AllOps.RISING_EDGE/FALLING_EDGE)))
        :param rst: optional reset signal specification
        :note: rst/rst_n resolution is done from signal type,
            if it is negated type the reset signal is interpreted as rst_n
        :note: if clk or rst is not specified default signal
            from parent unit instance will be used
        """
        if clk is None:
            clk = getClk(self)

        if def_val is None:
            # if no value is specified reset is not required
            rst = None
        elif rst is None:
            rst = getRst(self)

        if isinstance(dtype, HStruct):
            container = HdlTypeToIntf(dtype)
            container._loadDeclarations()
            flattened_def_val = {}
            _flatten_map(TypePath(), def_val, flattened_def_val)
            for path, intf in container._fieldsToInterfaces.items():
                if isinstance(intf, Signal):
                    _def_val = flattened_def_val.get(path, None)
                    intf._sig = self._reg(
                        "%s_%s" % (name, intf._getFullName(separator_getter=lambda x: "_")),
                        intf._dtype,
                        def_val=_def_val)

            return container
        elif isinstance(dtype, HArray):
            raise NotImplementedError()

        return self._ctx.sig(name,
                             dtype=dtype,
                             clk=clk,
                             syncRst=rst,
                             def_val=def_val)

    def _sig(self, name: str,
             dtype: HdlType=BIT,
             def_val: Union[int, None, dict, list]=None,
             nop_val: Union[int, None, dict, list, "NO_NOPVAL"]=NO_NOPVAL) -> RtlSignal:
        """
        Create signal in this unit
        
        :see: :func:`hwt.synthesizer.rtlLevel.netlist.RtlNetlist.sig`
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
        for i in chain(self._interfaces, self._private_interfaces):
            i._clean()

    @internal
    def _signalsForSubUnitEntity(self, context, prefix: str):
        """
        generate signals in this context for all ports of this subunit
        """
        for i in self._interfaces:
            if i._isExtern:
                i._signalsForInterface(context, None, None, prefix=prefix + i._NAME_SEPARATOR)

