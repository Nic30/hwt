import re
from vivado_toolkit.ip_packager.helpers import appendSpiElem, \
         findS, mkSpiElm, ns
from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.hdlObjects.operators import Op

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
        w = getParam(p.var_type.width)
        
        if w == 1:
            t.typeName = "STD_LOGIC"
            port.vector = False
        else:
            t.typeName = "STD_LOGIC_VECTOR"
            if isinstance(w, int):
                port.vector = (w - 1, 0)
            elif isinstance(w, Op):
                port.vector = (w.op0, w.op1)
            else:
                raise NotImplementedError()
        t.viewNameRefs = ["xilinx_vhdlsynthesis", "xilinx_vhdlbehavioralsimulation"]
        return port
    
    def asElem(self):
        e = mkSpiElm("port")
        appendSpiElem(e, "name").text = self.name
        w = appendSpiElem(e, "wire")
        appendSpiElem(w, "direction").text = self.direction
        if self.vector:
            v = appendSpiElem(w, "vector")
            def mkBoundry(name, val):
                d = appendSpiElem(v, name)
                
                d.attrib["spirit:format"] = "long"
                if isinstance(val, Op):  # value is symple type and does not contains generic etc...
                    resolve = 'dependent'  # [HOTFIX] needs to be a custom str method for expr
                    depStr = re.sub("(\A\S*)", "spirit:decode(id('MODELPARAM_VALUE.\g<1>'))", str(val))
                    d.attrib["spirit:dependency"] = "(" + depStr + ")"
                    d.text = str(val.evalFn())
                else:
                    resolve = "immediate"
                    d.text = str(getParam(val))
                d.attrib["spirit:resolve"] = resolve
                    
            mkBoundry("left", self.vector[0])
            mkBoundry("right", self.vector[1])
        td = appendSpiElem(w, "wireTypeDefs")
        td.append(self.type.asElem())
        return e
