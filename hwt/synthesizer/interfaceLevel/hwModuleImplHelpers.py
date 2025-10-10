from itertools import chain
from typing import Union, Optional, Tuple

from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hdl.operatorDefs import HOperatorDef
from hwt.hdl.types.array import HArray
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct
from hwt.hwIOs.hwIOArray import HwIOArray
from hwt.hwIOs.hwIOStruct import HdlType_to_HwIO, HwIOStruct
from hwt.hwIOs.std import HwIOSignal, HwIOClk, HwIORst, HwIORst_n
from hwt.mainBases import HwModuleBase, HwIOBase
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.interfaceLevel.getDefaultClkRts import getClk, getRst
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from ipCorePackager.constants import INTF_DIRECTION


def getSignalName(sig: RtlSignalBase):
    """
    Name getter which works for RtlSignal and HwIO instances as well
    """
    return sig._name


def HwIO_getName(top: HwModuleBase, io: Union[HwIOBase, RtlSignal,
                                              Tuple[Union[HwIOBase, RtlSignal]]]) -> str:
    if isinstance(io, HwIOBase):
        prefix = []
        parent = io._parent
        while parent is not None:
            if parent is top:
                break
            try:
                prefix.append(parent._name)
            except AttributeError:
                prefix.append(repr(parent))
                break
                
            parent = parent._parent

        n = io._getFullName()
        if prefix:
            prefix.reverse()
            prefix.append(n)
            return ".".join(prefix)
        else:
            return n
    elif isinstance(io, tuple):
        return f"({', '.join(HwIO_getName(top, _io) for _io in io)})"
    else:
        return getSignalName(io)


@internal
def _default_param_updater(self, myP: "HwParam", otherP_val):
    myP.set_value(otherP_val)


@internal
def _normalize_default_value_dict_for_HwIO_array(root_val: dict,
                                                val: Union[dict, list, None],
                                                name_prefix: str,
                                                hobj_list: HwIOArray,
                                                neutral_value):
    """
    This function is called to convert data in format
    .. code-block:: python

        {"x": [3, 4]}
        # into
        {"x_0": 3, "x_1": 4}

    This is required because the items of HwIOArray are stored in _hwIOs as a separate items
    and thus we can not resolve the value association otherwise.
    """

    for i, intf in enumerate(hobj_list):
        if val is neutral_value:
            continue
        elif isinstance(val, dict):
            _val = val.get(i, neutral_value)
        else:
            _val = val[i]
        if _val is neutral_value:
            continue

        elm_name = f"{name_prefix:s}_{i:d}"
        if isinstance(intf, HwIOArray):
            _normalize_default_value_dict_for_HwIO_array(root_val, _val, elm_name, intf, neutral_value)
        else:
            root_val[elm_name] = _val


@internal
def _instantiate_signals(hwIO: Union[HwIOSignal, HwIOArray, HwIOStruct],
                         clk: HwIOClk, rst: Union[HwIORst, HwIORst_n],
                         def_val:Union[int, None, dict, list],
                         nop_val:Union[int, None, dict, list],
                         nextSig: Optional[RtlSignalBase], signal_create_fn):
    hwIO._direction = INTF_DIRECTION.UNKNOWN
    if isinstance(hwIO, HwIOSignal):
        name = hwIO._getHdlName()
        hwIO._sig = signal_create_fn(
            name,
            hwIO._dtype,
            clk, rst, def_val, nop_val, nextSig)
        hwIO._sig._hwIO = hwIO

    elif isinstance(hwIO, HwIOArray):
        intf_len = len(hwIO)
        if isinstance(def_val, dict):
            for k in def_val.keys():
                assert k > 0 and k < intf_len, ("Default value for", hwIO, " specifies ", k, " which is not present on interface")
        elif def_val is not None:
            assert len(def_val) == intf_len, ("Default value does not have same size, ", len(def_val), intf_len, hwIO)

        if isinstance(nop_val, dict):
            for k in nop_val.keys():
                assert k > 0 and k < intf_len, ("Nop value for", hwIO, " specifies ", k, " which is not present on interface")
        elif nop_val is not NOT_SPECIFIED:
            assert len(nop_val) == intf_len, ("Nop value does not have same size, ", len(nop_val), intf_len, hwIO)

        for i, elm in enumerate(hwIO):
            if def_val is None:
                _def_val = None
            elif isinstance(def_val, dict):
                _def_val = def_val.get(i, None)
            else:
                _def_val = def_val[i]

            if nop_val is NOT_SPECIFIED:
                _nop_val = NOT_SPECIFIED
            elif isinstance(nop_val, dict):
                _nop_val = nop_val.get(i, NOT_SPECIFIED)
            else:
                _nop_val = nop_val[i]
            if nextSig is NOT_SPECIFIED:
                _nextSig = NOT_SPECIFIED
            else:
                _nextSig = nextSig.get(i, NOT_SPECIFIED)
            _instantiate_signals(elm, clk, rst, _def_val, _nop_val, _nextSig, signal_create_fn)

    else:
        if def_val is not None:
            for k in tuple(def_val.keys()):
                _i = getattr(hwIO, k, NOT_SPECIFIED)
                assert _i is not NOT_SPECIFIED, ("Default value for", hwIO, " specifies ", k, " which is not present on interface")
                if isinstance(_i, HwIOArray):
                    _normalize_default_value_dict_for_HwIO_array(
                        def_val, def_val[k], k, _i, None)

        if nop_val is not NOT_SPECIFIED:
            for k in tuple(nop_val.keys()):
                _i = getattr(hwIO, k, NOT_SPECIFIED)
                assert _i is not NOT_SPECIFIED, ("Nop value for", hwIO, " specifies ", k, " which is not present on interface")
                if isinstance(_i, HwIOArray):
                    _normalize_default_value_dict_for_HwIO_array(
                        nop_val, nop_val[k],
                        k, _i, NOT_SPECIFIED)

        for elm in hwIO._hwIOs:
            name = elm._name
            if def_val is None:
                _def_val = None
            else:
                _def_val = def_val.get(name, None)

            if nop_val is NOT_SPECIFIED:
                _nop_val = NOT_SPECIFIED
            else:
                _nop_val = nop_val.get(name, NOT_SPECIFIED)

            if nextSig is NOT_SPECIFIED:
                _nextSig = NOT_SPECIFIED
            else:
                _nextSig = getattr(nextSig, name)
            _instantiate_signals(elm, clk, rst, _def_val, _nop_val, _nextSig, signal_create_fn)


@internal
def _loadHwDeclarations(intf_or_list: HwIOBase, suggested_name: str):
    if isinstance(intf_or_list, HwIOArray):
        for i, intf in enumerate(intf_or_list):
            _loadHwDeclarations(intf, f"{suggested_name:s}_{i:d}")
    else:
        intf_or_list._name = suggested_name
        intf_or_list._loadHwDeclarations()


def HwIO_without_registration(
        parent:HwModuleBase,
        container: HwIOBase,
        suggested_name:str,
        def_val: Union[int, None, dict, list]=None,
        nop_val: Union[int, None, dict, list, "NOT_SPECIFIED"]=NOT_SPECIFIED,
        nextSig:Optional[RtlSignalBase]=NOT_SPECIFIED):
    """
    Load all parts of interface and construct signals in RtlNetlist context with an automatic name check,
    without need to explicitly add the HwIO into _hwIOs list.
    """
    _loadHwDeclarations(container, suggested_name)
    _instantiate_signals(
        container, None, None, def_val, nop_val, nextSig,
        lambda name, dtype, clk, rst, def_val, nop_val, nextSig: parent._sig(name, dtype,
                                                                  def_val=def_val,
                                                                  nop_val=nop_val,
                                                                  ))
    container._parent = parent
    parent._private_hwIOs.append(container)
    return container


class HwModuleImplHelpers(HwModuleBase):

    def _reg(self, name: str,
             dtype: HdlType=BIT,
             def_val: Union[int, None, dict, list]=None,
             clk: Union[RtlSignalBase, None, Tuple[RtlSignalBase, HOperatorDef]]=None,
             rst: Optional[RtlSignalBase]=None,
             nextSig:Optional[RtlSignalBase]=NOT_SPECIFIED) -> RtlSignal:
        """
        Create RTL FF register in this unit

        :param def_val: s default value of this register,
            if this value is specified reset signal of this component is used
            to generate a reset logic
        :param clk: optional clock signal specification,
            (signal or tuple(signal, edge type (AllOps.RISING_EDGE/FALLING_EDGE)))
        :param rst: optional reset signal specification
        :param nextSig: the signal which should be used as "next" signal for this register
            if is not specified the new signal is generated. (Next signal holds value which should be in register in next clk.)
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

        if isinstance(dtype, (HStruct, HArray)):
            container = HdlType_to_HwIO().apply(dtype)
            _loadHwDeclarations(container, name)
            _instantiate_signals(
                container, clk, rst, def_val, nextSig, NOT_SPECIFIED,
                lambda name, dtype, clk, rst, def_val, nop_val, nextSig: self._reg(name, dtype,
                                                                                   def_val=def_val,
                                                                                   clk=clk, rst=rst,
                                                                                   nextSig=nextSig))
            container._parent = self
            return container
        else:
            # primitive data type signal
            return self._rtlCtx.sig(
                name,
                dtype=dtype,
                clk=clk,
                syncRst=rst,
                def_val=def_val,
                nextSig=nextSig,
            )

    def _sig(self, name: str,
             dtype: HdlType=BIT,
             def_val: Union[int, None, dict, list]=None,
             nop_val: Union[int, None, dict, list, "NOT_SPECIFIED"]=NOT_SPECIFIED) -> RtlSignal:
        """
        Create signal in this unit

        :see: :func:`hwt.synthesizer.rtlLevel.netlist.RtlNetlist.sig`
        """
        if isinstance(dtype, HStruct):
            container = HdlType_to_HwIO().apply(dtype)
            return HwIO_without_registration(self, container, name, def_val=def_val, nop_val=nop_val)
        else:
            # primitive data type signal
            return self._rtlCtx.sig(name, dtype=dtype, def_val=def_val, nop_val=nop_val)

    @internal
    def _cleanThisSubunitRtlSignals(self):
        """
        Disconnect internal signals so unit can be reused by parent unit
        """
        for hwio in chain(self._hwIOs, self._private_hwIOs):
            hwio._cleanRtlSignals()

    @internal
    def _signalsForSubHwModuleEntity(self, context: RtlNetlist, prefix: str):
        """
        generate signals in this context for all ports of this subunit
        """
        for hio in self._hwIOs:
            if hio._isExtern:
                hio._signalsForHwIO(context, None, None, prefix=prefix + hio._NAME_SEPARATOR)

