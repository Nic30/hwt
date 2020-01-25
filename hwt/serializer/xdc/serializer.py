from hwt.constraints import set_max_delay, get_parent_unit, set_false_path,\
    set_async_reg, get_clock_of, ConstrainBase
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit
from hwt.hdl.types.bits import Bits
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal


class XdcSerializer():
    """
    Convert constrains containers to a XDC format
    """
    DEFAULT_FILE_NAME = "constraints.xdc"
    def __init__(self, out):
        self.out = out

    def _get(self, o: [Unit, RtlSignal, Interface], only_first=False):
        if isinstance(o, ConstrainBase):
            return self.any(o)

        is_reg = False
        if isinstance(o, RtlSignal):
            q = "get_cells"
            n = o.name
            for d in o.drivers:
                if d._now_is_event_dependent:
                    is_reg = True
        elif isinstance(o, Interface):
            q = "get_pins"
            n = o._name
        else:
            raise NotImplementedError(o)

        pu = get_parent_unit(o)
        w = self.out.write
        w(q)
        w(" -hier -filter {NAME =~ */")
        path = []
        # [TODO] find out how to make select with ip top module/entity name
        while pu is not None and pu._parent is not None:
            path.append(pu._name)
            pu = pu._parent
        for p in reversed(path):
            w(p)
            w("_inst")
            w("/")
        w(n)
        t = o._dtype
        if is_reg:
            w("_reg")
        if isinstance(t, Bits) and (t.bit_length() > 1 or t.force_vector):
            # * on end because of Vivado _replica
            if only_first:
                w("[0]*")
            else:
                w("[*]*")
        w("}")

    def get_clock_of(self, o: get_clock_of):
        w = self.out.write
        if isinstance(o.obj, RtlSyncSignal):
            w("get_clocks -of [")
            self._get(o.obj)
            w("]")
        else:
            raise NotImplementedError()

    def any(self, o):
        return getattr(self, o.__class__.__name__)(o)

    def set_async_reg(self, o: set_async_reg):
        w = self.out.write
        w("set_property ASYNC_REG TRUE [")
        self._get(o.sig)
        w("]\n")
    
    def set_false_path(self, o: set_false_path):
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

    def set_max_delay(self, o: set_max_delay):
        w = self.out.write
        w("set_max_delay -from [")
        self._get(o.start)
        w("] -to [")
        self._get(o.end)
        w("]")
        if o.datapath_only:
            w(" -datapath_only")
        w(" %f\n" % o.time_ns)
