
"""
Abstract tree tweaker module
"""

import os

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
