from hdl_toolkit.parser.baseParser import BaseParser
from hdl_toolkit.hdlObjects.reference import HdlRef



def collectReferences(jCtx, scope=[]):
    """
    walk objects in jCtx and discovery required and declared references
    
    @return: tuple (required, declared, defined) which are lists of HdlRef objects
    """
    required = []
    declared = []
    defined = []
    
    caseSensitive = False
    bp = BaseParser(caseSensitive)
    
    ref = lambda names: HdlRef(scope + names, caseSensitive)
    
    for i in jCtx["imports"]:
        _i = bp.hdlRefFromJson(i)
        required.append(_i)
        
    for e in jCtx["entities"]:
        eName = bp._hdlId(e['name'])
        _e = ref([eName])
        declared.append(_e)
    
    for a in jCtx["architectures"]:
        entityName = bp._hdlId(a['entityName'])
        e = ref([entityName])
        defined.append(e)
        
        for c in a['componentInstances']:
            entRef = bp.hdlRefFromJson(c['entityName'])
            required.append(entRef)
  
        
    for ph in jCtx["packageHeaders"]:
        pName = bp._hdlId(ph['name'])
        p = ref([pName])
        declared.append(p)
        for c in ph["components"]:
            cname = bp._hdlId(c['name'])
            _c = ref([pName, cname])
            _c.defined = True
            declared.append(_c)
            
        for v in ph["variables"]:
            vname = bp._hdlId(v['name'])
            _v = ref([pName, vname])
            _v.defined = True
            declared.append(_v)
        
        for f in ph["functions"]:
            fname = bp._hdlId(f['name'])
            _f = ref([pName, fname])
             
            declared.append(_f)
        
        
    for p in jCtx["packages"]:
        pName = bp._hdlId(p['name'])
        _p = ref([pName])
        defined.append(_p)
        for c in p["components"]:
            cname = bp._hdlId(c['name'])
            _c = ref([pName, cname])
            defined.append(_c)
            
        for v in p["variables"]:
            raise NotImplementedError()
        
        for f in p["functions"]:
            fname = bp._hdlId(f['name'])
            _f = ref([pName, fname])
             
            defined.append(_f)
    
    for v in jCtx["variables"]:
        vName = bp._hdlId(v['name'])
        _v = ref([vName])
        defined.append(_v)
        defined.append(_v)
        
    
    return (required, declared, defined)
