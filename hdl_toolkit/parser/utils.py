from hdl_toolkit.parser.loader import ParserFileInfo, ParserLoader
from python_toolkit.arrayQuery import single
from hdl_toolkit.parser.compileOrderResolver import resolveComplileOrder

def getLib(fileName, fileInfos):
    return single(fileInfos, lambda x: x.fileName == fileName).lib

def entityFromFile(fileName, debug=False):
    fi = ParserFileInfo(fileName, 'work')
    fi.primaryUnitsOnly = True
    
    _, fileCtxs = ParserLoader.parseFiles([fi], debug=debug)
    c = fileCtxs[0]
    
    assert len(c.entities.items()) == 1
    ent = list(c.entities.items())[0][1]
    return ent

def loadCntxWithDependencies(hdlFiles, debug=False):
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
    
    mainFile = fileInfos[0]
    
    dependencies = resolveComplileOrder(fileInfos, mainFile)

    depFileInfos = []
    for d in dependencies:
        fi = ParserFileInfo(d, getLib(d, fileInfos))
        depFileInfos.append(fi)
    
    _, fCtxs = ParserLoader.parseFiles(depFileInfos, debug=debug)

    return single(fCtxs, lambda x: x.name == mainFile)
