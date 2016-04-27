import sys
import os
import inspect
import subprocess
import hashlib

from python_toolkit.fileHelpers import find_files
from hdl_toolkit.intfLvl import UnitFromHdl

class VivadoHlsConfig():
    EXECUTABLE = ["bash", "/opt/Xilinx/Vivado_HLS/2015.2/vivado_hls.sh"]


def hashFile(file, hasher):
    BLOCKSIZE = 65536
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

def getHashInfoDirs(directory, exceptFiles=[]):
    hasher = hashlib.md5()
    if not os.path.exists (directory):
        return -1
    
    for root, dirs, files in os.walk(directory):
        for names in files:
            filepath = os.path.join(root, names)
            if filepath in exceptFiles:
                continue
            try:
                f1 = open(filepath, 'rb')
            except:
                # You can't open the file for some reason
                f1.close()
                continue
    
            while 1:
                # Read file in as little chunks
                buf = f1.read(4096)
                if not buf: 
                    break
                hasher.update(hashlib.md5(buf).digest())
            f1.close()
            
    
    return hasher.digest()

class VivadoHLSUnit(UnitFromHdl):
    """
    @cvar _project: path to vivado hls project
    @cvar _top    : name of top
    """
    __hashFileName = "__hash__.txt"
    
    @classmethod
    def _runSynthesisInVivadoHls(cls):
        hashFileN = os.path.join(cls._project, cls.__hashFileName)
        try:
            with open(hashFileN) as hf:
                oldHash = int(hf.readline())
        except:
            oldHash = 0
        
        def getActualHash():
            return int.from_bytes((getHashInfoDirs(cls._project, exceptFiles=[hashFileN])), byteorder='little')
            
        actualHash = getActualHash()
        if oldHash != actualHash: 
            #print("synt", oldHash, actualHash)
            originalCWD = os.getcwd()
            os.chdir(os.path.join(cls._project, ".."))
            
            synTcl = os.path.join(cls._project, "solution1/script.tcl")
            cmd = []
            cmd.extend(VivadoHlsConfig.EXECUTABLE)
            cmd.append(synTcl)
            sp = subprocess.Popen(cmd, shell=False,
                                 stdout=subprocess.DEVNULL, stderr=sys.stderr)
            sp.wait()
            os.chdir(originalCWD)
            actualHash = getActualHash()
            with open(hashFileN, "w") as hf:
                hf.write("%d" % actualHash)
       
        cls._collectSources()
        
    @classmethod
    def _collectSources(cls):
        cls._hdlSources = sorted(find_files(os.path.join(cls._project, "solution1/syn/vhdl/"), '*.vhd'),
                                  key=lambda f : f.endswith(cls._top + ".vhd"))
        
        
    @classmethod
    def _build(cls):
        # convert source filenames to absolute paths
        assert(cls._project)
        assert(cls._top)
        baseDir = os.path.dirname(inspect.getfile(cls))
        cls._project = os.path.join(baseDir, cls._project) 
        
        cls._runSynthesisInVivadoHls()
        
        super(VivadoHLSUnit, cls)._build()
