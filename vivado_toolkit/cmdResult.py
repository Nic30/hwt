import re

class VivadoErr(Exception):
    def __init__(self, cmdResult):
        super(VivadoErr, self).__init__()
        self.cmdResult = cmdResult
    def __str__(self):
        return 'Cmd "%s" caused errors:\n%s' % (self.cmdResult.cmd, str(self.cmdResult.errors))

class VivadoCmdResult():
    regex_invalidCmd = re.compile("(invalid command name \".*\")")
    regex_err = re.compile("ERROR: (.*)")
    regex_critWarn = re.compile('CRITICAL WARNING: (.*)')
    regex_warn = re.compile("WARNING: (.*)")
    regex_info = re.compile('INFO: (.*)')
        
    def __init__(self, cmd, resultText, errors, criticalWarnings, warnings, infos):
        self.cmd = cmd
        self.resultText = resultText
        self.errors = errors
        self.criticalWarnings = criticalWarnings
        self.warnings = warnings
        self.infos = infos
        
    @staticmethod
    def extractMsgs(msg, regex, listOfMsgs):
        for m in regex.finditer(msg):
            listOfMsgs.append(m.group(1).strip())
        return regex.sub("", msg)
    
    @classmethod
    def fromStdoutStr(cls, cmd, text):
        resultText = text
        errors = []
        criticalWarnings = []
        warnings = []
        infos = []
        
        resultText = VivadoCmdResult.extractMsgs(resultText, VivadoCmdResult.regex_invalidCmd, errors)
        resultText = VivadoCmdResult.extractMsgs(resultText, VivadoCmdResult.regex_err, errors)
        resultText = VivadoCmdResult.extractMsgs(resultText, VivadoCmdResult.regex_critWarn, criticalWarnings)
        resultText = VivadoCmdResult.extractMsgs(resultText, VivadoCmdResult.regex_warn, warnings)
        resultText = VivadoCmdResult.extractMsgs(resultText, VivadoCmdResult.regex_info, infos)
        
        return cls(cmd, resultText.strip(), errors, criticalWarnings, warnings, infos)
    def raiseOnErrors(self):
        if self.errors:
            raise VivadoErr(self)    
