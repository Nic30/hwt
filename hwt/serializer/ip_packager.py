import math
from typing import List, Tuple, Union

from hwt.doc_markers import internal
from hwt.hdl.typeShortcuts import hInt
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, STR, BIT, INT
from hwt.hdl.types.hdlType import HdlType
from hwt.serializer.vhdl.serializer import Vhdl2008Serializer, _to_Vhdl2008_str,\
    ToHdlAstVhdl2008
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
from ipCorePackager.intfIpMeta import VALUE_RESOLVE
from io import StringIO
from hwt.serializer.store_manager import SaveToFilesFlat
from hdlConvertor.to.vhdl.vhdl2008 import ToVhdl2008


class VivadoTclExpressionSerializer(Vhdl2008Serializer):

    # disabled because this code is not reachable in current implemetation
    @staticmethod
    def as_hdl_SignalItem(si, declaration=False):
        raise NotImplementedError(si)


class IpPackager(IpCorePackager):
    """
    IP-core packager

    :summary: Packs HDL, constraint and other files to IP-Core package
        for distribution and simple integration

    """

    def __init__(self, topUnit: Unit, name: str=None,
                 extra_files: List[str]=[],
                 serializer_cls=Vhdl2008Serializer,
                 target_platform=DummyPlatform()):
        """
        :param topObj: Unit instance of top component
        :param name: optional name of top
        :param extra_files: list of extra HDL/constrain file names for files
            which should be distributed in this IP-core
            (\*.v - verilog, \*.sv,\*.svh -system verilog, \*.vhd - vhdl, \*.xdc - XDC)
        :param serializer: serializer which specifies target HDL language
        :param target_platform: specifies properties of target platform, like available resources, vendor, etc.
        """
        assert not topUnit._wasSynthetised()
        if not name:
            name = topUnit._getDefaultName()

        super(IpPackager, self).__init__(
            topUnit, name, extra_files)
        self.serializer = serializer_cls
        self.target_platform = target_platform

    @internal
    def toHdlConversion(self, top, topName: str, saveTo: str) -> List[str]:
        """
        :param top: object which is represenation of design
        :param topName: name which should be used for ipcore
        :param saveTo: path of directory where generated files should be stored

        :return: list of file namens in correct compile order
        """
        ser = self.serializer
        name_scope = ser.getBaseNameScope()
        store = SaveToFilesFlat(ser, saveTo, name_scope=name_scope)
        toRtl(top, name=topName, store_manager=store,
              target_platform=self.target_platform)
        return store.files

    @internal
    def paramToIpValue(self, idPrefix: str, g: Param, resolve) -> Value:
        val = Value()
        val.id = idPrefix + g.hdl_name
        if resolve is not VALUE_RESOLVE.NONE:
            val.resolve = resolve
        v = g.get_hdl_value()
        t = v._dtype

        def getVal():
            if v.vld_mask:
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
        elif t == INT:
            val.format = "long"
            val.text = str(getVal())
        elif t == STR:
            val.format = "string"
            val.text = str(g.get_value())
        elif isinstance(t, Bits):
            bitString(v._dtype.bit_length())
        else:
            raise NotImplementedError(
                "Not implemented for datatype %s" % repr(t))
        return val

    @internal
    def getParamPhysicalName(self, p: Param):
        return p.hdl_name

    @internal
    def getParamType(self, p: Param) -> HdlType:
        v = p.get_value()
        if isinstance(v, bool):
            return BOOL
        elif isinstance(v, int):
            return INT
        else:
            return STR

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

        return _to_Vhdl2008_str(hdlType)

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

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Width value can not be converted do ipcore format (%r)",
                val)

        if do_eval:
            val = val.staticEval()
        to_hdl = ToHdlAstVhdl2008()
        to_hdl.createTmpVarFn = createTmpVar
        hdl = to_hdl.as_hdl(val)
        buff = StringIO()
        ser = ToVhdl2008(buff)
        ser.visit_iHdlObj(hdl)
        return buff.getvalue()

    @internal
    def getTypeWidth(self, dtype: HdlType, do_eval=False)\
            -> Tuple[int, Union[int, RtlSignal], bool]:
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

        buff = StringIO()
        ns = VivadoTclExpressionSerializer.getBaseNameScope()
        ser = VivadoTclExpressionSerializer(buff, ns)
        hdl = ser.as_hdl(val)
        ser.visit_iHdlObj(hdl)
        tclVal = buff.getvalue()
        if isinstance(val, RtlSignalBase):
            ser = VivadoTclExpressionSerializer(buff, ns)
            hdl = ser.as_hdl(val.staticEval())
            ser.visit_iHdlObj(hdl)
            tclValVal = buff.getvalue()

            return tclVal, tclValVal, False
        else:
            return tclVal, tclVal, True
