from typing import Tuple, Union, Optional, List

from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct, HStructField, HStructFieldMeta
from hwt.interfaces.agents.structIntf import StructIntfAgent
from hwt.interfaces.std import Signal, VldSynced, RegCntrl, BramPort_withoutClk
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pycocotb.hdlSimulator import HdlSimulator


class StructIntf(Interface):
    """
    Create dynamic interface based on HStruct or HUnion description

    :ivar ~._fieldsToInterfaces: dictionary {field_path: sub interface for it}
        field path is a tuple of HStructFields which leads to this interface
    :ivar ~._structT: HStruct instance used as template for this interface
    :param _instantiateFieldFn: function(FieldTemplateItem instance)
        return interface instance
    """

    def __init__(self, structT: HStruct,
                 field_path: Tuple[Union[HStructField, int], ...],
                 instantiateFieldFn,
                 masterDir=DIRECTION.OUT,
                 loadConfig=True):
        Interface.__init__(self,
                           masterDir=masterDir,
                           loadConfig=loadConfig)
        if not field_path:
            field_path = (structT, )
        self._field_path = field_path
        self._structT = structT
        self._instantiateFieldFn = instantiateFieldFn
        self._fieldsToInterfaces = {}

    def _declr(self):
        _t = self._structT
        if isinstance(_t, HStruct):
            fields = _t.fields
        else:
            fields = _t.fields.values()

        self._fieldsToInterfaces[self._field_path] = self

        for field in fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                intf = self._instantiateFieldFn(self, field)
                assert field not in self._fieldsToInterfaces, field
                self._fieldsToInterfaces[(*self._field_path, field)] = intf
                setattr(self, field.name, intf)

                if isinstance(intf, StructIntf):
                    intf._fieldsToInterfaces = self._fieldsToInterfaces

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = StructIntfAgent(sim, self)


class IntfMap(list):
    """
    Container of interface map

    Items can be Interface/RtlSignal or (type/interface/None/IntfMap, name).
    None is used for padding.
    """
    pass


@internal
def _HTypeFromIntfMap(intf):
    name = getSignalName(intf)
    if isinstance(intf, (RtlSignalBase, Signal)):
        dtype = intf._dtype
    elif isinstance(intf, VldSynced):
        dtype = intf.data._dtype
    elif isinstance(intf, RegCntrl):
        dtype = intf.din._dtype
    elif isinstance(intf, BramPort_withoutClk):
        dtype = Bits(int(intf.DATA_WIDTH))[2 ** int(intf.ADDR_WIDTH)]
    else:
        dtype, name = intf
        assert isinstance(dtype, HdlType)
        assert isinstance(name, str)

    return (dtype, name)


@internal
def HTypeFromIntfMapItem(
        interfaceMapItem: Union[Tuple[HdlType, Optional[str]],
                                Tuple[Union[Interface, RtlSignalBase], str],
                                Tuple[List[Union[Interface, RtlSignalBase]], str],
                                Union[Interface, RtlSignalBase]]):
    isTerminal = False
    if isinstance(interfaceMapItem, (InterfaceBase, RtlSignalBase)):
        dtype, nameOrPrefix = _HTypeFromIntfMap(interfaceMapItem)
        isTerminal = True
    else:
        typeOrListOfInterfaces, nameOrPrefix = interfaceMapItem

        if isinstance(typeOrListOfInterfaces, list) and \
                not isinstance(typeOrListOfInterfaces, IntfMap):
            # list of HType instances for array
            parts = []
            arrayItem_t = None

            for item in typeOrListOfInterfaces:
                if isinstance(item, IntfMap):
                    t = HTypeFromIntfMap(item)
                else:
                    t = HTypeFromIntfMapItem(item).dtype
                if arrayItem_t is None:
                    arrayItem_t = t
                else:
                    assert arrayItem_t == t, (
                        "all items in array has to have same type", arrayItem_t, t)
                parts.append(t)

            dtype = arrayItem_t[len(parts)]

        elif isinstance(typeOrListOfInterfaces, HdlType):
            dtype = typeOrListOfInterfaces
            isTerminal = True
        elif isinstance(typeOrListOfInterfaces,
                        (InterfaceBase, RtlSignalBase)):
            # renamed interface, ignore original name
            dtype = _HTypeFromIntfMap(typeOrListOfInterfaces)[0]
            isTerminal = True
        elif isinstance(typeOrListOfInterfaces, IntfMap):
            dtype = HTypeFromIntfMap(typeOrListOfInterfaces)
        else:
            # tuple (tuple of interfaces, prefix)
            assert isinstance(typeOrListOfInterfaces,
                              tuple), typeOrListOfInterfaces
            dtype = HTypeFromIntfMap(typeOrListOfInterfaces)

    assert isinstance(nameOrPrefix, str) or nameOrPrefix is None, nameOrPrefix

    f = HStructField(dtype, nameOrPrefix)

    if not isTerminal:
        f.meta = HStructFieldMeta(split=True)

    return f


def HTypeFromIntfMap(interfaceMap: IntfMap) -> HStruct:
    """
    Generate flattened register map for HStruct

    :param interfaceMap: sequence of
        a tuple (HdlType, name) (will create HStructField) or
        a tuple (HdlType, None) (will create HStructField as padding) or
        a tuple (list of Interface instances, name) (will create HStructField of HStruct type) or
        an Interface instance (will create a HStructField for an interface, with a name of interface)
    :param DATA_WIDTH: width of word
    :param terminalNodes: None or set whre are placed StructField instances
        which are derived directly from interface
    :return: generator of tuple (type, name, BusFieldInfo)
    """
    structFields = []

    for m in interfaceMap:
        f = HTypeFromIntfMapItem(m)
        structFields.append(f)

    return HStruct(*structFields)
