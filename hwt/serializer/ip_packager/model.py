from hwt.serializer.ip_packager.exprSerializer import VivadoTclExpressionSerializer
from hwt.serializer.ip_packager.helpers import appendSpiElem, appendStrElements, \
         findS, mkSpiElm, spi_ns_prefix, appendSpiArray
from hwt.serializer.ip_packager.otherXmlObjs import Value
import xml.etree.ElementTree as etree


class FileSetRef():
    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.localName = findS(elm, 'localName').text
        return self
    
    def asElem(self):
        e = etree.Element(spi_ns_prefix + "fileSetRef")
        appendSpiElem(e, "localName").text = self.localName
        return e

class View():
    _requiredVal = ["name", "displayName", "envIdentifier"]
    _optionalVal = ["language", "modelName"]
    
    @classmethod
    def fromElem(cls, elm):
        self = cls()
        for n in self._requiredVal:
            e = findS(elm, n)
            if e is None:
                raise Exception("View is missing " + n)
            setattr(self, n, e.text)
        for n in self._optionalVal:
            e = findS(elm, n)
            if e is None:
                continue
            setattr(self, n, e.text)
        
            
        self.fileSetRef = FileSetRef.fromElem(findS(elm, "fileSetRef"))
        return self
    
    def asElem(self):
        e = mkSpiElm("view")
        appendStrElements(e, self,
                          reqPropNames=self._requiredVal,
                          optPropNames=self._optionalVal)
        e.append(self.fileSetRef.asElem())
        return e

class ModelParameter():
    def __init__(self, name:str, displayName:str, datatype:str, value:Value):
        self.name = name
        self.displayName = displayName
        self.datatype = datatype
        self.value = value
    @classmethod
    def fromGeneric(cls, g):
        val = Value.fromGeneric("MODELPARAM_VALUE.", g, Value.RESOLVE_GENERATED)
        def createTmpVar(suggestedName, dtype):
            raise NotImplementedError("Value of generic %s can not be converted do ipcore format (%s)", g.name, repr(val))
        return cls(g.name,
                   g.name.replace("_", " "),
                   VivadoTclExpressionSerializer.HdlType(g._dtype, createTmpVar).lower(), val)
    
    def asElem(self):
        e = mkSpiElm("modelParameter")
        e.attrib["spirit:dataType"] = self.datatype
        appendStrElements(e, self,
                          reqPropNames=['name', "displayName"])
        e.append(self.value.asElem())
        return e

class Model():
    
    def __init__(self, vhdl_syn_fileSetName, vhdl_sim_fileSetName, tcl_fileSetName):
        self.views = []
        self.ports = []
        self.modelParameters = []
        self.vhdl_syn_fileSetName = vhdl_syn_fileSetName
        self.vhdl_sim_fileSetName = vhdl_sim_fileSetName
        self.tcl_fileSetName = tcl_fileSetName
        
    def addDefaultViews(self, unit):
        viewsTemplate = ("""
       <views xmlns:xilinx="http://www.xilinx.com" xmlns:spirit="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <spirit:view>
        <spirit:name>xilinx_vhdlsynthesis</spirit:name>
        <spirit:displayName>VHDL Synthesis</spirit:displayName>
        <spirit:envIdentifier>vhdlSource:vivado.xilinx.com:synthesis</spirit:envIdentifier>
        <spirit:language>vhdl</spirit:language>
        <spirit:modelName>{0}</spirit:modelName>
        <spirit:fileSetRef>
          <spirit:localName>""" + self.vhdl_syn_fileSetName + """</spirit:localName>
        </spirit:fileSetRef>
      </spirit:view>
      <spirit:view>
        <spirit:name>xilinx_vhdlbehavioralsimulation</spirit:name>
        <spirit:displayName>VHDL Simulation</spirit:displayName>
        <spirit:envIdentifier>vhdlSource:vivado.xilinx.com:simulation</spirit:envIdentifier>
        <spirit:language>vhdl</spirit:language>
        <spirit:modelName>{0}</spirit:modelName>
        <spirit:fileSetRef>
          <spirit:localName>""" + self.vhdl_sim_fileSetName + """</spirit:localName>
        </spirit:fileSetRef>
      </spirit:view>
      <spirit:view>
        <spirit:name>xilinx_xpgui</spirit:name>
        <spirit:displayName>UI Layout</spirit:displayName>
        <spirit:envIdentifier>:vivado.xilinx.com:xgui.ui</spirit:envIdentifier>
        <spirit:fileSetRef>
          <spirit:localName>""" + self.tcl_fileSetName + """</spirit:localName>
        </spirit:fileSetRef>
      </spirit:view>
    </views>
        """).format(unit._name)
        for v in etree.fromstring(viewsTemplate):
            v = View.fromElem(v)
            v.modelName = unit._name
            self.views.append(v)
        for g in unit._entity.generics:
            mp = ModelParameter.fromGeneric(g)
            self.modelParameters.append(mp)
            
    
    # @classmethod
    # def fromElem(cls, elm):
    #    self = cls()
    #    views = findS(elm, "views")
    #    for vElm in views:
    #        self.views.append(View.fromElem(vElm))
    #    ports = findS(elm, "ports")
    #    for p in ports:
    #        self.ports.append(Port.fromElem(p))
    #    return self
    
    def asElem(self):
        e = mkSpiElm("model")
        appendSpiArray(e, 'views', self.views)
        appendSpiArray(e, 'ports', self.ports)
        appendSpiArray(e, 'modelParameters', self.modelParameters)
            
        return e
