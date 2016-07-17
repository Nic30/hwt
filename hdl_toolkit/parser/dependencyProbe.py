from hdl_toolkit.parser.baseParser import BaseParser
from hdl_toolkit.hdlObjects.reference import HdlRef


def collectReferences(jCtx):
    """
    walk objects in jCtx and discovery required and declared references
    
    @return: tuple (required, defined) which are lists of HdlRef objects
    """
    required = []
    defined = []
    caseSensitive = False
    bp = BaseParser(caseSensitive)
    
    for i in jCtx["imports"]:
        _i = bp.hdlRefFromJson(i)
        required.append(_i)
        
    for e in jCtx["entities"]:
        eName = bp._hdlId(e['name'])
        _e = HdlRef([eName], caseSensitive)
        defined.append(_e)
    
    for a in jCtx["architectures"]:
        entityName = bp._hdlId(a['entityName'])
        e = HdlRef([entityName], caseSensitive)
        required.append(e)
        for c in a['componentInstances']:
            entRef = bp.hdlRefFromJson(c['entityName'])
            required.append(entRef)
  
        
    for ph in jCtx["packageHeaders"]:
        pName = bp._hdlId(ph['name'])
        p = HdlRef([pName], caseSensitive)
        defined.append(p)
        for c in ph["components"]:
            cname = bp._hdlId(c['name'])
            defined.append(HdlRef([pName, cname], caseSensitive))
        for v in ph["variables"]:
            raise NotImplementedError()
        for f in ph["functions"]:
            fname = bp._hdlId(f['name'])
            defined.append(HdlRef([pName, fname], caseSensitive))
        
        
    for p in jCtx["packages"]:
        pName = bp._hdlId(p['name'])
        _p = HdlRef([pName], caseSensitive)
        required.append(_p)
    
    for v in jCtx["variables"]:
        raise NotImplementedError()
        
    
    return (required, defined)