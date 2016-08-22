from subprocess import PIPE, Popen
import os

DEFAULT_VCOM_PARAMS = ["2008", "explicit", "just p"]
DEFAULT_VLOG_PARAMS = ["sv"]
VSIM = "vsim -batch"

def runVerificationCmd(vhdlFiles, svFiles,
                       vcomParams=DEFAULT_VCOM_PARAMS,
                       vlogParams=DEFAULT_VLOG_PARAMS):
    lib = "work"
    verName = "tbench"
    
    def formatFileNames(fileNames):
        return "\\\n".join(map(lambda x: "{%s}" % x, fileNames))
    
    def formatParams(params):
        return " ".join(map(lambda x: "-" + x , params))
    
    buildVhdls = "vcom %s -work {%s} %s" % (
                                          formatParams(vcomParams),
                                          lib,
                                          formatFileNames(vhdlFiles)
                                          )
    
    sv_incdir = set(map(lambda f: "+incdir+" + os.path.basename(f), svFiles))
    
    
    buildSv = "vlog %s -work {%s} %s %s" % (
                                         formatParams(vlogParams),
                                         lib,
                                         formatFileNames(svFiles),
                                         " ".join(sv_incdir)
                                         )
    
    cmd = """
# auto-generated file
# setup error handlers
onbreak {status; puts "Quit on break"; quit -code 1}
onerror {status; puts "Quit on error"; quit -code 2}
onElabError {status; puts "Quit on elabError"; quit -code 3}

# create new clean work lib
vlib work
vdel -lib work -all
vlib work

# compile vhdl files
%s

# compile system verilog files
%s

vsim -wlf wlf -errorfile errors -onfinish final   -lib %s %s
view wave
delete wave *
restart -f
run 5us
quit -code 0
""" % (buildVhdls, buildSv, lib, verName)
    
    return cmd


def runModelsim(cmds, gui=False):
    raise NotImplementedError()
    
def runSVVer(vhdlFiles, systemVerilogSources,
              vcomParams=DEFAULT_VCOM_PARAMS,
              vlogParams=DEFAULT_VLOG_PARAMS):
    
    verCmd = runVerificationCmd(vhdlFiles, systemVerilogSources,
                                vcomParams, vlogParams)
    p = Popen(VSIM, shell=True, stdin=PIPE)
    print(p.communicate(verCmd.encode(encoding='utf_8')))
    

    
    
