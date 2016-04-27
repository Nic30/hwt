

#'/opt/Xilinx/Vivado/2015.2/vivado.sh'
class VivadoConfig():
    VIVADO_HOME = None
    
    @classmethod
    def getHome(cls):
        if cls.VIVADO_HOME is not None:
            return cls.VIVADO_HOME
        
        raise NotImplementedError()
    
    @classmethod
    def getExec(cls):
        raise NotImplementedError()