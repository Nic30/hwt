
class HdlSimConfig():
    """
    Container of configuration of hdl simulator
    """
        
    def beforeSim(self, simulator, signals):
        """
        called beforee preparing of simulation
        """
        pass
    
    def logChange(self, nowTime, sig, nextVal):
        """
        Log change of value for signal
        """
        pass
        
    def logPropagation(self, x):
        """
        Log value propagation over netlist
        """
        pass

    def logApplyingValues(self, simulator, values):
        """
        Log simulator value quantum applied
        """
        pass