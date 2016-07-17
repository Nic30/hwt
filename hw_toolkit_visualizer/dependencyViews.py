import os
from flask.blueprints import Blueprint
from hdl_toolkit.parser.hierarchyExtractor import DesignFile
from python_toolkit.fileHelpers import find_files
from flask import render_template
from hdl_toolkit.parser.loader import ParserFileInfo


dependenciesBp = Blueprint('dependencies', __name__, template_folder='templates/dependencies/')



# http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
@dependenciesBp.route('/dependencies/')
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
    #unisimFiles = ['/opt/Xilinx/Vivado/2015.2/data/vhdl/src/unisims/retarget_VCOMP.vhd']
    # workspace = "/home/nic30/Downloads/fpgalibs/src/hfer/"
    workspace = "/home/nic30/Documents/workspace/sprobe10/fpgalibs/src/"
    files = []
    # files.extend(find_files(workspace, '*.vhd'))
    files.extend(list(find_files(workspace + 'util/', '*.vhd')) 
               + list(find_files(workspace + 'axi/', '*.vhd')))
    
    files = list(map(lambda f : ParserFileInfo(f, "work"), files ))
    #unisimDesFiles = DesignFile.loadFiles(unisimFiles, libName='unisim')
    workDesFiles = DesignFile.loadFiles(files)
    depDict = DesignFile.fileDependencyDict(workDesFiles) # + unisimDesFiles)
    depDict = convertToRelativePaths(workspace, depDict)
    nodes = []
    links = []
    indexes = {}
    indx = 0
    for file in depDict:
        indexes[file] = indx
        indx += 1
        nodes.append({"name": file, 'group': 1})

    for file, connections in depDict.items():
        for c in connections:
            links.append({"source": indexes[file],
                          'target': indexes[c],
                          "value": 1})

    return render_template('hls/dependency.html', nodes=nodes, links=links)