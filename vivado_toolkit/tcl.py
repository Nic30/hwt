from vhdl_toolkit.types import DIRECTION
import multiprocessing

# http://www.xilinx.com/support/documentation/sw_manuals/xilinx2013_1/ug975-vivado-quick-reference.pdf

class VivadoFSOpsTCL():
    @staticmethod
    def ls():
        return 'ls'
    @staticmethod
    def cd(path):
        return 'cd %s' % (path)
    
    @staticmethod
    def pwd():
        return "pwd"
    
    class file():
        # file system manipulator
        @staticmethod
        def delete(files, force=True):
            if force:
                params = '-force'
            else:
                params = "" 
            return "file delete %s %s" % (params, ' '.join(files))


class VivadoBDOpsTCL():
    # [TODO]
    # copy_bd_objs /  [get_bd_cells {c_accum_0}]
    # delete_bd_objs [get_bd_nets c_accum_0_Q] [get_bd_cells c_accum_0]
    
    @staticmethod
    def open_bd_design(fileName):
        return 'open_bd_design {%s}' % fileName
    
    @staticmethod
    def get_bd_ports(names):
        return 'get_bd_ports %s' % (' '.join(names))

    @staticmethod
    def create_bd_port(name, direction, typ=None):
        params = []
        
        if direction == DIRECTION.IN:
            d = "I"
        elif direction == DIRECTION.OUT:
            d = "O"
        else:
            raise Exception()
        params.append("-dir %s" % d)
        
        if typ != None:
            params.append("-type %s" % typ)
        
        return "create_bd_port %s %s" % (' '.join(params), name)
  
    @staticmethod
    def get_bd_intf_pins(names):
        return 'get_bd_intf_pins %s' % (' '.join(names))
    
    @staticmethod
    def get_bd_intf_ports(names):
        raise NotImplemented()
    
    @staticmethod
    def get_bd_pins(names):
        return 'get_bd_pins %s' % (' '.join(names))

    @staticmethod
    def create_bd_design(name):
        return 'create_bd_design "%s"' % name
    
    @staticmethod
    def create_bd_cell(ipId, name):
        return "create_bd_cell -type ip -vlnv %s %s" % (ipId, name)
    
    @staticmethod
    def make_wrapper(bdFile):
        # top has to be at end
        return "make_wrapper -files [get_files %s] -top " % (bdFile)
    
    @staticmethod
    def get_bd_cells(names):
        return "[get_bd_cells %s]" % ' '.join(names)

    @staticmethod
    def connect_bd_net(src, dst):
        # connect_bd_net [get_bd_pins /eth0/txp] [get_bd_ports txp]
        return "connect_bd_net [%s] [%s]" % (src, dst)
    
    @staticmethod
    def connect_bd_intf_net(src, dst):
        # connect_bd_intf_net [get_bd_intf_pins eth3a/m_axis_rx] [get_bd_intf_pins eth3a/s_axis_tx]
        return "connect_bd_intf_net [%s] [%s]" % (src, dst)
    @staticmethod
    def regenerate_bd_layout():
        return "regenerate_bd_layout"

    @staticmethod
    def save_bd_design():
        return "save_bd_design"
    
    @staticmethod
    def write_bd_tcl(tclFileName, force=False):
        """save bd as independent tcl
           bd has to be saved and opened"""
        params = []
        if force:
            params.append('-force')
        return "write_bd_tcl %s %s" % (' '.join(params), tclFileName)

class VivadoProjectOpsTCL():
    @staticmethod
    def add_files(files, norecurse=True):
        params = []
        if norecurse:
            params.append('-norecurse')
        return 'add_files %s %s' % (' '.join(params), ' '.join(files))
    
    @staticmethod
    def update_compile_order(fileSet):    
        return "update_compile_order -fileset %s" % (fileSet)
    
    @staticmethod
    def generate_target(bdFile):
        return 'generate_target all [get_files  %s]' % (bdFile)
    
    class ip_repo_paths():
        @staticmethod
        def add(repoPath): 
            """Multiple add will not cause duplicates"""
            return VivadoTCL.set_property("[current_project]", name="ip_repo_paths", value=repoPath)
        
    @staticmethod    
    def remove_files(files):
        '''remove from project'''  
        return "remove_files %s" % (' '.join(files))
    
    @staticmethod
    def update_ip_catalog(rebuild=True, scan_changes=True):
        params = []
        if rebuild:
            params.append('-rebuild')
        if scan_changes:
            params.append('-scan_changes')
        return "update_ip_catalog %s" % (' '.join(params))

    @staticmethod
    def open_project(filename): 
        return 'open_project %s' % (filename)
    @staticmethod
    def close_project():
        return 'close_project'

    @staticmethod
    def reset_run(name):
        return "reset_run " + name
    
    @staticmethod
    def launch_runs(names, jobs=multiprocessing.cpu_count()):
        return "launch_runs %s -jobs %d" % (' '.join(names), jobs)

    @staticmethod    
    def run(jobName):
        return VivadoTCL.reset_run(jobName) + '\n' + VivadoTCL.launch_runs(jobName)
    
    
class VivadoTCL(VivadoFSOpsTCL, VivadoBDOpsTCL, VivadoProjectOpsTCL):
    """
    python wraps for Vivado TCL commands
    """

    @staticmethod
    def set_property(obj, name=None, value=None, valDict=None, valList=None):
        if valDict != None:
            valueStr = ' '.join(map(lambda kv : "%s {%s}" % (kv[0], str(kv[1])), valDict.items()))
            params = "-dict [list %s]" % valueStr
        elif name != None:
            params = "%s %s" % (name, str(value))
        elif valList != None:
            params = "{%s}" % " ".join(valList)
        else:
            raise Exception()
        
        return "set_property %s %s" % (params, obj)
        

    @staticmethod
    def source(scriptPath):
        return "source %s" % (scriptPath)
    
    
    class group():
        @staticmethod
        def start():
            return 'startgroup'
        @staticmethod
        def end():
            return 'endgroup'
    
    @staticmethod
    def exit():
        return "exit"
    

        
        
        
