
from hls_toolkit.types import BitSingle, BitVector, Handshake, AxiStream



class HLSSyntetizatorConfig(object):
    '''
    Config class for hls syntetizator
    '''
    class interfaces(object):
        class direct(object):
            BitSingle =BitSingle
            BitVector =BitVector
        class handshake(object):
            Handshake = Handshake
            AxiStream = AxiStream
        