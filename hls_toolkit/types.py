# from hwt.hdlObjects.types import PortItem
# from hls_toolkit.errors import InvalidAsign
"""
name and direction atributes are asigned by HLS core

"""


class InterfaceType():
    """Template class for interfaces"""
    def _getSignals(self):
        """ This method is called when constructing interfaces signals
        @return:  list of signals which interface uses"""
        raise NotImplementedError()

class Handshake(InterfaceType):
    def __init__(self, interface):
        self.interface = interface
        self.ready = interface.ready
        self.valid = interface.valid
    
    def _getSignals(self):
        return self
    

    def canRead(self):
        def canReadFn():
            if self.valid:
                return True
            else: 
                return False
        return canReadFn
        

    def canWrite(self):
        def canWriteFn():
            return self.ready
        return canWriteFn

    def read(self, dataOut, _call):
        def readFn():
            if _call:
                dataOut.next = self.d
                self.ready.next = True
            else:
                self.ready.next = False
        return readFn
    
    def write(self, dataIn, _call):
        def writeFn():
            if _call:
                self.d.next = dataIn
                self.valid.next = True
            else:
                self.valid.next = False