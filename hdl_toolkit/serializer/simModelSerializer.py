from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from keyword import kwlist

from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.serializer.exceptions import SerializerException
from hdl_toolkit.serializer.nameScope import LangueKeyword, NameScope
from hdl_toolkit.serializer.simModelSerializer_Value import SimModelSerializer_value
from hdl_toolkit.serializer.simModelSerializer_ops import SimModelSerializer_ops
from hdl_toolkit.serializer.simModelSerializer_types import SimModelSerializer_types
from hdl_toolkit.serializer.utils import maxStmId
from hdl_toolkit.synthesizer.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthesizer.param import Param, evalParam
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase
from python_toolkit.arrayQuery import where


env = Environment(loader=PackageLoader('hdl_toolkit', 'serializer/templates_simModel'))
unitTmpl = env.get_template('modelCls.py')
processTmpl = env.get_template('process.py')
iftmpl = env.get_template("if.py")
assignTmpl = env.get_template("assign.py")

_indent = "    "
_indentCache = {}        
def getIndent(indentNum):
    try:
        return  _indentCache[indentNum]
    except KeyError:
        i = "".join([_indent for _ in range(indentNum)])   
        _indentCache[indentNum] = i
        return i

class SimModelSerializer(SimModelSerializer_value, SimModelSerializer_ops, SimModelSerializer_types):
    __keywords_dict = {kw: LangueKeyword() for kw in kwlist}
    __keywords_dict.update({'sim': LangueKeyword(),
                            'self': LangueKeyword()})
    
    @classmethod
    def getBaseNameScope(cls):
        s = NameScope(True)
        s.setLevel(1)
        s[0].update(cls.__keywords_dict)
        return s
    
    formater = lambda s: s
    
    @classmethod
    def asHdl(cls, obj):
        if isinstance(obj, UnitFromHdl):
            raise NotImplementedError()
        elif isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj)
        elif isinstance(obj, Value):
            return cls.Value(obj)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s" % (repr(obj)))
            return serFn(obj)
    
    @classmethod
    def stmAsHdl(cls, obj, indent=0):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, indent)
    
    @classmethod
    def FunctionContainer(cls, fn):
        raise NotImplementedError()
        # return fn.name
    @classmethod
    def Entity(cls, ent, scope):
        return ""
        
    @classmethod
    def Architecture(cls, arch, scope):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)
        
        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, (Enum, Array)) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, scope, declaration=True))

            v.name = scope.checkedName(v.name, v)
            variables.append(v)
            
        
        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope, 0))
        
        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)    
             
        return unitTmpl.render({
        "name"               : arch.getEntityName(),
        "ports"              : list(map(lambda p: (p.name, cls.HdlType(p._dtype)), arch.entity.ports)),
        "signals"            : list(map(lambda v: (v.name, cls.HdlType(v._dtype), cls.Value(evalParam(v.defaultVal))), variables)),
        "extraTypes"         : extraTypes_serialized,
        "processes"          : procs,
        "processObjects"     : arch.processes,
        "processesNames"     : map(lambda p: p.name, arch.processes),
        "componentInstances" : arch.componentInstances,
        "unsensitiveProcesses" : list(where(arch.processes, lambda proc: not proc.sensitivityList)),
        })
   
    @classmethod
    def Assignment(cls, a, indent=0):
        dst = a.dst
        if dst._dtype == a.src._dtype:
            if a.indexes is not None:
                raise NotImplementedError()
            else:
                return assignTmpl.render(indent = getIndent(indent),
                                         dst=dst.name,
                                         src=cls.Value(a.src),
                                         isEventDependent=a.isEventDependent)
                
        else:
            raise SerializerException("%s <= %s  is not valid assignment\n because types are different (%s; %s) " % 
                         (cls.asHdl(dst), cls.Value(a.src), repr(dst._dtype), repr(a.src._dtype)))
        
    @classmethod
    def comment(cls, comentStr):
        return "#" + comentStr.replace("\n", "\n#")     

    @classmethod
    def condAsHdl(cls, cond):
        cond = list(cond)
        return "[%s]" % (",".join(map(lambda x: cls.asHdl(x), cond)))
    
    @classmethod
    def IfContainer(cls, ifc, indent):
        cond = cls.condAsHdl(ifc.cond)
        ifTrue = ifc.ifTrue
        elIfs = []
        ifFalse = ifc.ifFalse
        
        for c, statements in ifc.elIfs:
            elIfs.append((cls.condAsHdl(c),
                          map(lambda obj: cls.stmAsHdl(obj, indent + 2), statements)))
        
        return iftmpl.render(indent=getIndent(indent),
                             cond=cond,
                             ifTrue=map(lambda obj: cls.stmAsHdl(obj, indent + 1), ifTrue),
                             elIfs=elIfs,
                             ifFalse=map(lambda obj: cls.stmAsHdl(obj, indent + 1), ifFalse))  
    
    @classmethod
    def SwitchContainer(cls, sw):
        switchOn = cls.condAsHdl(sw.switchOn, False)
        
        cases = []
        for key, statements in sw.cases:
            if key is not None:  # None is default
                key = cls.asHdl(key)
                
            cases.append((key, statements))  
        return VHDLTemplates.Switch.render(switchOn=switchOn,
                                           cases=cases)  
   
    @classmethod
    def WaitStm(cls, w):
        if w.isTimeWait:
            return "wait for %d ns" % w.waitForWhat
        elif w.waitForWhat is None:
            return "wait"
        else:
            raise NotImplementedError()
    
    @classmethod
    def HWProcess(cls, proc, scope, indentLvl):
        body = proc.statements
        proc.name = scope.checkedName(proc.name, proc)
        sensitivityList = sorted(where(proc.sensitivityList,
                                       lambda x : not isinstance(x, Param)), key=lambda x: x.name)
        
        return processTmpl.render({
              "name": proc.name,
              "sensitivityList": [s.name for s in sensitivityList],
              "stmLines": [ cls.stmAsHdl(s, 2) for s in body] })
           


