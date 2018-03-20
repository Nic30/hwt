from typing import List, Dict, Union

from hwt.hdl.constants import INTF_DIRECTION
from hwt.serializer.ip_packager.exprSerializer import VivadoTclExpressionSerializer
from hwt.serializer.ip_packager.helpers import mkSpiElm, spi_ns_prefix
from hwt.serializer.ip_packager.otherXmlObjs import Parameter
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.entity import Entity
from hwt.synthesizer.interface import Interface


DEFAULT_CLOCK = 100000000


class Type():
    __slots__ = ['name', 'version', 'vendor', 'library']

    #@classmethod
    # def fromElem(cls, elm):
    #    self = cls()
    #    for s in ['name', 'version', 'vendor', 'library']:
    #        setattr(self, s, elm.attrib[spi_ns_prefix + s])
    #    return self

    def asElem(self, elmName):
        e = mkSpiElm(elmName)
        for s in ['name', 'version', 'vendor', 'library']:
            e.attrib[spi_ns_prefix + s] = getattr(self, s)
        return e


class IntfConfig(Type):
    def __init__(self):
        self.parameters = []

        self.name = None
        self.quartus_name = None

        self.map = {}
        self.quartus_map = None

    def get_quartus_map(self):
        if self.quartus_map is None:
            return self.map
        else:
            return self.quartus_map

    def get_quartus_name(self):
        if self.quartus_name is None:
            return self.name
        else:
            return self.quartus_name

    def addSimpleParam(self, thisIntf, name, value):
        p = Parameter()
        p.name = name
        p.value.resolve = "immediate"
        p.value.id = "BUSIFPARAM_VALUE.%s.%s" % (thisIntf._name.upper(),
                                                 name.upper())
        p.value.text = value
        self.parameters.append(p)
        return p

    def addWidthParam(self, thisIntf, name, value):
        ctx = VhdlSerializer.getBaseContext()

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError(
                "Value of generic %s can not be converted do ipcore format (%r)",
                name, value)
        ctx.createTmpVarFn = createTmpVar

        v = VivadoTclExpressionSerializer.asHdl(value.staticEval(), ctx)
        p = self.addSimpleParam(thisIntf, "ADDR_WIDTH", v)
        if isinstance(value, RtlSignalBase):
            p.value.resolve = "user"

    def postProcess(self, component, entity, allInterfaces, thisIf):
        pass

    def quartus_tcl_add_interface(self, buff, thisIntf):
        """
        Create interface in Quartus TCL

        :return: add_interface command string
        """
        if thisIntf._direction == INTF_DIRECTION.MASTER:
            dir_ = "start"
        else:
            dir_ = "end"

        name = getSignalName(thisIntf)
        buff.extend(["add_interface %s %s %s" %
                     (name, self.get_quartus_name(), dir_)])

        self.quartus_prop(buff, name, "ENABLED", True)
        self.quartus_prop(buff, name, "EXPORT_OF", "")
        self.quartus_prop(buff, name, "PORT_NAME_MAP", "")
        self.quartus_prop(buff, name, "CMSIS_SVD_VARIABLES", "")
        self.quartus_prop(buff, name, "SVD_ADDRESS_GROUP", "")

    def quartus_prop(self, buff: List[str], intfName: str, name: str, value,
                     escapeStr=True):
        """
        Set property on interface in Quartus TCL

        :param buff: line buffer for output
        :param intfName: name of interface to set property on
        :param name: property name
        :param value: property value
        :param escapeStr: flag, if True put string properties to extra ""
        """
        if escapeStr and isinstance(value, str):
            value = '"%s"' % value
        elif isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        buff.append("set_interface_property %s %s %s" %
                    (intfName, name, value))

    def quartus_add_interface_port(self, buff: List[str], intfName: str, signal,
                                   logicName: str):
        """
        Add subinterface to Quartus interface

        :param buff: line buffer for output
        :param intfName: name of top interface
        :param signal: subinterface to create port for
        :param logicName: name of port in Quartus
        """
        d = signal._direction
        if d == INTF_DIRECTION.MASTER:
            dir_ = "Input"
        elif d == INTF_DIRECTION.SLAVE:
            dir_ = "Output"
        else:
            raise ValueError(d)

        width = signal._dtype.width
        if isinstance(width, int):
            width = str(width)
        else:
            ctx = VhdlSerializer.getBaseContext()

            def createTmpVar(suggestedName, dtype):
                raise NotImplementedError(
                    "Width value can not be converted do ipcore format (%r)",
                    width)
            ctx.createTmpVarFn = createTmpVar
            width = VivadoTclExpressionSerializer.asHdl(
                width.staticEval(), ctx)

        buff.append("add_interface_port %s %s %s %s %s" % (
            intfName,
            signal._sigInside.name,
            logicName,
            dir_,
            width
        ))

    def _asQuartusTcl(self, buff: List[str], version: str, intfName: str,
                      component, entity: Entity, allInterfaces: List[Interface],
                      thisIf: Interface, intfMapOrName: Dict[str, Union[Dict, str]]):
        """
        Add interface to Quartus tcl by specified name map

        :param buff: line buffer for output
        :param version: Quartus version
        :param intfName: name of top interface
        :param component: component object from ipcore generator
        :param entity: Entity instance of top unit
        :param allInterfaces: list of all interfaces of top unit
        :param thisIf: interface to add into Quartus TCL
        :param intfMapOrName: Quartus name string for this interface
            or dictionary to map subinterfaces
        """

        if isinstance(intfMapOrName, str):
            self.quartus_add_interface_port(
                buff, intfName, thisIf, intfMapOrName)
        else:
            for thisIf_ in thisIf._interfaces:
                v = intfMapOrName[thisIf_._name]
                self._asQuartusTcl(buff, version, intfName, component, entity,
                                   allInterfaces, thisIf_, v)

    def asQuartusTcl(self, buff: List[str], version: str, component,
                     entity: Entity, allInterfaces: List[Interface],
                     thisIf: Interface):
        """
        Add interface to Quartus tcl

        :param buff: line buffer for output
        :param version: Quartus version
        :param intfName: name of top interface
        :param component: component object from ipcore generator
        :param entity: Entity instance of top unit
        :param allInterfaces: list of all interfaces of top unit
        :param thisIf: interface to add into Quartus TCL
        """
        self.quartus_tcl_add_interface(buff, thisIf)
        m = self.get_quartus_map()
        if m:
            intfMapOrName = m
        else:
            intfMapOrName = thisIf.name
        self._asQuartusTcl(buff, version, getSignalName(thisIf), component,
                           entity, allInterfaces, thisIf, intfMapOrName)
