from vhdl_toolkit.parser import Parser
from vhdl_toolkit.hierarchyExtractor import DesignFile


def entityFromFile(fileName, debug=False):
    lang = Parser.langFromExtension(fileName)
    
    ctx = Parser.parseFiles([fileName], lang, primaryUnitsOnly=True, debug=debug)
    if lang == Parser.VHDL:
        ctx = ctx['work']
    
    
    assert(len(ctx.entities.items()) == 1)
    ent = list(ctx.entities.items())[0][1]

    return ent

def loadCntxWithDependencies(hdlFiles, debug=False):
    """Load full context for first file"""
    dfs = DesignFile.loadFiles(hdlFiles)
    dep = DesignFile.fileDependencyDict(dfs)
    mainFile = hdlFiles[0]

    ctx = None
    firstTime = True
    lang = Parser.VHDL
    for d in list(dep[mainFile]) + [mainFile]:
        ctx = Parser.parseFiles([d], lang, hdlCtx=ctx, debug=debug)
        if firstTime:
            firstTime = False
            if lang == Parser.VHDL:
                ctx = ctx['work']
    return ctx