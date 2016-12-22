import os
from flask.blueprints import Blueprint
from hwt.pyUtils.fileHelpers import find_files
from flask import render_template

# [TODO] move gui out of hwt

dependenciesBp = Blueprint('dependencies', __name__, template_folder='templates/dependencies/')

def rel(root, f):
    """
    convert to relative path
    """
    return os.path.relpath(f, root)


# http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
@dependenciesBp.route('/dependencies/')
def dependencyGraph():
    # unisimFiles = ['/opt/Xilinx/Vivado/2015.2/data/vhdl/src/unisims/retarget_VCOMP.vhd']
    workspace = "/home/nic30/Documents/workspace/sprobe10/fpgalibs/src/hfer/"
    # workspace = "/home/nic30/Documents/workspace/sprobe10/fpgalibs/src/"
    # workspace = "../../hwtLib/hwtLib/samples/vhdlCodesign/vhdl/dependencies0"
    r = lambda df: rel(workspace, df.fileInfo.fileName) 
    files = []
    files.extend(find_files(workspace, '*.vhd'))
    # files.extend(list(find_files(workspace + 'util/', '*.vhd')) 
    #           + list(find_files(workspace + 'axi/', '*.vhd')))
    #
    files = list(map(lambda f : ParserFileInfo(f, "work"), files))
    # unisimDesFiles = DesignFile.loadFiles(unisimFiles, libName='unisim')
    desFiles = DesignFile.loadFiles(files, debug=True)
    DesignFile.resolveDependencies(desFiles)  # + unisimDesFiles)
    
    nodes = []
    links = []
    indexes = {}
    indx = 0
    for file in desFiles:
        indexes[file] = indx
        indx += 1
        nodes.append({"name": r(file), 'group': 1})

    for df in desFiles:
        for defi in df.depOnDefinitions:
            links.append({"source": indexes[defi],
                          'target': indexes[df],
                          "value": 1})
        for decl in df.depOnDeclarations:
            links.append({'target': indexes[decl],
                          "source": indexes[df],
                          "value": 1})

    return render_template('dependency.html', nodes=nodes, links=links)
