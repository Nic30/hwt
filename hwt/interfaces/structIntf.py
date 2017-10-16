from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct, HStructField, HStructFieldMeta
from hwt.interfaces.agents.structIntf import StructIntfAgent
from hwt.interfaces.std import Signal, VldSynced, RegCntrl, BramPort_withoutClk
from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class StructIntf(Interface):
    """
    Create dynamic interface based on HStruct or HUnion description

    :ivar _fieldsToInterfaces: dictionary {field from HStruct template:
        sub interface for it}
    :ivar _structT: HStruct instance used as template for this interface
    :param _instantiateFieldFn: function(FieldTemplateItem instance)
        return interface instance
    """

    def __init__(self, structT, instantiateFieldFn,
                 masterDir=DIRECTION.OUT, asArraySize=None,
                 loadConfig=True):
        Interface.__init__(self,
                           masterDir=masterDir,
                           asArraySize=asArraySize,
                           loadConfig=loadConfig)
        self._structT = structT
        self._instantiateFieldFn = instantiateFieldFn
        self._fieldsToInterfaces = {}

    def _declr(self):
        _t = self._structT
        if isinstance(_t, HStruct):
            fields = _t.fields
        else:
            fields = _t.fields.values()

        self._fieldsToInterfaces[self._structT] = self

        for field in fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                intf = self._instantiateFieldFn(self, field)
                self._fieldsToInterfaces[field] = intf
                setattr(self, field.name, intf)

                if isinstance(intf, StructIntf):
                    intf._fieldsToInterfaces = self._fieldsToInterfaces

    def _initSimAgent(self):
        self._ag = StructIntfAgent(self)


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


def isIntfMap(intfMap):
    if not isinstance(intfMap, tuple):
        return False
    elif len(intfMap) == 2 and (intfMap[1] is None
                                or isinstance(intfMap, str)):
        return False
    else:
        return True


def HTypeFromIntfMapItem(interfaceMapItem):
    isTerminal = False
    if isinstance(interfaceMapItem, (InterfaceBase, RtlSignalBase)):
        dtype, nameOrPrefix = _HTypeFromIntfMap(interfaceMapItem)
        isTerminal = True
    else:
        typeOrListOfInterfaces, nameOrPrefix = interfaceMapItem

        if isinstance(typeOrListOfInterfaces, list):
            # tuple (list or items, name of this array)
            types = []
            reference = None

            for item in typeOrListOfInterfaces:
                if isIntfMap(item):
                    t = HTypeFromIntfMap(item)
                else:
                    f = HTypeFromIntfMapItem(item)
                    t = f.dtype

                types.append(t)
                if reference is None:
                    reference = t
                else:
                    assert reference == t, (
                        "all items in array has to have same type")

            dtype = reference[len(types)]

        elif isinstance(typeOrListOfInterfaces, HdlType):
            dtype = typeOrListOfInterfaces
            isTerminal = True
        elif isinstance(typeOrListOfInterfaces,
                        (InterfaceBase, RtlSignalBase)):
            # renamed interface, ignore original name
            dtype = _HTypeFromIntfMap(typeOrListOfInterfaces)[0]
            isTerminal = True

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


def HTypeFromIntfMap(interfaceMap):
    """
    Generate flattened register map for HStruct

    :param interfaceMap: sequence of
        tuple (type, name) or (will create standard struct field member)
        interface or (will create a struct field from interface)
        instance of hdl type (is used as padding)
        tuple (list of interface, name)
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
