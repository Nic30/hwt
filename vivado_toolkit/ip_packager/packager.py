import os, shutil
from vhdl_toolkit.parser import entityFromFile
from python_toolkit.fileHelpers import find_files
from vivado_toolkit.ip_packager.helpers import prettify
from vivado_toolkit.ip_packager.component import Component

def makeDummyXGUIFile(fileName):
    s = """
    # Definitional proc to organize widgets for parameters.
proc init_gui { IPINST } {
  #Adding Page
  ipgui::add_page $IPINST -name "Page 0"

}"""
    with open(fileName, "w") as f:
        f.write(s)


def packageMultipleProjects(workspace, names):
    for folder, name in names.items():
        packageVivadoHLSProj(os.path.join(workspace, folder), "solution1", name + ".vhd")
        print(folder + " packaged")

def packageVivadoHLSProj(projPath, solutionName, mainVhdlFileName, relIpPath="impl/ip"):
    # rm others ip in project
    ip_dir = os.path.join(projPath, solutionName, "impl/ip/")
    vhdlPath = os.path.join(projPath, solutionName, "syn/vhdl")
    tclPath = os.path.join(ip_dir, "xgui")
    ip_srcPath = os.path.join(ip_dir, "src")
    guiFile = os.path.join(tclPath, "gui.tcl")
    
    if os.path.exists(ip_dir):
        shutil.rmtree(ip_dir)
    for d in [ip_dir , ip_srcPath, tclPath]:
        os.makedirs(d)
    vhdlfiles = list(find_files(vhdlPath, "*.vhd"))
    for f in vhdlfiles:
        shutil.copy2(f, ip_srcPath + "/")
    
    makeDummyXGUIFile(guiFile)
    e = entityFromFile(os.path.join(ip_srcPath, mainVhdlFileName))
    
    c = Component()
    c._files = vhdlfiles + [guiFile ]
    c.vendor = "nic"
    c.library = "mylib"
    c.description = e.name + "_v" + c.version
    c.asignTopEntity(e)
    xml_str = prettify(c.xml()) 
    with open(ip_dir + "component.xml", "w") as f:
        f.write(xml_str)
    # print(xml_str)

def demo():
    c_folder = "/home/nic30/Documents/vivado/ip_repo/component_test/"
    e = entityFromFile(c_folder + "src/component1.vhd")
    c = Component()
    c.vendor = "nic"
    c.library = "mylib"
    c.description = e.name + "_v" + c.version
    c._files = ["src/component1.vhd", "xgui/component1_v1_0.tcl" ]
    c.asignTopEntity(e)
    xml_str = prettify(c.xml()) 
    with open(c_folder + "component.xml", "w") as f:
        f.write(xml_str)
    print(xml_str)

if __name__ == "__main__":
    demo()
    packageMultipleProjects("/home/nic30/Documents/vivado_hls/", {"axi_custom_master": "axi_custom_master",
                                                                  "axi_trans_tester2": "axi_trans_tester"})
