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
    def __init__(self, unit, portItem, portIndexLookup ):
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
                outIndx+=1
            else:
                rec.inputs[id(pi)] = inIndx
                inIndx+=1
                
        self.cache[id(unit)] = rec
    def lookup(self, unit, portItem):
        unitId = id(unit)
        if unitId not in self.cache.keys():
            self._index(unit)
        
        rec =  self.cache[unitId]
        if portItem.direction == PortItem.typeOut:   
            portArr =  rec.outputs
        else:
            portArr =  rec.inputs
        return portArr[id(portItem)]
    



@connectionsBp.route('/connections/')
def connections():
    return render_template('hls/connections.html')

@connectionsBp.route('/connections-tests/')
def connections_test():
    return render_template('hls/connections_test.html')

    
@connectionsBp.route('/hls/connections/data.json')
def connectionData():
    interf, c = superDMA_complex()
    c.synthetize(interf)
    nets = []
    indxLookup = PortIndexLookup()
    for s in c.signals:
        driver = s.getDriver()
        if driver and isinstance(driver, PortConnection):
            n = {"name":s.name, "source": None, "targets": []}
            n["source"] = ConnectionInfo(driver.unit, driver.portItem, indxLookup)
            for expr in s.expr:
                if isinstance(expr, PortConnection) and expr.portItem.direction == PortItem.typeIn:
                    n["targets"].append(ConnectionInfo(expr.unit, expr.portItem, indxLookup))
            if len(n["targets"]) >0:
                nets.append(n)
    
        
    dat =json.dumps( {"nodes":list(c.subUnits), "nets" : nets }, default=_defaultToJson)
    return Response(response= dat, status=200, mimetype="application/json")