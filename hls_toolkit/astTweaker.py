
"""
Abstract tree tweaker module
"""

import ast, os

from hls_toolkit.shotcuts.ast import addSignal, fnFileAst, nodeOfFn, dump
from hls_toolkit.unparse import Unparser
import myhdl


def import_file(full_path_to_module):
    """
    imports module by name
    @return: imported module
    """
    try:
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
        save_cwd = os.getcwd()
        if len(module_dir) > 0:
            os.chdir(module_dir)
        module_obj = __import__(module_name)
        module_obj.__file__ = full_path_to_module
        globals()[module_name] = module_obj
        os.chdir(save_cwd)
    except:
        raise ImportError
    moduleName = os.path.splitext(full_path_to_module)[0]
    module = globals()[moduleName]
    return module

def hlsPreprocess(compFn, conf, interfaces):
    """ 
    transforms hls syntax to basic myhdl
    @return: preprocessed modul 
    """
    tree = fnFileAst(compFn)
    node = nodeOfFn(tree, compFn)
    # print(dump(tree))
    addSignal(node, "sigX", bool)
    addSignal(node, "sigX", myhdl.intbv(0)[10:])
    outFileName = "__" + compFn.__code__.co_name + ".py"
    with open(outFileName, "w") as f:
        Unparser(tree, file=f)

    # with open(outFileName) as f:
    #    print(f.read())
    preprModul = import_file(outFileName)
    return preprModul

# if __name__ == "__main__":
#    hlsPreprocess(compFn, compFn_conf)
