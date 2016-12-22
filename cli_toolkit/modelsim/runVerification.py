from subprocess import PIPE, Popen
import os
from hwt.pyUtils.arrayQuery import where
import subprocess
import re
from copy import copy

DEFAULT_VCOM_PARAMS = ['-2008', "-explicit"]
DEFAULT_VLOG_PARAMS = ["-work {work}", "-sv"]
VSIM = ["vsim"]

MTI_HOME = "/opt/modelsim_se_105/modeltech/"
UVM_HOME = MTI_HOME + "verilog_src/uvm-1.2/"

hasPackageRe = re.compile(".*package\s+\S+\s*;.*", re.MULTILINE | re.DOTALL)

def formatFileNames(fileNames):
    return "\\\n".join(map(lambda x: "{%s}" % x, fileNames))

def formatParams(params):
    return " ".join(params)

def findSVPackageFiles(svFiles):
    for f in svFiles:
        with open(f) as _f:
            if hasPackageRe.match(_f.read()):
                yield f

def buildSv(sv_incdir, svFiles, vlogParams):
    return ("vlog %s +incdir+" + UVM_HOME + "src " + UVM_HOME + "src/uvm.sv %s %s") % (
            formatParams(vlogParams),
            " ".join(map(lambda x:"+incdir+"+ x, sv_incdir)),
            formatFileNames(where(svFiles, lambda x: x.endswith(".sv"))),
           )

def runVerificationCmds(vhdlFiles, svFiles, top, uvmTestNames,
                       vcomParams,
                       vlogParams,
                       vsimParams):
    lib = "work"
    vsimParams = vsimParams + ["-wlf sim.wlf",
                  "-sv_lib " + MTI_HOME + "uvm-1.2/linux_x86_64/uvm_dpi",
                  '-do "run -all;"',
                  "-errorfile errors"
                  ]
    
    if vhdlFiles:
        buildVhdls = "vcom %s -work {%s} %s" % (
                                          formatParams(vcomParams),
                                          lib,
                                          formatFileNames(vhdlFiles)
                                          )
    else:
        buildVhdls = ""
        
    sv_incdir = set(map(lambda f: os.path.dirname(f), svFiles))
    svFiles = list(where(svFiles, lambda x: x.endswith(".sv")))
    buildSvCmd = []
    packageFiles = list(findSVPackageFiles(svFiles))
    packageFiles.sort(key=lambda x: len(x))
    
    
    # build all packages
    for f in packageFiles:
        # we need includes only from this package
        dirName = os.path.dirname(f)
        # we are building only this package
        buildSvCmd.append(buildSv([dirName], [f], vlogParams))
    
    packageFiles = set(packageFiles)
    # build rest of files
    buildSvCmd.append(
        buildSv(sv_incdir,
                list(where(svFiles,
                            lambda x: x not in packageFiles)),
                vlogParams)
        )
    
    for uvmTestName in uvmTestNames:
        _vsimParams = vsimParams + ["+UVM_TESTNAME=%s" % uvmTestName]
        cmd = ("""
onbreak {status; puts "Quit on break"; quit -code 1}
onerror {status; puts "Quit on error"; quit -code 2}
onElabError {status; puts "Quit on elabError"; quit -code 3}

vlib work
%s
%s

add wave -divider DUT
add wave -noupdate -hex /top/dut1/*

vsim  %s -lib %s %s 
quit -code 0
""") % (buildVhdls, "\n".join(buildSvCmd),
        formatParams(_vsimParams), lib, top)
        yield cmd


def runSVVer(vhdlFiles, systemVerilogSources, top, uvmTestNames=[""],
              vcomParams=DEFAULT_VCOM_PARAMS,
              vlogParams=DEFAULT_VLOG_PARAMS,
              vsimParams = ["+UVM_NO_RELNOTES"],
              gui=False):
    verCmds = list(runVerificationCmds(vhdlFiles, systemVerilogSources, 
                                  top, uvmTestNames,
                                  vcomParams, vlogParams, vsimParams))
    cmdFileName = "modelsimCmd.tcl"
    with open(cmdFileName, 'w') as f:
        f.write("\n---------------\n".join(verCmds))

    
    for cmd in verCmds:
        _VSIM = VSIM + ["-c"]
        p = Popen(_VSIM, shell=True, stdin=PIPE)
        p.communicate(cmd.encode(encoding='utf_8'))

    if gui:
        p = subprocess.call(VSIM + ["-gui"])
    

    
    
