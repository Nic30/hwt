from typing import Union, Tuple, Optional, List

from hwt.doc_markers import internal
from hwt.hwIO import HwIO
from hwt.hwIOs.std import HwIOBramPort_noClk, HwIORegCntrl, HwIODataVld, HwIOSignal
from hwt.hwIOs.hwIOStruct import HwIOStruct
from hwt.hwIOs.hwIOUnion import HwIOUnionSink, HwIOUnionSource
from hwt.hObjList import HObjList
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct, HStructFieldMeta, HStructField
from hwt.mainBases import HwIOBase
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.interfaceLevel.hwModuleImplHelpers import getSignalName
from hwt.synthesizer.typePath import TypePath


class HwIOObjMap(List["HwIoMapItem"]):
    """
    Container of interface map. The interface map object describes
    the data type using existing HwIO instances.

    Items can be HwIO/RtlSignal or (type/interface/None/HwIOObjMap, name).
    None is used for padding.
    """
    pass


HwIoMapCompatibleHwIO = Union[
    RtlSignalBase,
    HwIODataVld,
    HwIORegCntrl,
    HwIOBramPort_noClk,
    HwIOStruct,
    HwIOUnionSink,
    HwIOUnionSource,
]
HwIOMapItem =  Union[
    Tuple[HdlType, Optional[str]],
    Tuple[Union[HwIoMapCompatibleHwIO, RtlSignalBase], str],
    Tuple[List[Union[HwIoMapCompatibleHwIO, RtlSignalBase]], str],
    HwIoMapCompatibleHwIO
]


@internal
def _HTypeFromHwIOObjMap(hwIO: HwIoMapCompatibleHwIO):
    name = getSignalName(hwIO)
    if isinstance(hwIO, (RtlSignalBase, HwIOSignal)):
        dtype = hwIO._dtype
    elif isinstance(hwIO, HwIODataVld):
        dtype = hwIO.data._dtype
    elif isinstance(hwIO, HwIORegCntrl):
        dtype = hwIO.din._dtype
    elif isinstance(hwIO, HwIOBramPort_noClk):
        dtype = HBits(int(hwIO.DATA_WIDTH))[2 ** int(hwIO.ADDR_WIDTH)]
    else:
        raise ValueError(hwIO)

    return (dtype, name)


@internal
def HTypeFromHwIOObjMapItem(hwIOMapItem: HwIOMapItem):
    isTerminal = False
    if isinstance(hwIOMapItem, (HwIOBase, RtlSignalBase)):
        dtype, nameOrPrefix = _HTypeFromHwIOObjMap(hwIOMapItem)
        isTerminal = True
    else:
        typeOrListOfHwIOs, nameOrPrefix = hwIOMapItem

        if isinstance(typeOrListOfHwIOs, list) and \
                not isinstance(typeOrListOfHwIOs, HwIOObjMap):
            # list of HType instances for array
            parts = []
            arrayItem_t = None

            for item in typeOrListOfHwIOs:
                if isinstance(item, HwIOObjMap):
                    t = HTypeFromHwIOObjMap(item)
                else:
                    t = HTypeFromHwIOObjMapItem(item).dtype
                if arrayItem_t is None:
                    arrayItem_t = t
                else:
                    assert arrayItem_t == t, (
                        "all items in array has to have same type", arrayItem_t, t)
                parts.append(t)

            dtype = arrayItem_t[len(parts)]

        elif isinstance(typeOrListOfHwIOs, HdlType):
            dtype = typeOrListOfHwIOs
            isTerminal = True
        elif isinstance(typeOrListOfHwIOs,
                        (HwIOBase, RtlSignalBase)):
            # renamed interface, ignore original name
            dtype = _HTypeFromHwIOObjMap(typeOrListOfHwIOs)[0]
            isTerminal = True
        elif isinstance(typeOrListOfHwIOs, HwIOObjMap):
            dtype = HTypeFromHwIOObjMap(typeOrListOfHwIOs)
        else:
            # tuple (tuple of interfaces, prefix)
            assert isinstance(typeOrListOfHwIOs,
                              tuple), typeOrListOfHwIOs
            dtype = HTypeFromHwIOObjMap(typeOrListOfHwIOs)

    assert isinstance(nameOrPrefix, str) or nameOrPrefix is None, nameOrPrefix
    assert isinstance(dtype, HdlType)

    f = HStructField(dtype, nameOrPrefix)

    if not isTerminal:
        f.meta = HStructFieldMeta(split=True)

    return f


def HTypeFromHwIOObjMap(hwIOMap: HwIOObjMap) -> HStruct:
    """
    Generate flattened register map for HStruct

    :param hwIOMap: sequence of
        a tuple (HdlType, name) (will create HStructField) or
        a tuple (HdlType, None) (will create HStructField as padding) or
        a tuple (list of HwIO instances, name) (will create HStructField of HStruct type) or
        an HwIO instance (will create a HStructField for an interface, with a name of interface)
    :param DATA_WIDTH: width of word
    :param terminalNodes: None or set where are placed StructField instances
        which are derived directly from interface
    :return: generator of tuple (type, name, BusFieldInfo)
    """
    structFields = []

    for m in hwIOMap:
        f = HTypeFromHwIOObjMapItem(m)
        structFields.append(f)

    return HStruct(*structFields)


def isPaddingInHwIOObjMap(item: Union[HdlType, Tuple[object, Optional[str]]]):
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


def _walkHwIOStructAndHwIOObjMap_unpack(io: Union[HObjList, HwIOStruct, HwIOUnionSink, HwIOUnionSource], hwIOMap):
    """
    Try to unpack hwIOMap and apply the selection on io

    :return: Optional tuple HwIO, hwIOMap
    """
    # items are HwIO/RtlSignal or (type/interface/None or list of items, name)
    if isPaddingInHwIOObjMap(hwIOMap):
        return
    elif isinstance(hwIOMap, tuple):
        item, name = hwIOMap
    else:
        item = hwIOMap
        assert isinstance(item, (HwIOBase, RtlSignalBase)), item
        name = getSignalName(item)

    if isinstance(item, HdlType):
        # this part of io was generated from type descriptin
        # and we are re searching only for those parts which were generated
        # from HwIO/RtlSignal
        return

    return getattr(io, name), item


def walkHwIOStructAndHwIOObjMap(io: Union[HObjList, HwIOStruct, HwIOUnionSink, HwIOUnionSource], hwIOMap):
    """
    Walk HwIOStruct and interface map
    and yield tuples (HwIO in HwIOStruct, interface in hwIOMap)
    which are on same place

    :param io: an interface to walk
    :param hwIOMap: interface map

    :note: typical usecase is when there is HwIOStruct generated from description in hwIOMap
        and then you need to connect interface from hwIOMap to io
        and there you can use this function to iterate over interfaces which belongs together
    """

    if isinstance(hwIOMap, (HwIOBase, RtlSignalBase)):
        yield io, hwIOMap
        return
    elif isinstance(hwIOMap, tuple):
        item = _walkHwIOStructAndHwIOObjMap_unpack(io, hwIOMap)
        if item is None:
            # is padding or there is no interface specified for it in hwIOMap
            return
        else:
            io, item = item
            yield from walkHwIOStructAndHwIOObjMap(io, item)
    elif isinstance(io, list):
        io
        assert len(io) == len(hwIOMap)
        for sItem, item in zip(io, hwIOMap):
            yield from walkHwIOStructAndHwIOObjMap(sItem, item)
    else:
        assert isinstance(hwIOMap, HwIOObjMap), hwIOMap
        for item in hwIOMap:
            _item = _walkHwIOStructAndHwIOObjMap_unpack(io, item)
            if _item is not None:
                sItem, _item = _item
                yield from walkHwIOStructAndHwIOObjMap(sItem, _item)


def HwIOObjMapItem_find_by_name(hwIOMapItem, name: str):
    if isinstance(hwIOMapItem, HStructField):
        hwIOMapItem = hwIOMapItem.dtype
    if isinstance(hwIOMapItem, HwIOObjMap):
        for x in hwIOMapItem:
            if isinstance(x, HwIOBase):
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
    elif isinstance(hwIOMapItem, HStruct):
        for f in hwIOMapItem.fields:
            if f.name == name:
                return f
        raise KeyError(name)
    else:
        raise NotImplementedError(hwIOMapItem)


def HwIOObjMap_get_by_field_path(root: HwIOObjMap, field_path: TypePath):
    actual = root
    # find in interfaceMap, skip first because it is the type itself
    for rec in field_path:
        # if isinstance(rec, (HwIOBase, RtlSignalBase)):
        #    shouldEnter, shouldUse = False, True
        #    return shouldEnter, shouldUse
        if isinstance(rec, int):
            actual = actual[rec]
        elif isinstance(rec, str):
            actual = HwIOObjMapItem_find_by_name(actual, rec)
        else:
            raise NotImplementedError(rec)
    return  actual

