from subprocess import Popen, PIPE
import multiprocessing
from os import path

   

# http://www.xilinx.com/support/documentation/sw_manuals/xilinx2013_1/ug975-vivado-quick-reference.pdf

def mkPackageIp(verdor, user, name, version):
    return ':'.join([verdor, user, name, version])
    

class VivadoTCL():
    # copy_bd_objs /  [get_bd_cells {c_accum_0}]
    # connect_bd_net [get_bd_pins c_accum_0/Q] [get_bd_pins c_accum_1/B]
    # delete_bd_objs [get_bd_nets c_accum_0_Q] [get_bd_cells c_accum_0]
    
    @staticmethod
    def open_bd_design(fileName):
        return 'open_bd_design {%s}' % fileName
    
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
            return "set_property  ip_repo_paths %s [current_project]" % (repoPath)
        
        
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
        def startgroup():
            return 'startgroup'
        @staticmethod
        def endgroup():
            return 'endgroup'
    
    @staticmethod
    def launch_runs(jobName):
        return "launch_runs %s -jobs %s" % (jobName, multiprocessing.cpu_count()) 
    
    @staticmethod
    def reset_run(jobName):
        return 'reset_run %s' % jobName
    
    @staticmethod    
    def run(jobName):
        return VivadoTCL.reset_run(jobName) + '\n' + VivadoTCL.launch_runs(jobName)
    
    @staticmethod
    def cleanOpenOfBd(dirOfSources, tclFile):
        """
        @param dirOfSources: : src directory in vivado project 
        @attention: bd is always primary source of information, if exists new tcl is generated from it
           this is """
        cmds = []
        boardName = path.splitext(path.basename(tclFile))[0]
        boardDirName = path.join(dirOfSources, 'bd', boardName)
        boardFileName = path.join(boardDirName, boardName + '.bd')
        
        # update tcl from bd
        if path.exists(boardFileName):
            cmds.append(VivadoTCL.open_bd_design(boardFileName))
            cmds.append(VivadoTCL.write_bd_tcl(tclFile, force=True))

        # tcl file does not contains revisions of ips
        cmds.append(VivadoTCL.update_ip_catalog(tclFile))
       
        # remove old bd
        cmds.append(VivadoTCL.remove_files([boardFileName]))
        cmds.append(VivadoTCL.file.delete([boardDirName]))
        bdWrapper = path.join(boardDirName, 'hdl', boardName + "_wrapper.vhd")
        cmds.append(VivadoTCL.remove_files([bdWrapper]))
        cmds.append(VivadoTCL.file.delete([bdWrapper]))
        
        
        # import new from tcl
        cmds.append(VivadoTCL.source(tclFile))
        
        # generate wrapper and set is as top
        cmds.append(VivadoTCL.make_wrapper(boardFileName))
        cmds.append(VivadoTCL.add_files([bdWrapper]))
        cmds.append(VivadoTCL.update_compile_order('sources_1'))  # [TODO]
        cmds.append(VivadoTCL.update_compile_order('sim_1'))  # [TODO]
        
        return '\n'.join(cmds)
    @staticmethod
    def synthetizeBd(dirOfSources, tclFileOfBd):
        cmds = []
        cmds.append(VivadoTCL.cleanOpenOfBd(dirOfSources, tclFile))
        cmds.append(VivadoTCL.run('synth_1'))
        # cmds.append(VivadoTCL.launch_runs('impl_1'))
        return '\n'.join(cmds)
    
class VivadoCtrl():
    def __init__(self, execFile, project):
        self.execFile = execFile
        self.project = project
        self.cmds = []
        self.cmds.append('open_project %s' % (project))
        self.jobs = multiprocessing.cpu_count()
    
    def updateIps(self, ips):
        self.cmds.append(VivadoTCL.update_ip_catalog())
        self.cmds.append('report_ip_status -name ip_status')
        self.cmds.append("upgrade_ip [get_ips  {%s}]" % (" ".join(ips)))
    
    def runSymth(self, name):
        self.cmds.append("reset_run " + name)
        self.cmds.append("launch_runs %s -jobs %d" % (name, self.jobs))
    
    def runImpl(self, name):
        self.cmds.append('launch_runs %s -jobs %d' % (name, self.jobs))
   
    def genBitstream(self, implName):
        self.cmds.append('launch_runs %s -to_step write_bitstream -jobs %d' % (implName, self.jobs))
        
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

