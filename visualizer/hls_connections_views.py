from flask import render_template, Response, request, jsonify
from flask.blueprints import Blueprint
import json, importlib, sys, os, glob, time
from stat import S_ISDIR

from hls_connections import serializeUnit, _defaultToJson
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit 


WORKSPACE_DIR = "workspace/" 
sys.path.append(WORKSPACE_DIR)

connectionsBp = Blueprint('connections', __name__, template_folder='templates/hls/')

def jsonResp(data):
    return Response(response=json.dumps(data, default=_defaultToJson), status=200, mimetype="application/json")


class FSEntry():
    def __init__(self, name, isGroup):
        self.isGroup = isGroup
        self.name = name
        self.size = ""
        self.type = ""
        self.dateModified = None
        self.children = []
    
    @classmethod
    def fromFile(cls, fileName):
        st = os.stat(fileName)
        
        self = cls(os.path.basename(fileName), S_ISDIR(st.st_mode))
        self.size = st.st_size
        #"%Y/%m/%d  %H:%M:%S"
        self.dateModified = time.strftime("%Y/%m/%d  %H:%M:%S", time.gmtime(st.st_ctime))
        
        return self
    
    def toJson(self):
        return {"group": self.isGroup,
                "data": { "name": self.name, "size": self.size, "type": self.type, "dateModified": self.dateModified},
                "children": []
                }


@connectionsBp.route(r'/hls/connections-save',  methods=[ 'POST'])
def connections_save():
    data = request.get_json()
    path = data["path"]
    path = os.path.join(WORKSPACE_DIR, path)
    if path.endswith(".json"):
        nodes = data["nodes"]
        nets = data["nets"]
        with open(path, mode='w') as f:
            json.dump({"name":data["name"],"nodes": nodes, "nets": nets}, f, indent=4)
        return jsonify( success = True) 
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
    path = os.path.join(WORKSPACE_DIR, path)
    if path.endswith(".py"):
        path = path[:-3]
        try:
            module = importlib.reload(sys.modules[path])
        except KeyError:
            module = importlib.import_module(path.replace("/","."))
        data = serializeUnit(module.interface, module.unit)       
    
    elif path.endswith(".json"):
        with open(path) as f:
            data =f.read()
    else:
        raise Exception("not implemented")
    return  Response(response=data, status=200, mimetype="application/json")
