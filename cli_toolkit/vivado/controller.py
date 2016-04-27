import pexpect, os
from cli_toolkit.vivado.cmdResult import VivadoCmdResult
from cli_toolkit.vivado.tcl import VivadoTCL
from cli_toolkit.vivado.config import VivadoConfig

def mkPackageIp(verdor, user, name, version):
    return ':'.join([verdor, user, name, version])


    
class VivadoCntrl():
    def __init__(self, execFile=VivadoConfig.getExec(), deleteLogsOnExit=True, timeout=6 * 60 * 60, logComunication=False):
        self.execFile = execFile
        self.proc = None
        self.jurnalFile = "vivado.jou"
        self.logFile = 'vivado.log'
        self.verbose = True
        self.timeout = timeout
        self.guiOpened = False
        self.logComunication = logComunication
        self.encoding = 'ASCII'
        
    def __enter__(self):
        cmd = ["-mode", 'tcl' , "-notrace"]
        if self.verbose:
            cmd.append('-verbose')
        self.proc = pexpect.spawn(self.execFile, cmd)
        self.firstCmd = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        p = self.proc
        if p.isalive():
            p.sendline(VivadoTCL.exit())
            p.expect("exit", timeout=self.timeout)  # block while cmd ends
        if p.isalive():
            p.terminate()
            
    def openGui(self):
        """
        @attention: this method disconnects controller and opens gui
        """    
        list(self.process([VivadoTCL.start_gui()]))  # list to execute because process() is  generator
        if self.proc.isalive():
            self.proc.wait()
    
    
    def _process(self, cmds):
        p = self.proc
        for cmd in cmds:
            if self.firstCmd:
                p.expect("Vivado%", timeout=self.timeout)  # block while command line init
                self.firstCmd = False
            if self.guiOpened:
                raise Exception("Controller have no acces to Vivado because gui is opened")
            
            p.sendline(cmd)
            # @attention: there is timing issue in reading from tty next command returns corrupted line 
            p.readline()  # read cmd from tty
            # p.expect(cmd, timeout=self.timeout)  
            if cmd == VivadoTCL.start_gui():
                self.guiOpened = True
            try:
                p.expect("Vivado%", timeout=self.timeout)  # block while cmd ends
            except pexpect.EOF:
                pass
            t = p.before.decode(self.encoding)
            if self.logComunication:
                print(cmd)
                print(t)
            res = VivadoCmdResult.fromStdoutStr(cmd, t)
            res.raiseOnErrors()
            yield res
    def process(self, cmds, iterator=False):
        """
        @attention: if iterator == True you must iterate trough it to execute commands, 
                    this is how python generator works
        @param iterator: return iterator over cmd results 
        """
        results = self._process(cmds)
        if iterator:
            return results
        else:
            return list(results)
    def rmLogs(self):
        if os.path.exists(self.logFile):
            os.remove(self.logFile)
        if os.path.exists(self.jurnalFile):
            os.remove(self.jurnalFile)   
            
if __name__ == "__main__":
    from cli_toolkit.tests.config import defaultVivadoExc
    import os
    with VivadoCntrl(defaultVivadoExc) as v: 
        _op, _pwd, _dir = v.process(['open_project /home/nic30/Documents/vivado/Sprobe10_board_test/Sprobe10_board_test.xpr', 'pwd', 'dir'])
        print(_op.resultText)
        ls = os.listdir(_pwd.resultText)
        vivadoLs = _dir.resultText.split()
        ls.sort()
        vivadoLs.sort()
        print(ls)
        print(vivadoLs)
        v.openGui()
    print('finished')
