import os
from time import gmtime, strftime

from vivado_toolkit.ip_packager.helpers import spi_ns_prefix, mkSpiElm, \
    appendSpiElem, appendStrElements, mkXiElm, appendXiElem, appendSpiAtribs
from vhdl_toolkit.synthetisator.param import getParam
import math
from vhdl_toolkit.expr import Unconstrained, BinOp


class Value():
    __slots__ = ['id', 'format', 'bitStringLength', 'resolve', 'text']
    RESOLVE_GENERATED = "generated"
    RESOLVE_USER = "user"

    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.id = elm.attrib[spi_ns_prefix + 'id']
        self.text = elm.text
        self.resolve = elm.attrib[spi_ns_prefix + 'resolve']
        for n in ['format', 'bitStringLength']:
            try:
                value = elm.attrib[spi_ns_prefix + n]
                setattr(self, n, value)
            except KeyError:
                pass
        return self
    @classmethod
    def fromGeneric(cls, idPrefix, g, resolve):
        self = cls()
        self.id = idPrefix + g.name
        self.resolve = resolve
        w = g.var_type.width
        def getVal():
            if g.defaultVal:
                return getParam(g.defaultVal)
            else:
                return 0  
        def bitString(w):
            self.format = "bitString"
            digits = math.ceil(w / 4)
            self.text = ('0x%0' + str(digits) + 'X') % getVal() 
            self.bitStringLength = str(w)
            
        if w == 1:
            raise NotImplementedError()
        elif w == bool:
            self.format = "bool"
            self.text = str(bool(getVal())).lower() 
        elif w == int:
            self.format = "long"
            self.text = str(getVal())
        elif w == str:
            self.format = "string"
            self.text = str(g.defaultVal.val.val)
        elif isinstance(w, int):
            bitString(w)
        elif w == Unconstrained:
            bitString(w.derivedWidth)
        elif isinstance(w, BinOp):
            w = w.evalFn()
            bitString(w)
        else:
            raise NotImplementedError()
        return self
        
    def asElem(self):
        e = mkSpiElm("value")
        appendSpiAtribs(self, e, spi_ns_prefix, reqPropNames=['id', 'resolve'],
                        optPropNames=['format', 'bitStringLength'])
        
        e.text = str(self.text)
        return e

class FileSet():
    def __init__(self):
        self.name = ""
        self.files = []
    def asElem(self):
        e = mkSpiElm("fileSet")
        appendSpiElem(e, "name").text = self.name
        for f in self.files:
            e.append(f.asElem())
        return e
                    
class File():
    _strValues = ["name", "fileType", "userFileType"]    
    def __init__(self):
        self.name = ""
        self.fileType = ""
        self.userFileType = ""
        
    @classmethod
    def fromFileName(cls, fileName):
        self = cls()
        extDict = {
                   ".vhd": ("vhdlSource", "IMPORTED_FILE"),
                   ".tcl": ("tclSource", "XGUI_VERSION_2")
                   }
        fileType = extDict[os.path.splitext(fileName.lower())[1]]
        self.fileType = fileType[0] 
        self.userFileType = fileType[1]
        self.name = fileName
        return self
                
    def asElem(self):
        e = mkSpiElm("file")
        appendStrElements(e, self, self._strValues)
        return e
    
class Parameter():
    __slots__ = ["name", 'displayName', "value", 'order']
    def __init__(self):
        self.name = ""
        self.value = Value()

    # @classmethod
    # def fromElem(cls, elm):
    #    self = cls()
    #    self.name = elm.find('spirit:name', ns).text
    #    v = elm.find('spirit:value', ns)
    #    self.value = Value.fromElem(v)
    #    return self
        
    def asElem(self):
        e = mkSpiElm("parameter")
        appendSpiElem(e, "name").text = self.name
        e.append(self.value.asElem())
        return e
    

class CoreExtensions():
    def __init__(self):
        self.supportedFamilies = {
                                  "zynq" : "Production"
                                  }
        self.taxonomies = [
                           "/BaseIP"
                           ]
        self.displayName = ""
        self.coreRevision = ""
        self.coreCreationDateTime = gmtime() 
              
    def asElem(self, displayName, revision):
        r = mkXiElm("coreExtensions")
        sf = appendXiElem(r, "supportedFamilies")
        for family, lifeCycle in self.supportedFamilies.items():
            f = appendXiElem(sf, "family")
            f.text = family
            f.attrib["xilinx:lifeCycle"] = lifeCycle
            
        ta = appendXiElem(r, "taxonomies")
        for t in self.taxonomies:
            appendXiElem(ta, "taxonomy").text = t
            
        appendXiElem(r, "displayName").text = displayName
        appendXiElem(r, "coreRevision").text = revision
        appendXiElem(r, "coreCreationDateTime").text = strftime("%Y-%m-%dT%H:%M:%SZ", self.coreCreationDateTime)
        return r
    
class VendorExtensions():
    def __init__(self):
        self.coreExtensions = CoreExtensions()
        self.packagingInfo = {"xilinxVersion": "2014.4.1"}
    def asElem(self, displayName, revision):
        r = mkSpiElm("vendorExtensions")
        r.append(self.coreExtensions.asElem(displayName, revision))
        pi = appendXiElem(r, "packagingInfo")
        for key, val in self.packagingInfo.items():
            appendXiElem(pi, key).text = val
        
        return r
