from typing import Union, Tuple, Optional, List

from hwt.doc_markers import internal
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct, HStructFieldMeta, HStructField
from hwt.interfaces.std import BramPort_withoutClk, RegCntrl, VldSynced, Signal
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.typePath import TypePath


class IntfMap(list):
    """
    Container of interface map. The interface map object describes
    the data type using existing interface instances.

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
    assert isinstance(dtype, HdlType)

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


def isPaddingInIntfMap(item):
    if isinstance(item, HdlType):
        return True
    else:
        try:
            if isinstance(item, tuple):
                _item, name = item
                if name is None:
                    return True
        except ValueError:
            pass

    return False


def _walkStructIntfAndIntfMap_unpack(structIntf, intfMap):
    """
    Try to unpack intfMap and apply the selection on structIntf

    :return: Optional tuple Interface, intfMap
    """
    # items are Interface/RtlSignal or (type/interface/None or list of items, name)
    if isPaddingInIntfMap(intfMap):
        return
    elif isinstance(intfMap, tuple):
        item, name = intfMap
    else:
        item = intfMap
        assert isinstance(item, (InterfaceBase, RtlSignalBase)), item
        name = getSignalName(item)

    if isinstance(item, HdlType):
        # this part of structIntf was generated from type descriptin
        # and we are re searching only for those parts which were generated
        # from Interface/RtlSignal
        return

    return getattr(structIntf, name), item


def walkStructIntfAndIntfMap(structIntf, intfMap):
    """
    Walk StructInterfacece and interface map
    and yield tuples (Interface in StructInterface, interface in intfMap)
    which are on same place

    :param structIntf: HObjList or StructIntf or UnionIntf instance
    :param intfMap: interface map

    :note: typical usecase is when there is StructIntf generated from description in intfMap
        and then you need to connect interface from intfMap to structIntf
        and there you can use this function to iterate over interfaces which belongs together
    """

    if isinstance(intfMap, (InterfaceBase, RtlSignalBase)):
        yield structIntf, intfMap
        return
    elif isinstance(intfMap, tuple):
        item = _walkStructIntfAndIntfMap_unpack(structIntf, intfMap)
        if item is None:
            # is padding or there is no interface specified for it in intfMap
            return
        else:
            structIntf, item = item
            yield from walkStructIntfAndIntfMap(structIntf, item)
    elif isinstance(structIntf, list):
        structIntf
        assert len(structIntf) == len(intfMap)
        for sItem, item in zip(structIntf, intfMap):
            yield from walkStructIntfAndIntfMap(sItem, item)
    else:
        assert isinstance(intfMap, IntfMap), intfMap
        for item in intfMap:
            _item = _walkStructIntfAndIntfMap_unpack(structIntf, item)
            if _item is not None:
                sItem, _item = _item
                yield from walkStructIntfAndIntfMap(sItem, _item)

def IntfMapItem_find_by_name(intf_map_item, name):
    if isinstance(intf_map_item, HStructField):
        intf_map_item = intf_map_item.dtype
    if isinstance(intf_map_item, IntfMap):
        for x in intf_map_item:
            if isinstance(x, InterfaceBase):
                if x._name == name:
                    return x
            elif isinstance(x, RtlSignalBase):
                if x.name == name:
                    return x
            else:
                v, n = x
                if n == name:
                    return v
        raise KeyError(name)
    elif isinstance(intf_map_item, HStruct):
        for f in intf_map_item.fields:
            if f.name == name:
                return f
        raise KeyError(name)
    else:
        raise NotImplementedError(intf_map_item)

def IntfMap_get_by_field_path(root: IntfMap, field_path: TypePath):
    actual = root
    # find in interfaceMap, skip first because it is the type itself
    for rec in field_path:
        #if isinstance(rec, (InterfaceBase, RtlSignalBase)):
        #    shouldEnter, shouldUse = False, True
        #    return shouldEnter, shouldUse
        if isinstance(rec, int):
            actual = actual[rec]
        elif isinstance(rec, str):
            actual = IntfMapItem_find_by_name(actual, rec)
        else:
            raise NotImplementedError(rec)
    return  actual

