import json, importlib, sys, os, glob, time
from flask.blueprints import Blueprint
from flask import render_template, Response
from hls_connections import serializeUnit, _defaultToJson
from stat import S_ISDIR

WORKSPACE_DIR = "workspace/" 
sys.path.append(WORKSPACE_DIR)

connectionsBp = Blueprint('connections', __name__, template_folder='templates/hls/')

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
    
    return Response(response=json.dumps(data, default=_defaultToJson), status=200, mimetype="application/json")



@connectionsBp.route('/hls/connections-data/<path:path>')
def connectionData(path):
    if path.endswith(".py"):
        path = path[:-3]
        try:
            module = importlib.reload(sys.modules[path])
        except KeyError:
            module = importlib.import_module(path.replace("/","."))
        dataDict = serializeUnit(module.interface, module.unit)       
        data = json.dumps(dataDict, default=_defaultToJson)
    
    elif path.endswith(".json"):
        with open(path) as f:
            data =f.read()
    else:
        raise Exception("not implemented")
    return Response(response=data, status=200, mimetype="application/json")
