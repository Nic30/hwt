from io import StringIO
import math
from typing import List, Tuple, Union

from hdlConvertorAst.hdlAst import HdlValueId
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.to.vhdl.vhdl2008 import ToVhdl2008
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call
from hwt.doc_markers import internal
from hwt.hwIO import HwIO
from hwt.hwModule import HwModule
from hwt.hwParam import HwParam
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, STR, BIT, INT
from hwt.hdl.types.hdlType import HdlType
from hwt.mainBases import RtlSignalBase
from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.vhdl import Vhdl2008Serializer, ToHdlAstVhdl2008
from hwt.synth import to_rtl
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.interfaceLevel.hwModuleImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from ipCorePackager.intfIpMeta import VALUE_RESOLVE
from ipCorePackager.otherXmlObjs import Value
from ipCorePackager.packager import IpCorePackager


class ToHdlAstVivadoTclExpr(ToHdlAstVhdl2008):
    _spirit_decode = HdlValueId("spirit:decode")
    _id = HdlValueId("id")

    def as_hdl_SignalItem(self, si, declaration=False):
        assert(declaration == False)
        if si.hidden:
            assert si.origin is not None, si
            return self.as_hdl(si.origin)
        else:
            id_ = hdl_call(self._id, [f'MODELPARAM_VALUE.{si.name}'])
            return hdl_call(self._spirit_decode, [id_])


class IpPackager(IpCorePackager):
    """
    IP-core packager

    :summary: Packs HDL, constraint and other files to IP-Core package
        for distribution and simple integration

    """

    def __init__(self, topHwModule: HwModule, name: str=None,
                 extra_files: List[str]=[],
                 serializer_cls=Vhdl2008Serializer,
                 target_platform=DummyPlatform()):
        """
        :param topObj: :class:`hwt.hwModule.HwModule` instance of top component
        :param name: optional name of top
        :param extra_files: list of extra HDL/constrain file names for files
            which should be distributed in this IP-core
            (\*.v - verilog, \*.sv,\*.svh -system verilog, \*.vhd - vhdl, \*.xdc - XDC)
        :param serializer: serializer which specifies target HDL language
        :param target_platform: specifies properties of target platform, like available resources, vendor, etc.
        """
        if not name:
            name = topHwModule._getDefaultName()

        super(IpPackager, self).__init__(
            topHwModule, name, extra_files)
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
        store = SaveToFilesFlat(ser, saveTo)
        to_rtl(top, name=topName, store_manager=store,
              target_platform=self.target_platform)
        return store.files

    @internal
    def paramToIpValue(self, idPrefix: str, g: HdlIdDef, resolve) -> Value:
        val = Value()
        val.id = idPrefix + g.name
        if resolve is not VALUE_RESOLVE.NONE:
            val.resolve = resolve
        v = g.value
        t = g.type

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
            val.text = v.val
        elif isinstance(t, HBits):
            bitString(t.bit_length())
        else:
            raise NotImplementedError(
                f"Not implemented for datatype {t}")
        return val

    @internal
    def getParamPhysicalName(self, p: HdlIdDef):
        return p.name

    @internal
    def getParamType(self, p: HdlIdDef) -> HdlType:
        assert p.type in [INT, BOOL, STR], p
        return p.type

    @internal
    def iterParams(self, module: HwModule):
        return module._ctx.ent.params

    @internal
    def iterInterfaces(self, top: HwModule):
        return top._hwIOs

    @internal
    def serializeType(self, hdlType: HdlType) -> str:
        """
        :see: doc of method on parent class
        """
        buff = StringIO()
        to_ast = ToHdlAstVhdl2008()
        hdl = to_ast.as_hdl_HdlType(hdlType)
        ser = ToVhdl2008(buff)
        ser.visit_iHdlObj(hdl)
        return buff.getvalue()

    @internal
    def getVectorFromType(self, dtype) -> Union[bool, None, Tuple[int, int]]:
        """
        :see: doc of method on parent class
        """
        if dtype == BIT:
            return False
        elif isinstance(dtype, HBits):
            return [dtype.bit_length() - 1, INT.from_py(0)]

    @internal
    def getInterfaceType(self, hwIO: HwIO) -> HdlType:
        """
        :see: doc of method on parent class
        """
        return hwIO._dtype

    @internal
    def getInterfaceLogicalName(self, hwIO: HwIO):
        """
        :see: doc of method on parent class
        """
        return getSignalName(hwIO)

    @internal
    def getInterfacePhysicalName(self, hwIO: HwIO):
        """
        :see: doc of method on parent class
        """
        return hwIO._sigInside.name

    @internal
    def getInterfaceDirection(self, thisHwIO: HwIO):
        """
        :see: doc of method on parent class
        """
        return thisHwIO._direction

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
    def getObjDebugName(self, obj: Union[HwIO, HwModule, HwParam]) -> str:
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
            val = INT.from_py(val)
        if do_eval:
            val = val.staticEval()

        buff = StringIO()
        to_hdl = ToHdlAstVivadoTclExpr()
        ser = Vhdl2008Serializer.TO_HDL(buff)

        hdl = to_hdl.as_hdl(val)
        ser.visit_iHdlObj(hdl)
        tclVal = buff.getvalue()

        if isinstance(val, RtlSignalBase):
            buff = StringIO()
            hdl = to_hdl.as_hdl(val.staticEval())
            ser = Vhdl2008Serializer.TO_HDL(buff)
            ser.visit_iHdlObj(hdl)
            tclValVal = buff.getvalue()

            return tclVal, tclValVal, False
        else:
            return tclVal, tclVal, True
