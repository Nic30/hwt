import re

from python_toolkit.arrayQuery import where
from vhdl_toolkit.valueInterpret import ValueInterpreter
from vivado_toolkit.ip_packager.helpers import appendSpiElem, appendStrElements, \
         findS, mkSpiElm, ns, spi_ns_prefix
import xml.etree.ElementTree as etree


class WireTypeDef():
    _requiredVal = ["typeName"]
    
    @classmethod
    def fromElem(cls, elm):
        self = cls()
        for s in cls._requiredVal:
            setattr(self, s, findS(elm, s).text)
        self.viewNameRefs = []
        for r in elm.findall("spirit:viewNameRef", ns):
            self.viewNameRefs.append(r.text)
        return self
    
    def asElem(self):
        e = mkSpiElm("wireTypeDef")
        for s in self._requiredVal:
            appendSpiElem(e, s).text = getattr(self, s)
        for r in self.viewNameRefs:
            appendSpiElem(e, "viewNameRef").text = r
        return e
    
class Port():
    
    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.name = findS(elm, "name").text
        vec = findS(elm, "vector")
        if vec is not None:
            self.vector = [findS(vec, "left").text, findS(vec, "right").text]
        else:
            self.vector = None
             
        wire = findS(elm, "wire")
        self.direction = findS(wire, "direction").text
        self.type = WireTypeDef.fromElem(findS(findS(wire, "wireTypeDefs"), "wiretypedef"))
        return self
    
    @staticmethod
    def _entPort2CompPort(e, p):
        port = Port()
        port.name = p.name
        port.direction = p.direction.lower()
        port.type = WireTypeDef()
        t = port.type
        t_str = p.var_type.str.upper()
        if "VECTOR" in t_str:
            t.typeName = "STD_LOGIC_VECTOR"
            m = re.match("STD_LOGIC_VECTOR\s*\((.*)\s+(to|downto)\s+(.*)\s*\)", p.var_type.str, re.IGNORECASE)
            direction = m.group(2).lower()
            l = ValueInterpreter.resolveInt(e, m.group(1))
            r = ValueInterpreter.resolveInt(e, m.group(3))
            if direction == "downto":
                port.vector = (l, r)
            elif direction == "to":
                port.vector = (r, l)
            else:
                raise Exception()
            
        else:
            t.typeName = "STD_LOGIC"
            port.vector = False
            
        t.viewNameRefs = ["xilinx_vhdlsynthesis", "xilinx_vhdlbehavioralsimulation"]
        return port
    
    def asElem(self):
        e = mkSpiElm("port")
        appendSpiElem(e, "name").text = self.name
        w = appendSpiElem(e, "wire")
        appendSpiElem(w, "direction").text = self.direction
        if self.vector:
            v = appendSpiElem(w, "vector")
            l = appendSpiElem(v, "left")
            l.text = str(self.vector[0])
            r = appendSpiElem(v, "right")
            r.text = str(self.vector[1])
            for d in [l, r]:
                d.attrib["spirit:format"] = "long"
                d.attrib["spirit:resolve"] = "immediate"
        td = appendSpiElem(w, "wireTypeDefs")
        td.append(self.type.asElem())
        return e
        


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

class Model():
    
    def __init__(self, vhdl_syn_fileSetName, vhdl_sim_fileSetName, tcl_fileSetName):
        self.views = []
        self.ports = []
        self.vhdl_syn_fileSetName = vhdl_syn_fileSetName
        self.vhdl_sim_fileSetName = vhdl_sim_fileSetName
        self.tcl_fileSetName = tcl_fileSetName
        
    def addDefaultViews(self, compName):
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
        """).format(compName)
        views = []
        for v in etree.fromstring(viewsTemplate):
            views.append(View.fromElem(v))
        for v in views:
            v.modelName = compName
            self.views.append(v)
    
    @classmethod
    def fromElem(cls, elm):
        self = cls()
        views = findS(elm, "views")
        for vElm in views:
            self.views.append(View.fromElem(vElm))
        ports = findS(elm, "ports")
        for p in ports:
            self.ports.append(Port.fromElem(p))
        return self
    
    def asElem(self):
        e = mkSpiElm("model")
        views = appendSpiElem(e, "views")
        for v in self.views:
            views.append(v.asElem())
        ports = appendSpiElem(e, "ports")
        for p in self.ports:
            ports.append(p.asElem())
        return e
