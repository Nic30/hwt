from myhdl import *


ACTIVE_LOW = 0
FRAME_SIZE = 8
t_State = enum('SEARCH', 'CONFIRM', 'SYNC')

def FramerCtrl(SOF, state, syncFlag, clk, reset):

    """ Framing control FSM.

    SOF -- start-of-frame output bit
    state -- FramerState output
    syncFlag -- sync pattern found indication input
    clk -- clock input
    reset_n -- active low reset

    """

    index = Signal(0) # position in frame

    @always_seq(clk.posedge, reset=reset)
    def FSM():
        index.next = (index + 1) % FRAME_SIZE
        SOF.next = 0

        if state == t_State.SEARCH:
            index.next = 1
            if syncFlag:
                state.next = t_State.CONFIRM

        elif state == t_State.CONFIRM:
            if index == 0:
                if syncFlag:
                    state.next = t_State.SYNC
                else:
                    state.next = t_State.SEARCH

        elif state == t_State.SYNC:
            if index == 0:
                if not syncFlag:
                    state.next = t_State.SEARCH
            SOF.next = (index == FRAME_SIZE-1)

        else:
            raise ValueError("Undefined state")

    return FSM