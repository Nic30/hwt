from subprocess import PIPE, Popen
import os
from python_toolkit.arrayQuery import where
import subprocess
import re

DEFAULT_VCOM_PARAMS = ['2008', "explicit"]
DEFAULT_VLOG_PARAMS = ["work {work}", "sv"]
VSIM = ["vsim"]

MTI_HOME = "/opt/modelsim_se_105/modeltech/"
UVM_HOME = MTI_HOME + "verilog_src/uvm-1.2/"

hasPackageRe = re.compile(".*package\s+\S+\s*;.*", re.MULTILINE | re.DOTALL)

def formatFileNames(fileNames):
    return "\\\n".join(map(lambda x: "{%s}" % x, fileNames))

def formatParams(params):
    return " ".join(map(lambda x: "-" + x , params))

def findSVPackageFiles(svFiles):
    for f in svFiles:
        with open(f) as _f:
            if hasPackageRe.match(_f.read()):
                yield f

def buildSv(sv_incdir, svFiles, vlogParams):
    return ("vlog %s +incdir+" + UVM_HOME + "src " + UVM_HOME + "src/uvm.sv %s %s") % (
            formatParams(vlogParams),
            " ".join(sv_incdir),
            formatFileNames(where(svFiles, lambda x: x.endswith(".sv"))),
           )

def runVerificationCmd(vhdlFiles, svFiles, top,
                       vcomParams=DEFAULT_VCOM_PARAMS,
                       vlogParams=DEFAULT_VLOG_PARAMS):
    lib = "work"

    if vhdlFiles:
        buildVhdls = "vcom %s -work {%s} %s" % (
                                          formatParams(vcomParams),
                                          lib,
                                          formatFileNames(vhdlFiles)
                                          )
    else:
        buildVhdls = ""
        
    sv_incdir = set(map(lambda f: "+incdir+" + os.path.dirname(f), svFiles))
    svFiles = list(where(svFiles, lambda x: x.endswith(".sv")))
    buildSvCmd = []
    packageFiles = list(findSVPackageFiles(svFiles))
    packageFiles.sort(key=lambda x: len(x))
    
    
    # build all packages
    for f in packageFiles:
        # we need includes only from this package
        dirName = os.path.dirname(f)
        _sv_incdir = list(where(sv_incdir, lambda x: x.startswith(dirName)))
        # we are building only this package
        buildSvCmd.append(buildSv(_sv_incdir, [f], vlogParams))
    
    packageFiles = set(packageFiles)
    # build rest of files
    buildSvCmd.append(
        buildSv(sv_incdir,
                list(where(svFiles,
                            lambda x: x not in packageFiles)),
                vlogParams)
        )
    
    
    cmd = ("""
onbreak {status; puts "Quit on break"; quit -code 1}
onerror {status; puts "Quit on error"; quit -code 2}
onElabError {status; puts "Quit on elabError"; quit -code 3}

vlib work
%s
%s

add wave -divider DUT
add wave -noupdate -hex /top/dut1/*

vsim -wlf sim.wlf -sv_lib """ + MTI_HOME + """uvm-1.2/linux_x86_64/uvm_dpi -lib %s %s -do "run -all; quit -f" -errorfile errors

view wave
delete wave *
restart -f
run 5us
quit -code 0
""") % (buildVhdls, "\n".join(buildSvCmd), lib, top)
    
    return cmd


def runSVVer(vhdlFiles, systemVerilogSources, top,
              vcomParams=DEFAULT_VCOM_PARAMS,
              vlogParams=DEFAULT_VLOG_PARAMS, gui=False):
    
    verCmd = runVerificationCmd(vhdlFiles, systemVerilogSources, top,
                                vcomParams, vlogParams)
    cmdFileName = "modelsimCmd.tcl"
    with open(cmdFileName, 'w') as f:
        f.write(verCmd)

    
    _VSIM = VSIM + ["-c"]
    p = Popen(_VSIM, shell=True, stdin=PIPE)
    p.communicate(verCmd.encode(encoding='utf_8'))

    if gui:
        p = subprocess.call(VSIM + ["-gui"])
    

    
    
