
import re, json
from slimit.parser import Parser
# from slimit.visitors import nodevisitor
import slimit

from hls_toolkit.component import HLSCompoenet
from hls_toolkit.variable import  HLSVariable
from hls_toolkit.vhdl_serializer import serializeComponent

class ConfError(Exception):
    pass

class MissingConfAttribErr(ConfError):
    pass

jsonConfRegex = re.compile(r"var\s+(\S*_conf)\s*=\s*({.*});?", re.MULTILINE | re.DOTALL)

class HLSConf:
    requiredAtribs = ["interface"]
    def __init__(self, confDict): 
        self.__dict__.update(confDict)
        for a in self.requiredAtribs:
            if not hasattr(self, a):
                err = MissingConfAttribErr()
                err.atrib = a
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


def parseComponent(filename, conf):
    def typeOfVariable(varName):
        return conf.interface[varName]

    with open(filename) as f:
        parser = Parser()
        tree = parser.parse(f.read())
        fn = tree.children()[0]
        assert type(fn) == slimit.ast.FuncDecl
        # for node in nodevisitor.visit(tree):
        name = fn.identifier.value
        comp = HLSCompoenet(name)
        for param in fn.parameters:
            assert type(param) == slimit.ast.Identifier
            vn = param.value
            p = HLSVariable(vn, typeOfVariable(vn))
            comp.port.append(p)
        #    print(node)
    return comp  

if __name__ == '__main__':
    filename = "samples/basic_wire.js"
    conffilename = "samples/basic_wire_conf.js"
    conf = parseComponentConfiguration(conffilename)
    c = parseComponent(filename, conf)
    print( serializeComponent(c) )
