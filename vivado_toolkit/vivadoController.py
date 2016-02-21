from subprocess import Popen, PIPE
import multiprocessing
from vhdl_toolkit.types import DIRECTION

# http://www.xilinx.com/support/documentation/sw_manuals/xilinx2013_1/ug975-vivado-quick-reference.pdf

def mkPackageIp(verdor, user, name, version):
    return ':'.join([verdor, user, name, version])

class PartBuilder:
    class Package():
        # all kintex7 packages
        fbv676 = "fbv676"
        fbv484 = "fbv484"
        fbg676 = "fbg676"
        fbg484 = "fbg484"
        ffg676 = "ffg676"
        ffv676 = "ffv676"
        ffg900 = "ffg900"
        ffv900 = "ffv900"
        fgb900 = "fgb900"
        fbg900 = "fbg900"
        ffv901 = "ffv901"
        ffg901 = "ffg901"
        ffv1156 = "ffv1156"
        ffg1156 = "ffg1156"
        rf676 = "rf676"
        rf900 = "rf900"
    class Size():
        _70 = "70"
        _160 = "160"
        _325 = "325"
        _355 = "355"
        _410 = "410"
        _420 = "420"
        _480 = "480"
        # boundary between kintex 7 and virtex 7 
        _585 = "585"
        _2000 = "2000"
        h580 = "h580"
        h870 = "h870"
        x330 = "x330" 
        x415 = "x415"
        x485 = "x485"
        x550 = "x550"
        x680 = "x680"
        x690 = "x690"
        x1140 = "x1140" 
        
    class Family():
        zynq7000 = '7z'
        atrix7 = '7a'
        kintex7 = '7k'
        virtex7 = '7v'
        
    class Speedgrade():
        _1 = "-1"
        _2 = "-2"
        _3 = "-3"
        
    def __init__(self, family, size, package, speedgrade):
        self.family = family
        self.size = size
        self.package = package
        self.speedgrade = speedgrade
        
    def name(self):
        return "xc" + self.family + self.size + self.package + self.speedgrade

class PorType():
    clk = "clk"
    rst = "rst"
    

class VivadoTCL():
    """
    python wraps for Vivado TCL commands
    """
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


    @staticmethod
    def source(scriptPath):
        return "source %s" % (scriptPath)
    
    @staticmethod
    def update_ip_catalog(rebuild=True, scan_changes=True):
        params = []
        if rebuild:
            params.append('-rebuild')
        if scan_changes:
            params.append('-scan_changes')
        return "update_ip_catalog %s" % (' '.join(params))

    class ip_repo_paths():
        @staticmethod
        def add(repoPath): 
            """Multiple add will not cause duplicates"""
            return VivadoTCL.set_property("[current_project]", name="ip_repo_paths", value=repoPath)
        
    @staticmethod    
    def remove_files(files):
        '''remove from project'''  
        return "remove_files %s" % (' '.join(files))
    
    class file():
        # file system manipulator
        @staticmethod
        def delete(files, force=True):
            if force:
                params = '-force'
            else:
                params = "" 
            return "file delete %s %s" % (params, ' '.join(files))
    
    class group():
        @staticmethod
        def start():
            return 'startgroup'
        @staticmethod
        def end():
            return 'endgroup'
    
    
    
    @staticmethod
    def synthetizeBd(dirOfSources, tclFileOfBd):
        cmds = []
        cmds.append(VivadoTCL.cleanOpenOfBd(dirOfSources, tclFile))
        cmds.append(VivadoTCL.run('synth_1'))
        # cmds.append(VivadoTCL.launch_runs('impl_1'))
        return '\n'.join(cmds)
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


# def mkPorts(cmd, names, direction):
#    for name in names:
#        i = VivadoTCL.create_bd_port(name, direction)
#        cmd.append(i)
#
        
# def addConnections(cmd, connections):
#    """
#    @attention: if port name starts with # it is marked as interface
#    @param cmd: is list of tcl comands result will be appended to this list
#    @param connections: dict of connections value can be name of port or list of names  
#    """
#    for k, v in connections.items():
#        def get(pinName):
#            if pinName.startswith('/'):
#                return VivadoTCL.get_bd_pins([pinName])
#            elif pinName.startswith("#/"):
#                # trim #
#                return VivadoTCL.get_bd_intf_pins([pinName[1:]])
#            elif pinName.startswith("#"):
#                raise NotImplementedError("poard intf port")
#            else:
#                return VivadoTCL.get_bd_ports([pinName])
#
#        if not isinstance(v, str):
#            for vi in v:
#                c = VivadoTCL.connect_bd_net(get(k), get(vi))
#                cmd.append(c)
#        else:
#            if k.startswith("#"):
#                c = VivadoTCL.connect_bd_intf_net(get(k), get(v))
#            else:
#                c = VivadoTCL.connect_bd_net(get(k), get(v))
#            cmd.append(c)


class VivadoCtrl():
    def __init__(self, execFile, project):
        self.execFile = execFile
        self.project = project
        self.cmds = []
        self.jobs = multiprocessing.cpu_count()
        
    def run(self, gui=False):
        if gui:
            mode = "gui"
        else:
            mode = 'tcl'
        p = Popen(['bash', self.execFile, "-mode", mode ], stdin=PIPE, stdout=PIPE)
        stdoutdata, stderrdata = p.communicate(input="\n".join(self.cmds).encode(encoding='utf_8'))
        return (stdoutdata, stderrdata)


if __name__ == "__main__":
    # v = VivadoCtrl('/opt/Xilinx/Vivado/2015.2/vivado.sh', '/home/nic30/Documents/vivado/block_ram_test/block_ram_test.xpr')
    # print(v.run())
    dirOfSources = '/home/nic30/Documents/vivado/scriptTest/scriptTest.srcs/sources_1/'
    tclFile = '/home/nic30/Documents/vivado/scriptTest/test_bd1.tcl'
    print(VivadoTCL.synthetizeBd(dirOfSources, tclFile))
