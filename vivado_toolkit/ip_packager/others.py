import os
from time import gmtime, strftime

from vivado_toolkit.ip_packager.helpers import spi_ns_prefix, mkSpiElm, \
    appendSpiElem, appendStrElements, ns, mkXiElm, appendXiElem


class Value():
    __slots__ = ['id', 'resolve', 'text']

    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.text = elm.text
        self.id = elm.attrib[spi_ns_prefix + 'id']
        self.resolve = elm.attrib[spi_ns_prefix + 'resolve']
        return self
        
    def asElem(self):
        e = mkSpiElm("value")
        e.attrib[spi_ns_prefix + 'id'] = self.id
        e.attrib[spi_ns_prefix + 'resolve'] = self.resolve
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
    __slots__ = ["name", "value"]
    def __init__(self):
        self.name = ""
        self.value = Value()

    @classmethod
    def fromElem(cls, elm):
        self = cls()
        self.name = elm.find('spirit:name', ns).text
        v = elm.find('spirit:value', ns)
        self.value = Value.fromElem(v)
        return self
        
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
