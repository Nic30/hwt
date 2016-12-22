import xml.dom.minidom

from hwt.pyUtils.arrayQuery import where
import xml.etree.ElementTree as etree


ns = { "spirit" : "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009",
       "xilinx" :"http://www.xilinx.com",
       "xsi":"http://www.w3.org/2001/XMLSchema-instance"}
spi_ns_prefix = "{" + ns["spirit"] + "}"
xi_ns_prefix = "{" + ns["xilinx"] + "}"



def findS(elm, name):
    return elm.find("spirit:" + name, ns)

def prettify(elm):
    s = xml.dom.minidom.parseString(etree.tostring(elm))  # or xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = s.toprettyxml()
    return pretty_xml_as_string

def mkSpiElm(elemName):
    e = etree.Element(spi_ns_prefix + elemName)
    return e

def mkXiElm(elemName):
    e = etree.Element(xi_ns_prefix + elemName)
    return e

def appendSpiElem(root, elemName):
    e = mkSpiElm(elemName)
    root.append(e)
    return e

def appendXiElem(root, elemName):
    e = mkXiElm(elemName)
    root.append(e)
    return e

def appendStrElements(root, obj, reqPropNames=[], optPropNames=[]):
    for p in reqPropNames:
        e = appendSpiElem(root, p)
        e.text = getattr(obj, p)
    for p in optPropNames:
        if hasattr(obj, p):
            e = appendSpiElem(root, p)
            e.text = getattr(obj, p)

whereEndsWithExt = lambda files, extension :\
             where(files, lambda x : x.lower().endswith(extension))
             
def whereEndsWithExts(files, extensions):
    for f in files:
        for extension in extensions:
            if f.lower().endswith(extension.lower()):
                yield f
             
             
def appendSpiAtribs(obj, elm, prefix='', reqPropNames=[], optPropNames=[]):
    for p in reqPropNames:
        elm.attrib[prefix + p] = getattr(obj, p) 
    for p in optPropNames:
        if hasattr(obj, p):
            elm.attrib[prefix + p] = getattr(obj, p) 

def appendSpiArray(root, arrName, arr):
    if arr:
        elmArr = appendSpiElem(root, arrName)
        for o in arr:
            elmArr.append(o.asElem())