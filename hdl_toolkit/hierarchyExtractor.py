from python_toolkit.arrayQuery import arr_any
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.package import PackageHeader
from hdl_toolkit.hdlObjects.reference import HdlRef
from hdl_toolkit.nonRedefDict import RedefinitionErr
from hdl_toolkit.hdlContext import HDLCtx, RequireImportErr
from hdl_toolkit.parser.loader import ParserLoader, getFileInfoFromObj 

class CircularReferenceError(Exception):
    pass


def depResolve(dep, k, resolved, unresolved):
    """
    Converts dependency dictionary to list of files in which they should be parsed.
    
    example:
    dfs = DesignFile.loadFiles(fileInfos) # get design file contexts
    dep = DesignFile.fileDependencyDict(dfs) # discovery dependeny between files 
    mainFile = hdlFiles[0] # choose our top file
    
    dependencies = []
    depResolve(dep, mainFile, dependencies, set()) # sort files for parser (top file is at the end)
    # now in dependencies are sorted fileInfos
    
    """
    unresolved.add(k)
    for child in dep[k]:
        if child not in resolved:
            if child in unresolved:
                if k == child:
                    continue
                else:
                    raise CircularReferenceError('Circular reference detected: %s -&gt; %s' % (k, child))
            depResolve(dep, child, resolved, unresolved)
    resolved.append(k)
    unresolved.remove(k)        

class DesignFile():
    """
    Wrapper around context of file
    """
    def __init__(self, fileName, hdlCtx):
        """
        @param fileName: filename of file that hdlCtx comes from
        @param hdlCtx: hdl context of file
        """
        self.fileName = fileName
        self.hdlCtx = hdlCtx
        self.importedNames = HDLCtx("imports", None)
        self.dependentOnFiles = set()

    def allDefinedRefs(self):
        """
        iterate over all tuples (reference, referenced object)
        """
        def allDefinedRefsInCtx(ctx, nameList):
            for n, obj in ctx.items():
                if isinstance(obj, Entity):
                    yield (HdlRef(nameList + [n], False), obj)
                elif isinstance(obj, PackageHeader):
                    if not obj._isDummy:
                        yield (HdlRef(nameList + [n], False), obj)
                        for k in obj:
                            yield (HdlRef(nameList + [n, k], False), obj[k])
                elif isinstance(obj, HDLCtx):
                    yield from allDefinedRefsInCtx(obj, nameList + [n])
        yield from allDefinedRefsInCtx(self.hdlCtx, [])
        
    @staticmethod
    def getAllTopCtxs(designFiles):
        def getTopCtx(df):
            top = df.hdlCtx
            while top.parent is not None:
                top = top.parent
            return top
        
        def uniq(seq): 
            seen = {}
            for item in seq:
                marker = id(item)
                seen[marker] = item
                
            return list(seen.values())        
        return uniq(map(getTopCtx, designFiles))

    def discoverImports(self, allDesignFiles, ignoredRefs=[]):
        """
        discover all imported names in design file
        """
        topCtxs = DesignFile.getAllTopCtxs(allDesignFiles)
        
        for d in self.allDependencies(importsOnly=True):
            if arr_any(ignoredRefs, lambda x: DesignFile.refMatch(d, x)):
                continue
            
            imp = None
            for c in topCtxs:
                try:
                    imp = c.lookupGlobal(d)
                    break
                except RequireImportErr:
                    pass
            if imp is None:
                raise Exception("%s: require to import %s and it is not defined in any file" % 
                                (self.fileName, str(d)))
            if d.all:
                try:
                    for k, v in imp.items():
                        self.importedNames[k] = v
                except RedefinitionErr:
                    pass
            else:
                k = imp.name
                self.importedNames[k] = imp

    def allDependencies(self, importsOnly=False):
        """
        iterate all dependencies of file
        """
        def allDependenciesForCtx(ctx, nameList):
            # packageHeader < ent|arch|package
            # ent <- arch
            for _, obj in ctx.items():
                if isinstance(obj, Entity):
                    # components in packages does not have dependencies
                    if hasattr(obj, "dependencies"):
                        yield from obj.dependencies
                elif isinstance(obj, PackageHeader) and obj._isDummy:
                    yield HdlRef(nameList + [obj.name], False)
                elif isinstance(obj, HDLCtx):
                    for a in obj.architectures:
                        yield from a.dependencies
                        if not importsOnly:
                            yield HdlRef(nameList + [a.entityName], False)
                            for ci in a.componentInstances:
                                yield ci.entityRef
                    yield from allDependenciesForCtx(obj, nameList + [obj.name])
                # else:
                #    raise NotImplementedError(
                #          "Not implemented for object of type %s" %
                #           (obj.__class__.__name__))
        yield from allDependenciesForCtx(self.hdlCtx, [])

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

    # @staticmethod
    # def findReference(ref, allDesignFiles):
    #    """
    #    find reference in allDesignFiles
    #    @return: iterator over tuples (filename, reference, defined object)
    #    """
    #    for df in allDesignFiles:
    #            for defDep, obj in df.allDefinedRefs():
    #                if DesignFile.refMatch(defDep, ref):
    #                    return (df.fileName, defDep, obj)
    #
    def discoverDependentOnFiles(self, allDesignFiles, ignoredRefs=[]):
        """
        Discover on which files is this file dependent
        """
        topCtxs = DesignFile.getAllTopCtxs(allDesignFiles)
        
        def isAlreadyImported(ref):
            if len(ref.names) != 1:
                return False
            return ref.names[0] in self.importedNames

        self.discoverImports(allDesignFiles, ignoredRefs=ignoredRefs)
        for d in self.allDependencies():
            if arr_any(ignoredRefs, lambda x: DesignFile.refMatch(d, x)):
                continue
            if isAlreadyImported(d):
                continue
            df = None
            for c in topCtxs:
                try:
                    df = c.lookupGlobal(d)
                except RequireImportErr:
                    pass

            if df is None:
                raise Exception(
                 "%s: require to import %s and it is not defined in any file" % 
                 (self.fileName, str(d)))
            fi = getFileInfoFromObj(df)
            self.dependentOnFiles.add(fi.fileName)

    @staticmethod
    def loadFiles(filesInfos, parallel=True):
        for fi in filesInfos:
            fi.hierarchyOnly = True
        
        _, fileContexts = ParserLoader.parseFiles(filesInfos, timeoutInterval=180)
        designFiles = []
        for fCtx in fileContexts:
            d = DesignFile(fCtx.name, fCtx)
            designFiles.append(d)
        
        return designFiles

    @staticmethod
    def fileDependencyDict(designFiles, ignoredRefs=[HdlRef(["ieee"], False),
                                                     HdlRef(["std"], False)]):
        depDict = {}
        for df in designFiles:
            df.discoverDependentOnFiles(designFiles, ignoredRefs)
            depDict[df.fileName] = df.dependentOnFiles
        return depDict


def findFileWhereNameIsDefined(designFiles, name):
    targetRef = HdlRef([name])
    for df in designFiles:
        refs = df.allDefinedRefs()
        for ref in refs:
            if DesignFile.refMatch(ref, targetRef):
                return df
