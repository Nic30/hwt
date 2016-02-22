import pexpect
from vivado_toolkit.cmdResult import VivadoCmdResult
from vivado_toolkit.tcl import VivadoTCL

def mkPackageIp(verdor, user, name, version):
    return ':'.join([verdor, user, name, version])

class PorType():
    clk = "clk"
    rst = "rst"
    
class VivadoCntrl():
    def __init__(self, execFile, deleteLogsOnExit=True):
        self.execFile = execFile
        self.proc = None
        self.jurnalFile = "vivado.jou"
        self.logFile = 'vivado.log'
        self.verbose = True
        self.timeout = 6 * 60 * 60
    
    def __enter__(self, gui=False):
        if gui:
            mode = "gui"
        else:
            mode = 'tcl'
        cmd = ["-mode", mode , "-notrace"]
        if self.verbose:
            cmd.append('-verbose')
        self.proc = pexpect.spawn(self.execFile, cmd)
        self.firstCmd = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        p = self.proc
        p.sendline(VivadoTCL.exit())
        p.expect("exit", timeout=self.timeout)  # block while cmd ends
        p.terminate()
        
        
    def process(self, cmds):
        p = self.proc
        for cmd in cmds:
            if self.firstCmd:
                p.expect("Vivado%", timeout=self.timeout)  # block while command line init
                self.firstCmd = False
            p.sendline(cmd)
            p.expect(cmd, timeout=self.timeout)  # read cmd by Vivado
            p.expect("Vivado%", timeout=self.timeout)  # block while cmd ends
            t = p.before.decode()
           
            res = VivadoCmdResult.fromStdoutStr(cmd, t)
            res.raiseOnErrors()
            yield res

       
if __name__ == "__main__":
    from vivado_toolkit.tests.config import defaultVivadoExc
    import os
    with VivadoCntrl(defaultVivadoExc) as v: 
        _pwd, _dir = v.process(['pwd', 'dir'])
        ls = os.listdir(_pwd.resultText)
        vivadoLs = _dir.resultText.split()
        ls.sort()
        vivadoLs.sort()
        print(ls)
        print(vivadoLs)
       
    print('finished')
