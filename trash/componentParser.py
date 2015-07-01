
import re, json
from slimit.parser import Parser
import slimit
from hls_toolkit.component import HLSCompoenet
from hls_toolkit.variable import  HLSVariable
from hls_toolkit.vhdl_serializer import serializeComponent
from hls_toolkit.errors import MissingConfAttribErr, ConfError
from hls_toolkit.syntetizator_config import HLSSyntetizatorConfig
from vhdl_toolkit.simple_formater import formatVhdl


jsonConfRegex = re.compile(r"var\s+(\S*_conf)\s*=\s*({.*});?", re.MULTILINE | re.DOTALL)

def constructInterfaceFromStr(s):
    return eval("HLSSyntetizatorConfig.interfaces." + s)


class HLSConf:
    requiredAtribs = ["interfaces"]
    def __init__(self, confDict): 
        self.__dict__.update(confDict)
        for a in self.requiredAtribs:
            if not hasattr(self, a):
                err = MissingConfAttribErr()
                err.atrib = a
                raise err
        # parse interfaces
        for i_key in self.interfaces:
            i = self.interfaces[i_key]
            try:
                self.interfaces[i_key] = constructInterfaceFromStr(i)
            except Exception as e:
                err = ConfError()
                err.__dict__.update(e.__dict__)
                raise err
                
def parseComponentConfiguration(fileName):
    with open(fileName) as f:
        s = f.read()
        m = jsonConfRegex.match(s)
        if m:
            conf = json.loads(m.group(2))
        else:
            err = ConfError()
            err.filename = fileName 
            raise err
    c = HLSConf(conf)
    return c

class DepListNode():
    def __init__(self, variable):
        self.variable = variable
        self.dependentOn = []

def parseComponentBody(fn, comp):
    def dependsOn(stages, precursors):
        for s in stages:
            
    for ch in fn.children():
        if type(ch) == slimit.ast.ExprStatement:
            t = type(ch.expr)
            if t == slimit.ast.Assign:
                comp.stages.append()
    

def parseComponent(filename, conf):
    def typeOfVariable(varName):
        return conf.interfaces[varName]

    with open(filename) as f:
        parser = Parser()
        tree = parser.parse(f.read())
        fn = tree.children()[0]
        assert type(fn) == slimit.ast.FuncDecl
        name = fn.identifier.value
        comp = HLSCompoenet(name)
        for param in fn.parameters:
            assert type(param) == slimit.ast.Identifier
            vn = param.value
            p = HLSVariable(vn, typeOfVariable(vn))
            comp.port.append(p)
        parseComponentBody(fn, comp)
    return comp  

if __name__ == '__main__':
    filename = "samples/basic_wire.js"
    conffilename = "samples/basic_wire_conf.js"
    conf = parseComponentConfiguration(conffilename)
    c = parseComponent(filename, conf)
    print(formatVhdl(serializeComponent(c)))
