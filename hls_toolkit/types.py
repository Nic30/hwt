# from vhdl_toolkit.types import PortItem
# from hls_toolkit.errors import InvalidAsign
from myhdl import Signal, intbv, always_comb
"""
name and direction atributes are asigned by HLS core

"""

class InterfaceType():
    """Template class for interfaces"""
    def _getSignals(self):
        """ This method is called when constructing interfaces signals
        @return:  list of signals which interface uses"""
        pass

class BitVector(InterfaceType):
    """
    alias std_logic_vector
    """
    def __init__(self, width):
        self.width = width
    def _getSignals(self):
        return Signal(intbv(0)[self.width:])
    # def _asignFrom(self, interface, hls_syn):
    #    if type(self) == type(interface):
    #        return "%s <= %s" % (self.name, interface.name)
    #    else:
    #        e = InvalidAsign()
    #        e.info = "%s <= %s" % (self.name, interface.name)
    #        raise e
    # def asPortItems(self):
    #    return [PortItem(self.name, self.direction, "STD_LOGIC_VECTOR(0 downto %d)" % (self.width - 1))]

class BitSingle(InterfaceType):
    """
    alias std_logic
    """
    def _getSignals(self):
        return Signal(bool(0))
    # def asPortItems(self):
    #    return [PortItem(self.name, self.direction, "STD_LOGIC")]



class Handshake(InterfaceType):
    def __init__(self, dataObj):
        # self.__dict__.update(dataObj.__dict__)
        self.d = dataObj
        self.ready = Signal(bool(0))
        self.valid = Signal(bool(0))
    
    def _getSignals(self):
        return self
    

    def canRead(self):
        @always_comb
        def canReadFn():
            if self.valid:
                return True
            else: 
                return False
        return canReadFn
        

    def canWrite(self):
        @always_comb
        def canWriteFn():
            if self.ready:
                return True
            else: 
                return False
        return canWriteFn

    def read(self, dataOut, _call):
        @always_comb
        def readFn():
            if _call:
                dataOut.next = self.d
                self.ready.next = True
            else:
                self.ready.next = False
        return readFn
    
    def write(self, dataIn, _call):
        @always_comb
        def writeFn():
            if _call:
                self.d.next = dataIn
                self.valid.next = True
            else:
                self.valid.next = False

class AxiStream(Handshake):
    pass
