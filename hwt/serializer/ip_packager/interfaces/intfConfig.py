from typing import List

from hwt.hdl.constants import INTF_DIRECTION
from hwt.serializer.ip_packager.exprSerializer import VivadoTclExpressionSerializer
from hwt.serializer.ip_packager.helpers import mkSpiElm, spi_ns_prefix
from hwt.serializer.ip_packager.otherXmlObjs import Parameter
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


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
        self.map = {}
        self.name = None
        self.quartus_map = None

    def get_quartus_map(self):
        if self.quartus_map is None:
            return self.map
        else:
            return self.quartus_map

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

        p = self.addSimpleParam(thisIntf, "ADDR_WIDTH",
                                VivadoTclExpressionSerializer.asHdl(
                                    value.staticEval(), ctx))
        if isinstance(value, RtlSignalBase):
            p.value.resolve = "user"

    def postProcess(self, component, entity, allInterfaces, thisIf):
        pass

    def quartus_tcl_add_interface(self, buff, thisIntf, intfClsName):
        if thisIntf._direction == INTF_DIRECTION.MASTER:
            dir_ = "start"
        else:
            dir_ = "end"

        buff.extend(["add_interface %s %s %s" %
                     (intfClsName, self.name, dir_)])
        self.quartus_prop(buff, "ENABLED", True)
        self.quartus_prop(buff, "EXPORT_OF", "")
        self.quartus_prop(buff, "PORT_NAME_MAP", "")
        self.quartus_prop(buff, "CMSIS_SVD_VARIABLES", "")
        self.quartus_prop(buff, "SVD_ADDRESS_GROUP", "")

    def quartus_prop(self, buff, name, value, escapeStr=True):
        if escapeStr and isinstance(value, str):
            value = '"%s"' % value
        elif isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        buff.append("set_interface_property %s %s %s" %
                    (self.name, name, value))

    def quartus_add_interface_port(self, buff, signal, logicName):
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
            self.name,
            getSignalName(signal),
            logicName,
            dir_,
            width
        ))

    def _asQuartusTcl(self, buff: List[str], version: str,
                      component, entity, allInterfaces, thisIf, intfMapOrName):

        if isinstance(intfMapOrName, str):
            self.quartus_add_interface_port(buff, thisIf, intfMapOrName)
        else:
            for thisIf_ in thisIf._interfaces:
                v = intfMapOrName[thisIf_._name]
                self._asQuartusTcl(buff, version, component, entity,
                                   allInterfaces, thisIf_, v)

    def asQuartusTcl(self, buff, version, component, entity, allInterfaces, thisIf):
        self.quartus_tcl_add_interface(buff, thisIf, getSignalName(thisIf))
        m = self.get_quartus_map()
        if m:
            intfMapOrName = m
        else:
            intfMapOrName = thisIf.name
        self._asQuartusTcl(buff, version, component, entity, allInterfaces,
                           thisIf, intfMapOrName)
