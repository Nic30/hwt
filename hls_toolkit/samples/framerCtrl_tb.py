from hls_toolkit.samples.framerCtrl import ACTIVE_LOW, FramerCtrl, t_State
from myhdl import Signal, instance, always, always_seq, ResetSignal, StopSimulation, Simulation, traceSignals, delay


def testbench():

    SOF = Signal(bool(0))
    syncFlag = Signal(bool(0))
    clk = Signal(bool(0))
    reset = ResetSignal(1, active=ACTIVE_LOW, async=True)
    state = Signal(t_State.SEARCH)

    framectrl = FramerCtrl(SOF, state, syncFlag, clk, reset)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        for _ in range(3):
            yield clk.posedge
        for n in (12, 8, 8, 4):
            syncFlag.next = 1
            yield clk.posedge
            syncFlag.next = 0
            for _ in range(n-1):
                yield clk.posedge
        raise StopSimulation

    @always_seq(clk.posedge, reset=reset)
    def output_printer():
        print( syncFlag, SOF, state)

    return framectrl, clkgen, stimulus, output_printer

tb_fsm = traceSignals(testbench)
sim = Simulation(tb_fsm)
sim.run()