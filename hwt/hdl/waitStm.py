from hwt.hdl.statements import HdlStatement


class WaitStm(HdlStatement):
    """
    Structural container of wait statemnet for hdl rendering
    """

    def __init__(self, waitForWhat):
        self.isTimeWait = isinstance(waitForWhat, int)
        self.waitForWhat = waitForWhat
