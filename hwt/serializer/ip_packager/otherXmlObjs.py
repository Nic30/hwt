import os, math
from time import gmtime, strftime

from hwt.serializer.ip_packager.helpers import spi_ns_prefix, mkSpiElm, \
    appendSpiElem, appendStrElements, mkXiElm, appendXiElem, appendSpiAtribs
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, STR
from hwt.hdlObjects.types.integer import Integer
from hwt.synthesizer.param import evalParam


class Value():
    __slots__ = ['id', 'format', 'bitStringLength', 'resolve', 'dependency', 'text']
    RESOLVE_GENERATED = "generated"
    RESOLVE_USER = "user"

    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.id = elm.attrib[spi_ns_prefix + 'id']
        self.text = elm.text
        self.resolve = elm.attrib[spi_ns_prefix + 'resolve']
        self.dependency = elm.attrib[spi_ns_prefix + 'dependency']
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
        t = g._dtype
        def getVal():
            v = evalParam(g.defaultVal) 
            if v.vldMask:
                return v.val
            else:
                return 0  
        def bitString(w):
            self.format = "bitString"
            digits = math.ceil(w / 4)
            self.text = ('0x%0' + str(digits) + 'X') % getVal() 
            self.bitStringLength = str(w)
            
        if t == BOOL:
            self.format = "bool"
            self.text = str(bool(getVal())).lower() 
        elif isinstance(t, Integer) :
            self.format = "long"
            self.text = str(getVal())
        elif t == STR:
            self.format = "string"
            self.text = g.defaultVal.staticEval().val
        elif isinstance(t, Bits):
            bitString(g.defaultVal._dtype.bit_length())
        else:
            raise NotImplementedError("Not implemented for datatype %s" % repr(t))
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
                   ".tcl": ("tclSource", "XGUI_VERSION_2"),
                   ".v"  : ("verilogSource", "IMPORTED_FILE")
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
                                  "zynq" : "Production",
                                  "atrix7" : "Production",
                                  "kintex7" : "Production",
                                  "virtex7" : "Production"
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

#  [TODO] XILINX_VERSION has to be extracted into some configuration
class VendorExtensions():
    XILINX_VERSION = "2014.4.1"
    def __init__(self):
        self.coreExtensions = CoreExtensions()
        self.packagingInfo = {"xilinxVersion": self.XILINX_VERSION}
    def asElem(self, displayName, revision):
        r = mkSpiElm("vendorExtensions")
        r.append(self.coreExtensions.asElem(displayName, revision))
        pi = appendXiElem(r, "packagingInfo")
        for key, val in self.packagingInfo.items():
            appendXiElem(pi, key).text = val
        
        return r
