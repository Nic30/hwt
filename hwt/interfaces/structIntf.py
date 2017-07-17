from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.typeShortcuts import vecT
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.struct import HStruct, HStructField
from hwt.interfaces.std import Signal, VldSynced, RegCntrl, BramPort_withoutClk
from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class StructIntf(Interface):
    """
    Create dynamic interface based on HStruct description

    :ivar _fieldsToInterfaces: dictionary {field from HStruct template: sub interface for it}
    """
    def __init__(self, structT, instantiateFieldFn, masterDir=DIRECTION.OUT, asArraySize=None, loadConfig=True):
        """
        :param structT: HStruct instance used as template for this interface
        :param instantiateFieldFn: function(FieldTemplateItem instance) used to instantiate fields
            (is called only on fields which have different type than HStruct)
        """
        Interface.__init__(self,
                           masterDir=masterDir,
                           asArraySize=asArraySize,
                           loadConfig=loadConfig)

        self._structT = structT
        self._instantiateFieldFn = instantiateFieldFn
        self._fieldsToInterfaces = {}

    def _declr(self):
        for field in self._structT.fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                t = field.dtype
                if isinstance(t, HStruct):
                    intf = StructIntf(t, self._instantiateFieldFn)
                else:
                    intf = self._instantiateFieldFn(self, field)

                self._fieldsToInterfaces[field] = intf
                setattr(self, field.name, intf)

                if isinstance(intf, StructIntf):
                    intf._fieldsToInterfaces = self._fieldsToInterfaces

    def _getSimAgent(self):
        from hwt.interfaces.agents.structIntf import StructIntfAgent
        return StructIntfAgent


def _HTypeFromIntfMap(intf):
    name = getSignalName(intf)
    if isinstance(intf, (RtlSignalBase, Signal)):
        dtype = intf._dtype
    elif isinstance(intf, VldSynced):
        dtype = intf.data._dtype
    elif isinstance(intf, RegCntrl):
        dtype = intf.din._dtype
    elif isinstance(intf, BramPort_withoutClk):
        dtype = vecT(int(intf.DATA_WIDTH))[2 ** int(intf.ADDR_WIDTH)]
    else:
        dtype, name = intf
        assert isinstance(dtype, HdlType)
        assert isinstance(name, str)

    return (dtype, name)


def HTypeFromIntfMap(interfaceMap, terminalNodes=None):
    """
    Generate flattened register map for HStruct

    :param interfaceMap: sequence of
        tuple (type, name) or (will create standard struct field member)
        interface or (will create a struct field from interface)
        instance of hdl type (is used as padding) 
        tuple (list of interface, name)
    :param DATA_WIDTH: width of word
    :param terminalNodes: None or set whre are placed StructField instances which are derived
        directly from interface
    :return: generator of tuple (type, name, BusFieldInfo)
    """
    structFields = []

    for m in interfaceMap:
        if isinstance(m, (InterfaceBase, RtlSignalBase)):
            f = HStructField(*_HTypeFromIntfMap(m))
            if terminalNodes is not None:
                terminalNodes.add(f)
            structFields.append(f)

        elif isinstance(m, HdlType):
            # padding value
            structFields.append((m, None))

        else:
            typeOrListOfInterfaces, nameOrPrefix = m

            if isinstance(typeOrListOfInterfaces, list):
                # tuple (list or items, name of this array)
                types = []
                reference = None
    
                for item in typeOrListOfInterfaces:
                    if isinstance(item, (list, map, tuple)):
                        if (isinstance(interfaceMap, tuple) and
                            len(interfaceMap) == 2 and
                            isinstance(interfaceMap[1], str)):
                            t, _ = _HTypeFromIntfMap(item)
                        else:
                            t = HTypeFromIntfMap(item)
                    else:
                        t, _ = _HTypeFromIntfMap(item)

                    types.append(t)
                    if reference is None:
                        reference = t
                    else:
                        assert reference == t, ("all items in array has to have same type")

                dtype = reference[len(types)]
            
            elif isinstance(typeOrListOfInterfaces, HdlType):
                dtype = typeOrListOfInterfaces
            else:
                # tuple (tuple of interfaces, prefix)
                try:
                    assert isinstance(typeOrListOfInterfaces, tuple), typeOrListOfInterfaces
                except AssertionError as e:
                    raise e
                dtype = HTypeFromIntfMap(typeOrListOfInterfaces)
            structFields.append((dtype, nameOrPrefix))

    return HStruct(*structFields)
