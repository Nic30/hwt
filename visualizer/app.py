import os, sys
from flask import Flask, render_template
from flask.helpers import send_from_directory

from vhdl_toolkit.hierarchyExtractor import DesignFile
from hls_connections_views import connectionsBp
from python_toolkit.fileHelpers import find_files

sys.path.append("..")  # [hotfix] to make visualizer run after downloading from git

app = Flask("Visualizer")

# for loading all static files (antipatent, but it is necessary because app is not deployed on webserver0
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

# http://roberto.open-lab.com/2012/06/14/the-javascript-gantt-odyssey/
@app.route('/gantt/')
def gantt():
    return render_template('hls/gantt_chart.html', ganttTasks=[], ganttTaskNames=[])

# http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
@app.route('/dependency')
def dependencyGraph():
    def convertToRelativePaths(root, depDict):
        outDict = {}
        for f, dep in depDict.items():
            f = os.path.relpath(f, root)
            depSet = set()
            outDict[f] = depSet
            for d in dep:
                depSet.add(os.path.relpath(d, root))
        return outDict
    unisimFiles = ['/opt/Xilinx/Vivado/2015.2/data/vhdl/src/unisims/retarget_VCOMP.vhd']
    workspace = "/home/nic30/Downloads/fpgalibs/src/"
    files = []
    #files.extend(find_files(workspace, '*.vhd'))
    files.extend(find_files(workspace + 'util/', '*.vhd'))
    unisimDesFiles = DesignFile.loadFiles(unisimFiles, libName='unisim')
    workDesFiles = DesignFile.loadFiles(files)
    depDict = DesignFile.fileDependencyDict(workDesFiles + unisimDesFiles)
    depDict = convertToRelativePaths(workspace, depDict)
    nodes = []
    links = []
    indexes = {}
    indx = 0
    for file in depDict:
        indexes[file] = indx
        indx += 1
        nodes.append({"name":file, 'group':1})
    
    for file, connections in depDict.items():
        for c in connections:
            links.append({"source":indexes[file],
                          'target':indexes[c],
                          "value":1})
    
    return render_template('hls/dependency.html', nodes=nodes, links=links)
app.register_blueprint(connectionsBp)
    
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')
