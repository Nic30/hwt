import os

class VivadoConfig():
    VIVADO_HOME = None
    _DEFAULT_VIVADO_DIR_LINUX = '/opt/Xilinx/Vivado/'
    _DEFAULT_VIVADO_EXEC_LINUX = 'vivado.sh'
    @classmethod
    def getHome(cls):
        if cls.VIVADO_HOME is not None:
            return cls.VIVADO_HOME
        try:
            vivadoHomes = os.listdir(VivadoConfig._DEFAULT_VIVADO_DIR_LINUX)
        except Exception:
            raise Exception("Can not find Vivado indtalation automaticaly, set up VivadoConfig.VIVADO_HOME")
        
        if len(vivadoHomes) != 1:
            raise Exception('Can not resolve default Vivado available are %s' % (str(vivadoHomes)))
        
        return os.path.join(cls._DEFAULT_VIVADO_DIR_LINUX, vivadoHomes[0])
    
    @classmethod
    def getExec(cls):
        e = os.path.join(cls.getHome(), cls._DEFAULT_VIVADO_EXEC_LINUX)
        if not os.path.isfile(e):
            raise Exception("Can not found vivado executable %s" % (e))
        return e
    
