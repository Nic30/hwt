import re, os
import zipfile
import xml.etree.ElementTree as ET
import tempfile

GUI_INIT_FN_REGEX = "proc\s+init_gui\s+{\s+IPINST\s+}\s+{([^{]*|(([^}{]*{[^}{]*}[^}{]*)*))}"
fileNameWithoutExtension = lambda filename : os.path.splitext(os.path.basename(filename))[0]
ns = {'spirit': "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009"}

def updateZip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)


class Component(object):
    """
    deprecated
    """
    def __init__(self, name, version, paramNames):
        self.name = name
        self.version = version
        self.paramNames = paramNames
    @staticmethod
    def fromXMLstr(xmlStr):
        root = ET.fromstring(xmlStr)
        name = root.find("spirit:name" , ns).text
        version = root.find("spirit:version" , ns).text
        paramNames = root.findall("spirit:parameters/spirit:parameter/spirit:name" , ns)
        paramNames = list(map(lambda x: x.text, paramNames))
        return Component(name, version, paramNames)
        
class IPCore(object):
    def __init__(self, filename):
        self.filename = filename
        self.ipCoreArchive = zipfile.ZipFile(filename, 'r')
        with self.ipCoreArchive.open("component.xml") as f:
            self.component = Component.fromXMLstr(f.read())
        self.guiConfFilename = "xgui/%s.tcl" % (self.component.name + "_v" + self.component.version.replace(".", "_"))

    def gui_init_fnBodySub(self, newBody):
        r = re.compile(GUI_INIT_FN_REGEX, re.MULTILINE)
        with self.ipCoreArchive.open(self.guiConfFilename) as f:
            result = r.sub("proc init_gui { IPINST } {%s}" % (newBody+"\n"), f.read().decode())
        updateZip(self.filename,self.guiConfFilename,  result)
    def makeParamsEditable(self):
        page = {"id":"main_page", "label":"main"}
        g = "M_axi"
        form = ['ipgui::add_param $IPINST -name "Component_Name"', 'set %s [ipgui::add_page $IPINST -name "%s"]' % (page["id"], page["label"])]        
        s = 'set %s [ipgui::add_group $IPINST -name "%s" -parent ${%s} -display_name {%s}]' % (g, g, page["id"], g)
        form.append(s)
        for p in ip.component.paramNames:
            if p.startswith("C_M_AXI_"):
                s = 'ipgui::add_param $IPINST -name "%s" -parent ${%s}' % (p, g)
                form.append(s)   
        self.gui_init_fnBodySub("\n".join(form))   
            
if __name__ == "__main__":
    ip = IPCore("/home/nic30/Documents/vivado_hls/axi4_trans_tester/solution1/impl/ip/xilinx_com_hls_axi4_trans_tester_1_0.zip")
    # Adding Group
    
    ip.makeParamsEditable()
