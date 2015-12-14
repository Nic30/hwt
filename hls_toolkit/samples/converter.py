from migen.actorlib.structuring import *
from migen.fhdl import verilog
from migen.fhdl.std import *
from migen.flow.actor import *
from migen.flow.network import *


class Converter(Module):
    def __init__(self, layout_from, layout_to):
        self.sink = Sink(layout_from)
        self.source = Source(layout_to)

        ###

        sink_w = flen(self.sink.payload.raw_bits())
        source_w = flen(self.source.payload.raw_bits())

        if sink_w > source_w:
            if sink_w % source_w:
                raise ValueError
            ratio = sink_w//source_w
            self.submodules.cast = Cast(layout_from, pack_layout(layout_to, ratio))
            self.submodules.unpack = Unpack(ratio, layout_to)

            self.comb += [
                Record.connect(self.sink, self.cast.sink),
                Record.connect(self.cast.source, self.unpack.sink),
                Record.connect(self.unpack.source, self.source)
            ]
        elif source_w > sink_w:
            if source_w % sink_w:
                raise ValueError
            ratio = source_w//sink_w
            self.submodules.pack = Pack(layout_from, ratio)
            self.submodules.cast = Cast(pack_layout(layout_from, ratio), layout_to)

            self.comb += [
                Record.connect(self.sink, self.pack.sink),
                Record.connect(self.pack.source, self.cast.sink),
                Record.connect(self.cast.source, self.source)
            ]
        else:
            self.comb += Record.connect(self.sink, self.source)

print(verilog.convert(Converter([("d", 32)], [("d", 8)])))
print(verilog.convert(Converter([("d", 8)], [("d", 32)])))