import os
import sys
import json
from subprocess import Popen, PIPE

from python_toolkit.arrayQuery import where

from vhdl_toolkit.parser import Parser, ParserException
from vhdl_toolkit.hdlContext import BaseVhdlContext, HDLCtx, BaseVerilogContext

baseDir = os.path.dirname(__file__)
JAVA = 'java'
CONVERTOR = os.path.join(baseDir, "vhdlConvertor", "hdlConvertor.jar")

class ParserFileInfo():
    def __init__(self, fileName, lib):
        assert(isinstance(fileName, str))
        self.fileName = fileName
        self.lang = langFromExtension(fileName)
        self.caseSensitive = isCaseSecsitiveLang(self.lang)
        if not self.caseSensitive:
            lib = lib.lower()
        self.lib = lib
        self.hierarchyOnly = False
        self.primaryUnitsOnly = False
        self.functionsOnly = False
        
    def getCacheKey(self):
        return (self.fileName, self.hierarchyOnly)

def getFileInfoFromObj(obj):
    while True:
        if isinstance(obj, HDLCtx):
            fi = obj.fileInfo
            if fi is not None:
                return fi 
        obj = obj.parent

def langFromExtension(fileName):
    n = fileName.lower()
    if n.endswith('.v'):
        return Parser.VERILOG
    elif n.endswith(".vhd"):
        return Parser.VHDL
    else:
        raise NotImplementedError("Can not resolve type of file")
def isCaseSecsitiveLang(lang):
    if  lang == Parser.VHDL:
        return False
    elif lang == Parser.VERILOG:
        return True
    else:
        raise ParserException("Invalid lang specification \"%s\" is not supported" % (str(lang)))
        
def getJson(byteData, fileInfo):
    if byteData == b'':
        j = None
    else:
        j = json.loads(byteData.decode("utf-8"))
    k = fileInfo.getCacheKey()
    Parser._cache[k] = j
    return j

def collectJsonFromProc(p, timeoutInterval, hierarchyOnly, ignoreErrors):
    stdoutdata, stdErrData = p.communicate(timeout=timeoutInterval)
    fileName = p.fileInfo.fileName
    
    # get json
    if p.returncode != 0:
        raise ParserException("Failed to parse file %s" % (fileName))
    if not ignoreErrors and (stdErrData != b'' and stdErrData is not None):
        sys.stderr.write(stdErrData.decode()) 
    try:
        return getJson(stdoutdata, p.fileInfo)
    except ValueError:
        raise ParserException(("Failed to parse file %s, ValueError while parsing" + 
                        " json from convertor\n%s") % (fileName, stdErrData.decode()))
                        


class ParserLoader():
    @staticmethod
    def spotLoadingProc(fInfo, debug=False):
        cmd = [JAVA, "-jar", str(CONVERTOR), fInfo.fileName]
        if fInfo.hierarchyOnly:
            cmd.append('-h')
        if debug:
            cmd.append("-d")
        cmd.extend(('-langue', fInfo.lang))
    
        p = Popen(cmd, stdout=PIPE)
        p.fileInfo = fInfo
        return p
    
    @staticmethod
    def parseFiles(fileList, timeoutInterval=20, ignoreErrors=False, debug=False):
        """
        @param fileList: list of files to parse in same context
        @param lang: hdl language name (currently supported are vhdl and verilog)
        @param hdlCtx: parent HDL context
        @param libName: name of actual library
        @param timeoutInterval: timeout for process of external vhdl parser
        @param hierarchyOnly: discover only presence of entities, architectures
               and component instances inside, packages and components inside, packages
        @param primaryUnitsOnly: parse only entities and package headers
        """
        
        lang = fileList[0].lang
        for f in fileList:
            assert(f.lang == lang)
        
        if lang == Parser.VHDL:
            topCtx = BaseVhdlContext.getBaseCtx()
            BaseVhdlContext.importFakeLibs(topCtx)
        else:
            topCtx = BaseVerilogContext.getBaseCtx()
            BaseVerilogContext.importFakeLibs(topCtx)
            
        # start parsing all files    
        p_list = []
        for fInfo in fileList:
            k = fInfo.getCacheKey()
            if k in Parser._cache:
                p = fInfo
            else:
                p = ParserLoader.spotLoadingProc(fInfo, debug=debug)
            p_list.append(p)

        fileCtxs = []
        # collect parsed json from java parser and construct python objects
        for p in p_list:
            if isinstance(p, ParserFileInfo):  # result is in cache
                j = Parser._cache[p.getCacheKey()]
                fileInfo = p
            else:  # parser process was spooted
                fileInfo = p.fileInfo
                j = collectJsonFromProc(p, timeoutInterval, fileInfo.hierarchyOnly, ignoreErrors)
            if j:
                lib = fileInfo.lib
                fName = fileInfo.fileName
                parser = Parser(fileInfo.caseSensitive, fileInfo.hierarchyOnly, fileInfo.primaryUnitsOnly, fileInfo.functionsOnly)
                if lib is None:
                    ctx = topCtx
                else:
                    try:
                        ctx = topCtx[lib]
                    except KeyError:
                        ctx = HDLCtx(lib, topCtx)
                        topCtx[lib] = ctx

                fileCtx = HDLCtx(fName, ctx)
                fileCtx.fileInfo = fileInfo
                fileCtxs.append(fileCtx)
                parser.parse(j, fName, fileCtx)
                
                # copy references to primary units
                for _, e in fileCtx.entities.items():
                    ctx.insertObj(e, fileInfo.caseSensitive, fileInfo.hierarchyOnly)
                for _, p in fileCtx.packages.items():
                    ctx.insertObj(p, fileInfo.caseSensitive, fileInfo.hierarchyOnly)
                    
                    
                    
                     
                # [TODO] update parent context
    
        return topCtx, fileCtxs
