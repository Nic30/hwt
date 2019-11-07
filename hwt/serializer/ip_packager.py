import math
from typing import List, Tuple, Union

from hwt.doc_markers import internal
from hwt.hdl.typeShortcuts import hInt
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, STR, BIT, INT
from hwt.hdl.types.hdlType import HdlType
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from ipCorePackager.otherXmlObjs import Value
from ipCorePackager.packager import IpCorePackager


class VivadoTclExpressionSerializer(VhdlSerializer):

    # disabled because this code is not reachable in current implemetation
    @staticmethod
    def SignalItem(si, declaration=False):
        raise NotImplementedError(si)


class IpPackager(IpCorePackager):
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
        if not name:
            name = topUnit._getDefaultName()

        super(IpPackager, self).__init__(
            topUnit, name, extraVhdlFiles, extraVerilogFiles)
        self.serializer = serializer
        self.targetPlatform = targetPlatform

    @internal
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

    @internal
    def paramToIpValue(self, idPrefix: str, g: Param, resolve) -> Value:
        val = Value()
        val.id = idPrefix + g.hdl_name
        val.resolve = resolve
        # t = g._dtype

        # def getVal():
        #     v = g.def_val
        #     if v.vld_mask:
        #         return v.val
        #     else:
        #         return 0
        #
        # def bitString(w):
        #     val.format = "bitString"
        #     digits = math.ceil(w / 4)
        #     val.text = ('0x%0' + str(digits) + 'X') % getVal()
        #     val.bitStringLength = str(w)

        # if t == BOOL:
        #     val.format = "bool"
        #     val.text = str(bool(getVal())).lower()
        # elif t == INT:
        #     val.format = "long"
        #     val.text = str(getVal())
        # elif t == STR:
        val.format = "string"
        val.text = str(g.get_value())
        # elif isinstance(t, Bits):
        #     bitString(g.def_val._dtype.bit_length())
        # else:
        #     raise NotImplementedError(
        #         "Not implemented for datatype %s" % repr(t))
        return val

    @internal
    def getParamPhysicalName(self, p: Param):
        return p.hdl_name

    @internal
    def getParamType(self, p: Param) -> HdlType:
        return STR  # p._dtype

    @internal
    def iterParams(self, unit: Unit):
        return unit._entity.generics

    @internal
    def iterInterfaces(self, top: Unit):
        return top._interfaces

    @internal
    def serializeType(self, hdlType: HdlType) -> str:
        """
        :see: doc of method on parent class
        """

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Can not seraialize hdl type %r into"
                "ipcore format" % (hdlType))

        return VhdlSerializer.HdlType(hdlType, VhdlSerializer.getBaseContext())

    @internal
    def getVectorFromType(self, dtype) -> Union[bool, None, Tuple[int, int]]:
        """
        :see: doc of method on parent class
        """
        if dtype == BIT:
            return False
        elif isinstance(dtype, Bits):
            return [dtype.bit_length() - 1, hInt(0)]

    @internal
    def getInterfaceType(self, intf: Interface) -> HdlType:
        """
        :see: doc of method on parent class
        """
        return intf._dtype

    @internal
    def getInterfaceLogicalName(self, intf: Interface):
        """
        :see: doc of method on parent class
        """
        return getSignalName(intf)

    @internal
    def getInterfacePhysicalName(self, intf: Interface):
        """
        :see: doc of method on parent class
        """
        return intf._sigInside.name

    @internal
    def getInterfaceDirection(self, thisIntf):
        """
        :see: doc of method on parent class
        """
        return thisIntf._direction

    @internal
    def getExprVal(self, val, do_eval=False):
        """
        :see: doc of method on parent class
        """
        ctx = VhdlSerializer.getBaseContext()

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Width value can not be converted do ipcore format (%r)",
                val)

        ctx.createTmpVarFn = createTmpVar
        if do_eval:
            val = val.staticEval()
        val = VivadoTclExpressionSerializer.asHdl(val, ctx)
        return val

    @internal
    def getTypeWidth(self, dtype: HdlType, do_eval=False)\
            ->Tuple[int, Union[int, RtlSignal], bool]:
        """
        :see: doc of method on parent class
        """
        width = dtype.bit_length()
        widthStr = str(width)
        return width, widthStr, False

    @internal
    def getObjDebugName(self, obj: Union[Interface, Unit, Param]) -> str:
        """
        :see: doc of method on parent class
        """
        return obj._getFullName()

    @internal
    def serialzeValueToTCL(self, val, do_eval=False) -> Tuple[str, str, bool]:
        """
        :see: doc of method on parent class
        """
        if isinstance(val, int):
            val = hInt(val)
        if do_eval:
            val = val.staticEval()

        if isinstance(val, RtlSignalBase):
            ctx = VivadoTclExpressionSerializer.getBaseContext()
            tclVal = VivadoTclExpressionSerializer.asHdl(val, ctx)
            tclValVal = VivadoTclExpressionSerializer.asHdl(
                        val.staticEval())
            return tclVal, tclValVal, False
        else:

            tclVal = VivadoTclExpressionSerializer.asHdl(val, None)
            return tclVal, tclVal, True
