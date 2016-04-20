from vhdl_toolkit.parser import Parser
from vhdl_toolkit.hierarchyExtractor import DesignFile
from python_toolkit.arrayQuery import where


def entityFromFile(fileName, debug=False):
    lang = Parser.langFromExtension(fileName)
    
    ctx = Parser.parseFiles([fileName], lang, primaryUnitsOnly=True, debug=debug)
    if lang == Parser.VHDL:
        ctx = ctx['work']
    
    
    assert(len(ctx.entities.items()) == 1)
    ent = list(ctx.entities.items())[0][1]

    return ent

def loadCntxWithDependencies(hdlFiles, debug=False, multithread=True):
    """Load full context for first file"""
    
    dfs = []
    libs = set()
    for f in hdlFiles:
        if not isinstance(f, str):
            libs.add(f[0])
            
    filesWithoutLib = list(where(hdlFiles, lambda x : isinstance(x, str)))
    _dfs = DesignFile.loadFiles(filesWithoutLib, parallel=multithread)
    dfs.extend(_dfs)
    for lib in libs:
        libFiles = list(map(lambda x: x[1],
                            where(hdlFiles, lambda x : not isinstance(x, str) and x[0] == lib)
                            ))
        _dfs = DesignFile.loadFiles(libFiles, libName=lib, parallel=multithread)
        dfs.extend(_dfs)   
    
    dep = DesignFile.fileDependencyDict(dfs)
    mainFile = hdlFiles[0]
    # [TODO] implement real loading from multiple libs
    ctx = None
    firstTime = True
    lang = Parser.VHDL
    
    def dep_resolve(k, resolved, unresolved):
        unresolved.add(k)
        for child in dep[k]:
            if child not in resolved:
                if child in unresolved:
                    if k == child:
                        continue
                    else:
                        raise Exception('Circular reference detected: %s -&gt; %s' % (k, child))
                dep_resolve(child, resolved, unresolved)
        resolved.append(k)
        unresolved.remove(k)
    dependencies = []
    dep_resolve(mainFile, dependencies, set())

    for d in dependencies:
        ctx = Parser.parseFiles([d], lang, hdlCtx=ctx, debug=debug, hierarchyOnly=True)
        if firstTime:
            firstTime = False
            if lang == Parser.VHDL:
                ctx = ctx['work']
    return ctx
