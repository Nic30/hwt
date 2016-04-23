from vhdl_toolkit.parserLoader import ParserFileInfo, ParserLoader
from vhdl_toolkit.hierarchyExtractor import DesignFile
from python_toolkit.arrayQuery import single

def depResolve(dep, k, resolved, unresolved):
    unresolved.add(k)
    for child in dep[k]:
        if child not in resolved:
            if child in unresolved:
                if k == child:
                    continue
                else:
                    raise Exception('Circular reference detected: %s -&gt; %s' % (k, child))
            depResolve(dep, child, resolved, unresolved)
    resolved.append(k)
    unresolved.remove(k)


def getLib(fileName, fileInfos):
    return single(fileInfos, lambda x: x.fileName == fileName).lib

def entityFromFile(fileName, debug=False):
    fi = ParserFileInfo(fileName, 'work')
    fi.primaryUnitsOnly = True
    
    _, fileCtxs = ParserLoader.parseFiles([fi], debug=debug)
    c = fileCtxs[0]
    
    assert(len(c.entities.items()) == 1)
    ent = list(c.entities.items())[0][1]
    return ent

def loadCntxWithDependencies(hdlFiles, debug=False, multithread=True):
    """Load full context for first file"""
    fileInfos = []
    for f in hdlFiles:
        if isinstance(f, str):
            fi = ParserFileInfo(f, 'work')
        elif isinstance(f, tuple):
            fi = ParserFileInfo(f[1], f[0])
        else:
            raise NotImplementedError()
        fileInfos.append(fi)
    
    dfs = DesignFile.loadFiles(fileInfos, parallel=multithread)
    
    dep = DesignFile.fileDependencyDict(dfs)
    mainFile = hdlFiles[0]
    
    dependencies = []
    depResolve(dep, mainFile, dependencies, set())

    depFileInfos = []
    for d in dependencies:
        fi = ParserFileInfo(d, getLib(d, fileInfos))
        fi.hierarchyOnly = False
        fi.functionsOnly = (mainFile != d)
        depFileInfos.append(fi)
    
    _, fCtxs = ParserLoader.parseFiles(depFileInfos, debug=debug)

    return single(fCtxs, lambda x: x.name == mainFile)
