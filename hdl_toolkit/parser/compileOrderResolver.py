from python_toolkit.arrayQuery import single, where
from hdl_toolkit.parser.hierarchyExtractor import DesignFile
from hdl_toolkit.parser.defaults import defaultIgnoredRefs

class CircularReferenceError(Exception):
    pass


def resolveComplileOrder(fileInfos, topFile, ignoredRefs=defaultIgnoredRefs, debug=False):
    """
    Converts dependency dictionary to list of files in which they should be parsed.
    
    example:

    mainFile = hdlFiles[0] # choose our top file
    
    # sort files for parser (top file is at the end)
    dependencies = resolveComplileOrder(dep, mainFile, dependencies) 
    # now in dependencies are sorted fileInfos
    """
    designFiles = DesignFile.loadFiles(fileInfos, debug=debug)
    topFile = single(designFiles, lambda df: df.fileInfo is topFile)
    
    DesignFile.resolveDependencies(designFiles, ignoredRefs=ignoredRefs)
    
    dependenciesDec = []
    dependenciesDef = []
    
    
    _resolveComplileOrder(topFile, dependenciesDec, dependenciesDef, set(), set())
    
    # first all declarations, then definitions which are not in declarations
    fileOrder = dependenciesDec
    _dependenciesDec = set(dependenciesDec) 
    
    fileOrder.extend(where(dependenciesDef, lambda x: x not in _dependenciesDec))
    # return only file infos not design files
    return list(map(lambda x: x.fileInfo, fileOrder))

def _resolveComplileOrder(top, resolvedDec, resolvedDef, unresolvedDec, unresolvedDef):
    unresolvedDec.add(top)
    unresolvedDef.add(top)
    
    for child in top.depOnDeclarations:
        if child not in resolvedDec:
            if child in unresolvedDec:
                if top == child:
                    continue
                else:
                    raise CircularReferenceError('Circular reference detected: %s -&gt; %s' % (top, child))
            _resolveComplileOrder(child,resolvedDec, resolvedDef, unresolvedDec, unresolvedDef)
    resolvedDec.append(top)
    unresolvedDec.remove(top)        
    
    for child in top.depOnDefinitions:
        if child not in resolvedDef:
            if child in unresolvedDef:
                if top == child:
                    continue
                else:
                    raise CircularReferenceError('Circular reference detected: %s -&gt; %s' % (top, child))
            _resolveComplileOrder(child,resolvedDec, resolvedDef, unresolvedDec, unresolvedDef)
    resolvedDef.append(top)
    unresolvedDef.remove(top)  