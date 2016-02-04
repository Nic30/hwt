from subprocess import Popen, PIPE
import multiprocessing


# http://www.xilinx.com/support/documentation/sw_manuals/xilinx2013_1/ug975-vivado-quick-reference.pdf

class VivadoCtrl():
    def __init__(self, execFile, project):
        self.execFile = execFile
        self.project = project
        self.cmds = []
        self.cmds.append('open_project %s' % (project))
        self.jobs = multiprocessing.cpu_count()
    
    def updateIps(self, ips):
        self.cmds.append("update_ip_catalog -rebuild -scan_changes")
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
    v = VivadoCtrl('/opt/Xilinx/Vivado/2015.2/vivado.sh', '/home/nic30/Documents/vivado/block_ram_test/block_ram_test.xpr')
    print(v.run())