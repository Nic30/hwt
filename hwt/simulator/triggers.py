from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class Timer():

    def __init__(self, time: int):
        self.time = time


class Edge():

    def __init__(self, signal: RtlSignalBase):
        self.signal = signal


class RisingEdge(Edge):
    pass


class FallingEdge(Edge):
    pass


class ReadOnly():
    pass
