from copy import copy
from typing import Optional, Union, Set

from hwt.code import And, Or
from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.structCast import hstruct_reinterpret
from hwt.hdl.types.structValBase import HStructConstBase
from hwt.hwIO import HwIO
from hwt.hwIOs.agents.rdSync import HwIODataRdAgent
from hwt.hwIOs.agents.rdVldSync import HwIODataRdVldAgent
from hwt.hwIOs.agents.struct import HwIOStructAgent
from hwt.hwIOs.agents.vldSync import HwIODataVldAgent
from hwt.hwIOs.std import HwIODataVld, HwIODataRd, HwIOSignal, HwIORdVldSync
from hwt.hwParam import HwParam
from hwt.pyUtils.typingFuture import override
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.typePath import TypePath
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION


class HwIOStruct(HwIO):
    """
    Create dynamic interface based on HStruct or HUnion description

    :ivar ~._fieldsToHwIOs: dictionary {field_path: sub interface for it}
        field path is a tuple of HStructFields which leads to this interface
    :ivar ~._dtype: HStruct instance used as template for this interface
    :param _instantiateFieldFn: function(FieldTemplateItem instance)
        return HwIO instance
    :attention: _instantiateFieldFn should also share _fieldsToHwIOs
        with all other instances of HwIOStruct on this interface
    """

    def __init__(self, structT: HStruct,
                 field_path: TypePath,
                 instantiateFieldFn,
                 masterDir=DIRECTION.OUT,
                 loadConfig=True):
        HwIO.__init__(self,
                           masterDir=masterDir,
                           loadConfig=loadConfig)
        if not field_path:
            field_path = TypePath()
        else:
            assert isinstance(field_path, TypePath), field_path

        self._field_path = field_path
        self._dtype = structT
        assert self._dtype.fields, "Needs to have at least some members (otherwise this interface is useless)"
        self._instantiateFieldFn = instantiateFieldFn
        self._fieldsToHwIOs = {}

    @override
    def hwDeclr(self):
        _t = self._dtype
        if isinstance(_t, HStruct):
            fields = _t.fields
        else:
            fields = _t.fields.values()

        self._fieldsToHwIOs[self._field_path] = self

        for field in fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                hwIO = self._instantiateFieldFn(self, field)
                p = self._field_path / field.name
                assert p not in self._fieldsToHwIOs, p
                self._fieldsToHwIOs[p] = hwIO

                setattr(self, field.name, hwIO)

    @override
    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOStructAgent(sim, self)

    @override
    def _eq(self, other: Union["HwIOStruct", HStructConstBase]):
        if isinstance(other, self.__class__):
            assert self._dtype == other._dtype
            return And(*(sHwIO._eq(oi) for sHwIO, oi in zip(self._hwIOs, other._hwIOs)))
        else:
            return And(*(sHwIO._eq(getattr(other, sHwIO._name)) for sHwIO in self._hwIOs))

    @override
    def __ne__(self, other: Union["HwIOStruct", HStructConstBase]):
        if isinstance(other, self.__class__):
            assert self._dtype == other._dtype
            return Or(*(sHwIO != oi for sHwIO, oi in zip(self._hwIOs, other._hwIOs)))
        else:
            return Or(*(sHwIO != getattr(other, sHwIO._name) for sHwIO in self._hwIOs))

    @override
    def _reinterpret_cast(self, toT: HdlType):
        return hstruct_reinterpret(self._dtype, self, toT)


class HdlType_to_HwIO():
    """
    Convert instance of HdlType to an interface which represents same data.

    :note: HwIO is only instantiated, that means it does not have sub-interfaces
        loaded yet, it can be done manually or by assigning to a property of parent HwIO/HwModule
        instance.
    """

    def apply(self, dtype: HdlType, field_path: Optional[TypePath]=None, masterDir=DIRECTION.OUT) -> HwIO:
        """
        Run the conversion
        """
        if isinstance(dtype, HStruct):
            return HwIOStruct(dtype, field_path,
                              instantiateFieldFn=self.instantiateFieldFn,
                              masterDir=masterDir)
        elif dtype.isScalar():
            return HwIOSignal(dtype=dtype, masterDir=masterDir)
        elif isinstance(dtype, HArray):
            return HObjList(self.apply(dtype.element_t, masterDir=masterDir)
                            for _ in range(dtype.size))
        else:
            raise NotImplementedError(dtype)

    @internal
    def instantiateFieldFn(self, hwIO, fieldInfo) -> HwIO:
        if isinstance(hwIO, HwIOStruct):
            c = self.apply(
                fieldInfo.dtype,
                field_path=hwIO._field_path / fieldInfo.name)
            c._fieldsToHwIOs = hwIO._fieldsToHwIOs
            return c
        else:
            raise NotImplementedError(hwIO)


class HwIO_to_HdlType():
    """
    Convert instance of HdlType to an interface which represents same data.

    :note: HwIO instance has to have definitions loaded.
    """

    def apply(self, hwIO: Union[HwIO, RtlSignal], const=False, exclude: Optional[Set[HwIO]]=None):
        """
        Run the conversion
        """
        assert exclude is None or hwIO not in exclude
        if isinstance(hwIO, HwIO) and hwIO._hwIOs:
            if exclude is None:
                return HStruct(
                    *((self.apply(sHwIO, const=const), sHwIO._name)
                      for sHwIO in hwIO._hwIOs)
                )
            else:
                return HStruct(
                    *((self.apply(sHwIO, const=const), sHwIO._name)
                      for sHwIO in hwIO._hwIOs if sHwIO not in exclude)
                )
        else:
            t = hwIO._dtype
            if t.const != const:
                t = copy(t)
                t.const = const
            return t


class HwIOStructRd(HwIODataRd):
    """
    A HwIODataRd interface which has a data signal of type specified in configuration of this interface
    """

    @override
    def hwConfig(self):
        self.T: HdlType = HwParam(None)

    @override
    def hwDeclr(self):
        assert isinstance(self.T, HdlType), (self.T, self._name)
        self._dtype = self.T
        self.data = HdlType_to_HwIO().apply(self.T)
        self.rd = HwIOSignal(masterDir=DIRECTION.IN)

    @override
    def _initSimAgent(self, sim:HdlSimulator):
        self._ag = HwIOStructRdAgent(sim, self)


class HwIOStructRdAgent(HwIODataRdAgent):

    def __init__(self, sim:HdlSimulator, hwIO:HwIOStructRd, allowNoReset=False):
        HwIODataRdAgent.__init__(self, sim, hwIO, allowNoReset=allowNoReset)
        hwIO.data._initSimAgent(sim)
        self._data_ag = hwIO.data._ag

    @override
    def set_data(self, data):
        return self._data_ag.set_data(data)

    @override
    def get_data(self):
        return self._data_ag.get_data()


class HwIOStructVld(HwIODataVld):
    """
    A handshaked interface which has a data signal of type specified in configuration of this interface
    """

    def hwConfig(self):
        self.T: HdlType = HwParam(None)

    @override
    def hwDeclr(self):
        assert isinstance(self.T, HdlType), (self.T, self._name)
        self._dtype = self.T
        self.data = HdlType_to_HwIO().apply(self.T)
        self.vld = HwIOSignal()

    @override
    def _initSimAgent(self, sim:HdlSimulator):
        self._ag = HwIOStructVldAgent(sim, self)


class HwIOStructVldAgent(HwIODataVldAgent):

    def __init__(self, sim:HdlSimulator, hwIO:HwIOStructVld, allowNoReset=False):
        HwIODataVldAgent.__init__(self, sim, hwIO, allowNoReset=allowNoReset)
        hwIO.data._initSimAgent(sim)
        self._data_ag = hwIO.data._ag

    @override
    def set_data(self, data):
        return self._data_ag.set_data(data)

    @override
    def get_data(self):
        return self._data_ag.get_data()


class HwIOStructRdVld(HwIORdVldSync):
    """
    A handshaked interface which has a data signal of type specified in configuration of this interface
    """

    @override
    def hwConfig(self):
        self.T: HdlType = HwParam(None)

    @override
    def hwDeclr(self):
        assert isinstance(self.T, HdlType), (self.T, self._name)
        self._dtype = self.T
        self.data = HdlType_to_HwIO().apply(self.T)
        HwIORdVldSync.hwDeclr(self)

    @override
    def _initSimAgent(self, sim:HdlSimulator):
        self._ag = HwIOStructRdVldAgent(sim, self)


class HwIOStructRdVldAgent(HwIODataRdVldAgent):

    def __init__(self, sim:HdlSimulator, hwIO:HwIOStructRdVld, allowNoReset=False):
        HwIODataRdVldAgent.__init__(self, sim, hwIO, allowNoReset=allowNoReset)
        hwIO.data._initSimAgent(sim)
        self._data_ag = hwIO.data._ag

    @override
    def set_data(self, data):
        return self._data_ag.set_data(data)

    @override
    def get_data(self):
        return self._data_ag.get_data()
