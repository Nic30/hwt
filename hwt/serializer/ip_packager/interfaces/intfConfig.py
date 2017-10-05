from hwt.serializer.ip_packager.exprSerializer import VivadoTclExpressionSerializer
from hwt.serializer.ip_packager.helpers import mkSpiElm, spi_ns_prefix
from hwt.serializer.ip_packager.otherXmlObjs import Parameter
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


DEFAULT_CLOCK = 100000000


class Type():
    __slots__ = ['name', 'version', 'vendor', 'library']

    #@classmethod
    #def fromElem(cls, elm):
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

    def addSimpleParam(self, thisIntf, name, value):
        p = Parameter()
        p.name = name
        p.value.resolve = "immediate"
        p.value.id = "BUSIFPARAM_VALUE." + thisIntf._name.upper() + "." + name.upper()
        p.value.text = value
        self.parameters.append(p)
        return p

    def addWidthParam(self, thisIntf, name, value):
        ctx = VhdlSerializer.getBaseContext()

        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError("Value of generic %s can not be converted do ipcore format (%s)", name, repr(value))
        ctx.createTmpVarFn = createTmpVar

        p = self.addSimpleParam(thisIntf, "ADDR_WIDTH",
                                VivadoTclExpressionSerializer.asHdl(value.staticEval(), ctx))
        if isinstance(value, RtlSignalBase):
            p.value.resolve = "user"

    def postProcess(self, component, entity, allInterfaces, thisIf):
        pass
