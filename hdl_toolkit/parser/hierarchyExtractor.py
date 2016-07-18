from copy import copy
import hdlConvertor
from python_toolkit.arrayQuery import arr_any
from hdl_toolkit.parser.referenceCollector import collectReferences
from hdl_toolkit.parser.defaults import defaultIgnoredRefs

class UnresolvedReferenceError(Exception):
    pass

class FileBoundedDict(dict):
    pass

def includeRefToDict(d, ref, obj):
    nLastIndx = len(ref.names) - 1
    for i, n in enumerate(ref.names):
        try:
            _d = d[n]
        except KeyError:
            _d = FileBoundedDict()
            d[n] = _d

        d = _d
        if i == nLastIndx:
            _d.designFile = obj
             

class DesignFile():
    """
    Wrapper around references of file
    """
    def __init__(self, fileInfo, jCtx):
        """
        @param fileInfo: ParserFileInfo objects contains filename, langue etc
        @param jCtx: JSON serialized HDL AST (output from hdlConvertor.parse) 
        """
        self.fileInfo = fileInfo
        self.required, self.declared, self.defined = collectReferences(jCtx, scope=[fileInfo.lib])
        self.unresolvedDep = copy(self.required) 
        
        self.depOnDefinitions = set()  # this file depends on definitions in DesignFiles 
        self.depOnDeclarations = set()  # declaration in this file has definition in DesignFiles

    @staticmethod
    def refMatch(iHad, iWontToHave):
        iwNames = iter(iWontToHave.names)
        ihNames = iter(iHad.names)
        # [TODO] not ideal solution will not work with other lib
        if iWontToHave.names[0] == 'work':
            next(iwNames)
        if iHad.names[0] == 'work':
            next(ihNames)
        for nh in ihNames:
            try:
                nw = next(iwNames)
            except StopIteration:
                return True
            if nh != nw:
                return False
            try:
                nw = next(iwNames)
            except StopIteration:
                return True

    @staticmethod
    def buildDefDecDict(allDesignFiles):
        topDef = {}
        topDec = {}
        
        for df in allDesignFiles:
            for d in df.declared:
                if hasattr(d, "defined") and d.defined:
                    includeRefToDict(topDef, d, df)
                includeRefToDict(topDec, d, df)
        
        for df in allDesignFiles:
            for d in df.defined:
                includeRefToDict(topDef, d, df)
                
        return topDec, topDef
    
    @staticmethod
    def findInGlobals(globalDict, ref, scope=[]):
        """
        @return: Parser of file info where ref is defined or FileBoundedDict with designFile property
        """
        names = ref.names
        try:
            names = scope + list(ref.names)
            top = globalDict
            for n in names:
                top = top[n]
        except KeyError:
            top = globalDict
            names = ref.names
            for n in names:
                top = top[n]
                
        return top
            
    
    def discoverDependentOnFiles(self, globalDecDict, globalDefDict, ignoredRefs=[]):
        """
        Discover on which files is this file dependent
        """
        imported = {}
        for d in self.required:
            if arr_any(ignoredRefs, lambda x: DesignFile.refMatch(d, x)):
                continue
            
            try:
                fi = DesignFile.findInGlobals(imported, d, scope=[self.fileInfo.lib])
            except KeyError:
                fi = None
            
            if d.all:
                _imported = DesignFile.findInGlobals(globalDecDict, d)
                imported.update(_imported) 

            if fi is None:
                try:
                    fi = DesignFile.findInGlobals(globalDecDict, d, scope=[self.fileInfo.lib])
                except KeyError:
                    raise UnresolvedReferenceError("%s: require to import %s" % 
                                            (self.fileInfo.fileName, str(d)))
                if fi is not self:
                    if isinstance(fi, FileBoundedDict):
                        fi = fi.designFile
                    
                    self.depOnDeclarations.add(fi)
        
        for d in self.declared:
            try:
                fi = DesignFile.findInGlobals(globalDefDict, d, scope=[self.fileInfo.lib])
            except KeyError:
                raise UnresolvedReferenceError("%s: can not find definition of %s" % 
                                       (self.fileInfo.fileName, str(d)))
                
            if fi is not self:
                if isinstance(fi, FileBoundedDict):
                    fi = fi.designFile
                self.depOnDefinitions.add(fi)
            
        
    @staticmethod
    def loadFiles(fileInfos, debug=False):
        """
        load ParserFileInfo and build DesignFile for it 
        """
        designFiles = []
        for fi in fileInfos:
            jCtx = hdlConvertor.parse(fi.fileName, fi.lang,
                                       hierarchyOnly=True,
                                       debug=debug)
            d = DesignFile(fi, jCtx)
            designFiles.append(d)
        
        return designFiles

    @staticmethod
    def resolveDependencies(designFiles, ignoredRefs=defaultIgnoredRefs):
        """
        collect depOnDefinitions and depOnDeclarations
        """
        globalDecDict, globalDefDict = DesignFile.buildDefDecDict(designFiles)
        for df in designFiles:
            df.discoverDependentOnFiles(globalDecDict, globalDefDict, ignoredRefs)


