
"""
Bernsteins Synthesis Algorithm - database key dependencies
http://www.risc.jku.at/publications/download/risc_2335/2004-02-18-A.pdf  - Lazy Thinking


"""
class HlsOperation():
    """
    @ivar requirements: set of bool signals which has to be true to execute this stage
    """
    def __init__(self, requirements, sigLvlOps, result):
        self.requirements = requirements
        self.sigLvlOps = sigLvlOps
        self.result = result


class FsmNode():
    """
        ______
 lValid>|     |>rValid
        |     |
 lReady<|     |<rReady
        #######

    """
    def __init__(self):
        self.ldata = None
        self.lReady = None
        self.lValid = None
        
        self.rdata = None
        self.rReady = None
        self.rValid = None
        
    def isClkDependent(self):
        raise NotImplementedError()

