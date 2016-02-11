import os

from hls_toolkit.astTweaker import hlsPreprocess
from hls_toolkit.errors import MissingConfAttribErr
from hls_toolkit.helpers import Chdir


class HLSparser(object):
    """
    main parser - converts hls_toolkit code to vhdl or verilog
    """
    def __init__(self, comp, conf):
        """
        @param comp: function of component to parse
        @param conf: configuration for this comp function 
        """
        self.comp = comp
        self.conf = conf
        
    def constructInterface(self):
        """ builds interface signals from config """
        intfConf = self.conf["interfaces"]
        interfaces = {}
        try:
            for intf in  self.comp.__code__.co_varnames[:self.comp.__code__.co_argcount]:
                interfaces[intf] = intfConf[intf]._getSignals()
        except KeyError as e:
            MissingConfAttribErr._raiseFromFn("Missing configuration for interface: %s" % e.args, self.comp)
        return interfaces
            
    def convert(self, toFn):
        """
        @param toFn:  toVHDL or toVerilog functions from myhdl 
        """
        interfaces = self.constructInterface()
        origFileName = self.comp.__code__.co_filename
        with Chdir(os.path.dirname(origFileName)):
            preprModul = hlsPreprocess(self.comp, self.conf, interfaces)
            preprComp = getattr(preprModul, self.comp.__code__.co_name)
            toFn(preprComp, **interfaces)
