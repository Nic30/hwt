from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.typeShortcuts import vecT
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BIT
from hwt.interfaces.signalOps import SignalOps
from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.vectorUtils import getWidthExpr


D = DIRECTION


class Signal(SignalOps, Interface):
    def __init__(self,
                 masterDir=D.OUT,
                 multipliedBy=None,
                 dtype=BIT,
                 alternativeNames=None,
                 loadConfig=True):
        super().__init__(masterDir=masterDir,
                         multipliedBy=multipliedBy,
                         alternativeNames=alternativeNames,
                         loadConfig=loadConfig)
        self._dtype = dtype
        self._setMultipliedBy(multipliedBy, updateTypes=True)

    def _injectMultiplerToDtype(self):
        t = self._dtype
        factor = self._multipliedBy
        if t == BIT:
            newT = vecT(factor)
        elif isinstance(t, Bits):
            w = getWidthExpr(t)
            if isinstance(w, RtlSignalBase):
                # bouth Param or factor Value
                newW = w * factor
            elif isinstance(factor, RtlSignalBase):
                # w is Value
                newW = factor * w
            else:
                # bouth Value
                newW = w.clone()
                newW.val *= factor.val
            newT = vecT(newW)
        else:
            raise NotImplementedError("type:%s" % (repr(t)))
        self._dtype = newT

    def _setMultipliedBy(self, factor, updateTypes=True):
        if type(self._multipliedBy) == type(factor) and self._multipliedBy == factor:
            pass
        else:
            self._multipliedBy = factor
            if updateTypes and factor is not None:
                self._injectMultiplerToDtype()

    def _getSimAgent(self):
        from hwt.interfaces.agents.signal import SignalAgent
        return SignalAgent


def VectSignal(width, signed=None, masterDir=D.OUT, multipliedBy=None,
                   alternativeNames=None,
                   loadConfig=True):
    return Signal(masterDir, multipliedBy, vecT(width, signed), 
                   alternativeNames, loadConfig)        


class Clk(Signal):
    _alternativeNames = ['ap_clk', 'aclk', 'clk', 'clock']

    def _getIpCoreIntfClass(self):
        from hwt.serializer.ip_packager.interfaces.std import IP_Clk
        return IP_Clk

    def _getSimAgent(self):
        from hwt.interfaces.agents.clk import OscilatorAgent
        return OscilatorAgent


class Rst(Signal):
    _alternativeNames = ['ap_rst', 'areset', 'reset', 'rst']

    def _getIpCoreIntfClass(self):
        from hwt.serializer.ip_packager.interfaces.std import IP_Rst
        return IP_Rst

    def _getSimAgent(self):
        from hwt.interfaces.agents.rst import PullDownAgent
        return PullDownAgent


class Rst_n(Signal):
    _alternativeNames = ['ap_rst_n', 'aresetn', 'resetn', 'rstn', 'rst_n']

    def _signalsForInterface(self,
                             context,
                             prefix='',
                             typeTransform=None):
        sigs = Signal._signalsForInterface(self,
                                           context,
                                           prefix,
                                           typeTransform=typeTransform)
        for s in sigs:
            s.negated = True
        return sigs

    def _getIpCoreIntfClass(self):
        from hwt.serializer.ip_packager.interfaces.std import IP_Rst_n
        return IP_Rst_n

    def _getSimAgent(self):
        from hwt.interfaces.agents.rst import PullUpAgent
        return PullUpAgent


class VldSynced(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.vld = s(alternativeNames=['valid'])

    def _getSimAgent(self):
        from hwt.interfaces.agents.vldSynced import VldSyncedAgent
        return VldSyncedAgent


class RdSynced(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])

    def _getSimAgent(self):
        from hwt.interfaces.agents.rdSynced import RdSyncedAgent
        return RdSyncedAgent


class Handshaked(VldSynced):
    def _declr(self):
        super()._declr()
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])

    def _getSimAgent(self):
        from hwt.interfaces.agents.handshaked import HandshakedAgent
        return HandshakedAgent


class HandshakeSync(Interface):
    def _declr(self):
        self.vld = s(alternativeNames=['valid'])
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])

    def _getSimAgent(self):
        from hwt.interfaces.agents.handshaked import HandshakeSyncAgent
        return HandshakeSyncAgent


class ReqDoneSync(Interface):
    def _declr(self):
        self.req = s()
        self.done = s(masterDir=D.IN)


class BramPort_withoutClk(Interface):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.addr = s(dtype=vecT(self.ADDR_WIDTH), alternativeNames=['addr_v'])
        self.din = s(dtype=vecT(self.DATA_WIDTH), alternativeNames=['din_v'])
        self.dout = s(masterDir=D.IN, dtype=vecT(self.DATA_WIDTH), alternativeNames=['dout_v'])
        self.en = s()
        self.we = s()

    def _getIpCoreIntfClass(self):
        from hwt.serializer.ip_packager.interfaces.std import IP_BlockRamPort
        return IP_BlockRamPort

    def _getSimAgent(self):
        from hwt.interfaces.agents.bramPort import BramPort_withoutClkAgent
        return BramPort_withoutClkAgent


class BramPort(BramPort_withoutClk):

    def _declr(self):
        super()._declr()
        self.clk = s(masterDir=D.OUT)

    def _getSimAgent(self):
        from hwt.interfaces.agents.bramPort import BramPortAgent
        return BramPortAgent

    @classmethod
    def fromBramPort_withoutClk(cls, bramPort, clk):
        assert isinstance(bramPort, BramPort_withoutClk)
        assert isinstance(clk, Clk)
        self = cls()
        rp = self._replaceParam

        def setIntf(name, intf):
            setattr(self, name, intf)
            self._interfaces.append(intf)

        rp("ADDR_WIDTH", bramPort.ADDR_WIDTH)
        rp("DATA_WIDTH", bramPort.DATA_WIDTH)

        self._interfaces = []
        for iName in ["addr", "din", "dout", "en", "we"]:
            intf = getattr(bramPort, iName)
            setIntf(iName, intf)
        setIntf("clk", clk)

        return self


class FifoWriter(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(8)

    def _declr(self):
        self.en = s()
        self.wait = s(masterDir=D.IN)
        self.data = s(dtype=vecT(self.DATA_WIDTH), alternativeNames=[''])

    def _getSimAgent(self):
        from hwt.interfaces.agents.fifo import FifoWriterAgent
        return FifoWriterAgent


class FifoReader(FifoWriter):
    def _declr(self):
        super()._declr()
        self.en._masterDir = D.IN
        self.wait._masterDir = D.OUT

    def _getSimAgent(self):
        from hwt.interfaces.agents.fifo import FifoReaderAgent
        return FifoReaderAgent


class RegCntrl(Interface):
    """
    Register control interface
    """
    def _config(self):
        self.DATA_WIDTH = Param(8)

    def _declr(self):
        self.din = Signal(dtype=vecT(self.DATA_WIDTH), masterDir=D.IN)
        with self._paramsShared():
            self.dout = VldSynced()

    def _getSimAgent(self):
        from hwt.interfaces.agents.regCntrl import RegCntrlAgent
        return RegCntrlAgent

s = Signal
