import math
from typing import List, Tuple, Union

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, STR, BIT
from hwt.hdl.types.integer import Integer
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.param import evalParam, Param
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from ipCorePackager.intfConfig import IntfConfigBase
from ipCorePackager.otherXmlObjs import Value
from hwt.hdl.types.hdlType import HdlType
from hwt.synthesizer.interface import Interface
from hwt.hdl.typeShortcuts import hInt


class IntfConfig(IntfConfigBase):

    def getInterfaceName(self, thisIntf):
        return getSignalName(thisIntf)

    def getPhysicalName(self, thisIntf):
        return thisIntf._sigInside.name

    def getDirection(self, thisIntf):
        return thisIntf._direction

    def getExprVal(self, val, do_eval=False):
        ctx = VhdlSerializer.getBaseContext()

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Width value can not be converted do ipcore format (%r)",
                val)
        ctx.createTmpVarFn = createTmpVar
        if do_eval:
            val = val.staticEval()
        val = VivadoTclExpressionSerializer.asHdl(val, ctx)

    def getWidth(self, signal) -> Tuple[int, Union[int, "RtlSignal"], bool]:
        width = signal._dtype.width
        if isinstance(width, int):
            width = str(width)
        else:
            width = self.getExprVal(width)

        return width, str(width), False


class VivadoTclExpressionSerializer(VhdlSerializer):
    # disabled because this code is not reachable in current implemetation
    @staticmethod
    def SignalItem(si, declaration=False):
        raise NotImplementedError()


class IpPackager(object):
    """
    IP-core packager

    :summary: Packs HDL, constraint and other files to IP-Core package
        for distribution and simple integration

    """

    def __init__(self, topUnit: Unit, name: str=None,
                 extraVhdlFiles: List[str]=[],
                 extraVerilogFiles: List[str]=[],
                 serializer=VhdlSerializer,
                 targetPlatform=DummyPlatform()):
        """
        :param topObj: Unit instance of top component
        :param name: optional name of top
        :param extraVhdlFiles: list of extra vhdl file names for files
            which should be distributed in this IP-core
        :param extraVerilogFiles: same as extraVhdlFiles just for Verilog
        :param serializer: serializer which specifies target HDL language
        :param targetPlatform: specifies properties of target platform, like available resources, vendor, etc.
        """
        assert not topUnit._wasSynthetised()
        super(IpPackager, self).__init__(
            topUnit, extraVhdlFiles, extraVerilogFiles)
        self.serializer = serializer
        self.targetPlatform = targetPlatform

    def toHdlConversion(self, top, topName: str, saveTo: str) -> List[str]:
        """
        :param top: object which is represenation of design
        :param topName: name which should be used for ipcore
        :param saveTo: path of directory where generated files should be stored

        :return: list of file namens in correct compile order
        """

        return toRtl(top,
                     saveTo=saveTo,
                     name=topName,
                     serializer=self.serializer,
                     targetPlatform=self.targetPlatform)

    def paramToIpValue(self, idPrefix: str, g: Param, resolve) -> Value:
        val = Value()
        val.id = idPrefix + g.name
        val.resolve = resolve
        t = g._dtype

        def getVal():
            v = evalParam(g.defVal)
            if v.vldMask:
                return v.val
            else:
                return 0

        def bitString(w):
            val.format = "bitString"
            digits = math.ceil(w / 4)
            val.text = ('0x%0' + str(digits) + 'X') % getVal()
            val.bitStringLength = str(w)

        if t == BOOL:
            val.format = "bool"
            val.text = str(bool(getVal())).lower()
        elif isinstance(t, Integer):
            val.format = "long"
            val.text = str(getVal())
        elif t == STR:
            val.format = "string"
            val.text = g.defVal.staticEval().val
        elif isinstance(t, Bits):
            bitString(g.defVal._dtype.bit_length())
        else:
            raise NotImplementedError(
                "Not implemented for datatype %s" % repr(t))
        return val
    
    def serializeType(self, hdlType: HdlType) -> str:
        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Can not seraialize hdl type %r into"
                "ipcore format" % (hdlType))
        return VivadoTclExpressionSerializer.HdlType(hdlType, createTmpVar)

    def getType(self, intf: Interface) -> HdlType:
        return intf._dtype

    def getVectorFromType(self, dtype) -> Union[False, None, Tuple[int, int]]:
        if dtype == BIT:
            return False
        elif isinstance(dtype, Bits):
            return [evalParam(dtype.width) - 1, hInt(0)]

