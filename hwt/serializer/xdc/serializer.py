from itertools import islice
from typing import Union, Tuple

from hwt.constraints import set_max_delay, set_false_path, \
    set_async_reg, get_clock_of, iHdlConstrain
from hwt.hdl.types.bits import HBits
from hwt.pyUtils.arrayQuery import iter_with_last
from hwt.hwIO import HwIO
from hwt.hwModule import HwModule
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class XdcSerializer():
    """
    Convert constrains containers to a XDC format (For Xilinx Vivado)
    """
    fileExtension = ".xdc"

    def __init__(self, out):
        self.out = out

    def _get(self, o: Union[Tuple[HwModule, RtlSignal, HwIO], iHdlConstrain], only_first=False):
        """
        :param only_first: if true select only first bit from vector, else select whole vector
        """
        if isinstance(o, iHdlConstrain):
            return self.visit_iHdlConstrain(o)

        is_reg = False
        _o = o[-1]
        if isinstance(_o, RtlSignal):
            q = "get_cells"
            for d in _o._rtlDrivers:
                if d._event_dependent_from_branch is not None:
                    is_reg = True

        elif isinstance(_o, HwIO):
            q = "get_pins"

        else:
            raise NotImplementedError(o)

        w = self.out.write
        w(q)
        w(" -hier -filter {NAME =~ */")
        path = o
        # [TODO] find out how to make select with ip top module/entity name
        for last, p in iter_with_last(islice(path, 1, None)):
            if isinstance(p, HwModule):
                w(p._name)
                w("_inst")
            elif isinstance(p, RtlSignal):
                w(p._name)
            elif isinstance(p, HwIO):
                w(p._name)
            else:
                raise NotImplementedError(p)
            if not last:
                w("/")

        t = _o._dtype
        if is_reg:
            w("_reg")
        if isinstance(t, HBits) and (t.bit_length() > 1 or t.force_vector):
            # * on end because of Vivado _replica
            if only_first:
                w("[0]*")
            else:
                w("[*]*")
        w("}")

    def visit_get_clock_of(self, o: get_clock_of):
        w = self.out.write
        if isinstance(o.obj[-1], RtlSignal) and o.obj[-1]._rtlNextSig is not None:
            w("get_clocks -of [")
            self._get(o.obj)
            w("]")
        else:
            raise NotImplementedError()

    def visit_iHdlConstrain(self, o):
        visitFn = getattr(self, "visit_" + o.__class__.__name__, None)
        if visitFn is None:
            return o.to_xdc(self, o)
        else:
            return visitFn(o)

    def visit_HdlConstraintList(self, o_list):
        return [self.visit_iHdlConstrain(o) for o in o_list]

    def visit_set_async_reg(self, o: set_async_reg):
        w = self.out.write
        w("set_property ASYNC_REG TRUE [")
        self._get(o.sig)
        w("]\n")

    def visit_set_false_path(self, o: set_false_path):
        w = self.out.write
        w("set_false_path")
        if o.start is not None:
            w(" -from [")
            self._get(o.start)
            w("]")
        if o.end is not None:
            w(" -to [")
            self._get(o.end)
            w("]")
        w("\n")

    def visit_set_max_delay(self, o: set_max_delay):
        w = self.out.write
        w("set_max_delay -from [")
        self._get(o.start)
        w("] -to [")
        self._get(o.end)
        w("]")
        if o.datapath_only:
            w(" -datapath_only")
        w(f" {o.time_ns:f}\n")
