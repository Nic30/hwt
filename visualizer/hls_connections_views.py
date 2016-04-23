from flask import render_template, request, jsonify
from flask.blueprints import Blueprint
import json, importlib, sys, os, glob
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit 
from hls_connections import serializeUnit 
from connectionsJsonObj import FSEntry, jsonResp 


WORKSPACE_DIR = "../vhdl_toolkit/samples/" 
sys.path.append(WORKSPACE_DIR)

connectionsBp = Blueprint('connections', __name__, template_folder='templates/hls/')



@connectionsBp.route(r'/hls/connections-save', methods=[ 'POST'])
def connections_save():
    data = request.get_json()
    path = data["path"]
    path = os.path.join(WORKSPACE_DIR, path)
    if path.endswith(".json"):
        nodes = data["nodes"]
        nets = data["nets"]
        with open(path, mode='w') as f:
            json.dump({"name":data["name"], "nodes": nodes, "nets": nets}, f, indent=4)
        return jsonify(success=True) 
    else:
        raise Exception("Not implemented")

@connectionsBp.route('/connections/')
def connections():
    return render_template('hls/connections.html')

@connectionsBp.route('/connections-tests/')
def connections_test():
    return render_template('hls/connections_test.html')

@connectionsBp.route('/hls/connections-data-ls/')
@connectionsBp.route('/hls/connections-data-ls/<path:path>')
def connectionDataLs(path=""):
    data = []
    path = os.path.join(WORKSPACE_DIR, path) + "/*"
    for f in glob.glob(path):
        data.append(FSEntry.fromFile(f))
    return jsonResp(data)

@connectionsBp.route('/hls/connections-view/<path:path>')
def connectionView(path):
    path = os.path.join(WORKSPACE_DIR, path)
    with open(path) as f:
        data = Unit.fromJson(json.loads(f.read()), path)
    
    return jsonResp(data)

@connectionsBp.route('/hls/connections-data/<path:path>')
def connectionData(path):
    # path = os.path.join(WORKSPACE_DIR, path)
    # if path.endswith(".py"):
    #    path = path[:-3]
        # try:
        #    module = importlib.reload(sys.modules[path])
        # except KeyError:
        #    module = importlib.import_module(path.replace("/", "."))
    from vhdl_toolkit.samples.iLvl.axiLiteSlaveContainer import AxiLiteSlaveContainer
    u = AxiLiteSlaveContainer()
    #for _ in u._toRtl():
    #    pass
    data = serializeUnit(u)       
    
    # elif path.endswith(".json"):
    #    with open(path) as f:
    #        data = f.read()
    # else:
    #    raise Exception("not implemented")
    return jsonResp(data)
