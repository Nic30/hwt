import hdlConvertor

from hdl_toolkit.parser.baseParser import BaseParser, ParserException
from hdl_toolkit.parser.vhdlParser import VhdlParser
from hdl_toolkit.parser.verilogParser import VerilogParser
from hdl_toolkit.parser.hdlContext import BaseVhdlContext, HDLCtx, BaseVerilogContext


class ParserFileInfo():
    def __init__(self, fileName, lib):
        assert isinstance(fileName, str)
        self.fileName = fileName
        self.lang = langFromExtension(fileName)
        self.caseSensitive = isCaseSecsitiveLang(self.lang)
        if not self.caseSensitive:
            lib = lib.lower()
        self.lib = lib
        self.hierarchyOnly = False
        self.primaryUnitsOnly = False
    
    def getParser(self):
        if self.lang == BaseParser.VERILOG:
            pcls = VerilogParser
        elif self.lang == BaseParser.VHDL:
            pcls = VhdlParser
        else:
            raise NotImplementedError()
         
        return pcls(self.caseSensitive, self.hierarchyOnly, self.primaryUnitsOnly)
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.fileName)
        
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
        return BaseParser.VERILOG
    elif n.endswith(".vhd"):
        return BaseParser.VHDL
    else:
        raise NotImplementedError("Can not resolve type of file \"%s\"" % (fileName))
    
def isCaseSecsitiveLang(lang):
    if  lang == BaseParser.VHDL:
        return False
    elif lang == BaseParser.VERILOG:
        return True
    else:
        raise ParserException("Invalid lang specification \"%s\" is not supported" % (str(lang)))

class ParserLoader():
    
    @staticmethod
    def getTopCtx(lang):
        if lang == BaseParser.VHDL:
            topCtxCls = BaseVhdlContext
        elif lang == BaseParser.VERILOG:
            topCtxCls = BaseVerilogContext
        else:
            raise NotImplementedError    
        
        topCtx = topCtxCls.getBaseCtx()
        topCtxCls.importFakeLibs(topCtx)
        return topCtx
    
    @staticmethod
    def parseFiles(fileList, debug=False):
        """
        @param fileList: list of ParserFileInfo object to parse in same context
        """
        
        lang = fileList[0].lang
        for f in fileList:
            assert f.lang == lang
        
        topCtx = ParserLoader.getTopCtx(lang)
        
        fileCtxs = []
        # start parsing all files    
        # collect parsed json from java parser and construct python objects
        for fileInfo in fileList:
            fName = fileInfo.fileName
            j = hdlConvertor.parse(fName, lang,
                                   hierarchyOnly=False,
                                   debug=debug)
            lib = fileInfo.lib
            parser = fileInfo.getParser()
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
            for pName, p in fileCtx.packages.items():
                try:
                    _p = ctx.packages[pName]
                except KeyError:
                    _p = None
                    
                if _p is None:                    
                    ctx.insertObj(p, fileInfo.caseSensitive, fileInfo.hierarchyOnly)
                else:
                    _p.update(p)
                # [TODO] update parent context
    
        return topCtx, fileCtxs
