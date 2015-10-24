from flask import render_template, Response
from vhdl_toolkit.variables import PortItem
from vhdl_toolkit.samples.superDMA_complex import superDMA_complex
from vhdl_toolkit.synthetisator.signal import PortConnection
import json
from flask.blueprints import Blueprint


connectionsBp = Blueprint('connections', __name__, template_folder='templates/hls/')

def _defaultToJson(obj):
    if hasattr(obj, "toJson"):
        return obj.toJson()
    
    return obj.__dict__

class ConnectionInfo():
    """Net connection info"""
    def __init__(self, unit, portItem, portIndexLookup):
        self.portItem = portItem
        self.unit = unit
        self.index = portIndexLookup.lookup(unit, portItem)
        
    def toJson(self):
        return {"name": self.portItem.name, "portIndex":  self.index, "id": id(self.unit) }

class PortIndexLookup():
    """ class for searching port indexes of portItems in units"""
    class LookupRecord():
        def __init__(self):
            self.inputs = {}
            self.outputs = {}
    def __init__(self):
        self.cache = {}
    def _index(self, unit):
        rec = PortIndexLookup.LookupRecord()
        inIndx = 0
        outIndx = 0
        for pi in unit.port:
            if pi.direction == PortItem.typeOut:
                rec.outputs[id(pi)] = outIndx
                outIndx += 1
            else:
                rec.inputs[id(pi)] = inIndx
                inIndx += 1
                
        self.cache[id(unit)] = rec
    def lookup(self, unit, portItem):
        unitId = id(unit)
        if unitId not in self.cache.keys():
            self._index(unit)
        
        rec = self.cache[unitId]
        if portItem.direction == PortItem.typeOut:   
            portArr = rec.outputs
        else:
            portArr = rec.inputs
        return portArr[id(portItem)]
    



@connectionsBp.route('/connections/')
def connections():
    return render_template('hls/connections.html')

@connectionsBp.route('/connections-tests/')
def connections_test():
    return render_template('hls/connections_test.html')

    
@connectionsBp.route('/hls/connections/data.json')
def connectionData():
    # interf, c = superDMA_complex()
    # c.synthetize(interf)
    # nets = []
    # indxLookup = PortIndexLookup()
    # for s in c.signals:
    #    driver = s.getDriver()
    #    if driver and isinstance(driver, PortConnection):
    #        n = {"name":s.name, "source": None, "targets": []}
    #        n["source"] = ConnectionInfo(driver.unit, driver.portItem, indxLookup)
    #        for expr in s.expr:
    #            if isinstance(expr, PortConnection) and expr.portItem.direction == PortItem.typeIn:
    #                n["targets"].append(ConnectionInfo(expr.unit, expr.portItem, indxLookup))
    #        if len(n["targets"]) >0:
    #            nets.append(n)
    
    nodes = [{
        "id" : 0,
        "name" : "smaller one",
        "inputs" : [ {"name" :"clk"}, {"name" :"rst"} ],
        "outputs" : [ {"name" :"outA"}, {"name" :"outB"} ]
    }, {
        "id": 1,
        "name" : "biggest",
        "inputs" : [ {"name" :"clk"}, {"name" :"rst"}, {"name" :"inA"}, {"name" :"inB"}],
        "outputs" : [{"name" : "outA2"}, {"name" :"outB2"} ]    
    }, {
        "id": 2,
        "name" : "clk",
        "inputs" : [],
        "outputs" : [{"name" :"clk"}]    
    }, {
        "id": 3,
        "name" : "rst",
        "inputs" : [],
        "outputs" : [{"name" :"rst"}]    
    }
             , {
        "id": 4,
        "name" : "dummy",
        "inputs" : [{"name" :"clk"}, {"name" :"rst"}],
        "outputs" : [{"name" :"a"}, {"name" :"b"}, {"name" :"c"}, {"name" :"d"}]    
    },
              {
        "id" : 5,
        "name" : "selfReference",
        "inputs" : [ {"name" :"clk"}, {"name" :"inC"}, {"name" :"inD"} ],
        "outputs" : [ {"name" :"c"}, {"name" :"d"} ]
    },
 {
        "id" : 6,
        "name" : "outA",
        "isExternalPort" : True,
        "inputs" : [{"name" :"outA"} ],
        "outputs" : [ ]
    }
]
   
    nets = [
            {
        "name" : "a",
        "source" : {
            "id" : 5,
            "portIndex" : 0
        },
        "targets" : [{
            "id" : 6,
            "portIndex" : 0
        }]},
         {
        "name" : "clk",
        "source" : {
            "id" : 2,
            "portIndex" : 0
        },
        "targets" : [ {
            "id" : 0,
            "portIndex" : 0
        }, {
            "id" : 1,
            "portIndex" : 0
        }]
        }, {
        "name" : "rst",
        "source" : {
            "id" : 3,
            "portIndex" : 0
        },
        "targets" : [ {
            "id" : 0,
            "portIndex" : 1
        }, {
            "id" : 1,
            "portIndex" : 1
        } ]
    }, {
        "name" : "A",
        "source" : {
            "id" : 0,
            "portIndex" : 0
        },
        "targets" : [ {
            "id" : 1,
            "portIndex" : 2
        } ]
    }, {
        "name" : "B",
        "source" : {
            "id" : 0,
            "portIndex" : 1
        },
        "targets" : [ {
            "id" : 1,
            "portIndex" : 3
        } ]
    }
            , {
        "name" : "C",
        "source" : {
            "id" : 5,
            "portIndex" : 0
        },
        "targets" : [ {
            "id" : 5,
            "portIndex" : 1
        } ]
    }
, {
        "name" : "D",
        "source" : {
            "id" : 5,
            "portIndex" : 1
        },
        "targets" : [ {
            "id" : 5,
            "portIndex" : 2
        } ]
    }
    ]

        
    dat = json.dumps({"nodes":nodes, "nets" : nets }, default=_defaultToJson)
    return Response(response=dat, status=200, mimetype="application/json")
