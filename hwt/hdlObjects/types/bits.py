from copy import copy

from hwt.hdlObjects.constants import Unconstrained
from hwt.hdlObjects.types.hdlType import HdlType 
from hwt.bitmask import mask


class Bits(HdlType):
    
    def __init__(self, widthConstr=None, forceVector=False, signed=None):
        """
        @param forceVector: use always hdl vector type 
            (for example std_logic_vector(0 downto 0) instead of std_logic)
        """
        super().__init__()
        self.forceVector = forceVector
        self.signed = signed
        if widthConstr is None:
            self.constrain = Unconstrained()
        else:
            self.constrain = widthConstr
    
    def __eq__(self, other):
        return isinstance(other, Bits) and other.bit_length() == self.bit_length()\
            and self.signed == other.signed and self.forceVector == other.forceVector
    
    def __hash__(self):
        return hash((self.signed, id(self.constrain), self.forceVector))
    
    def applySpecificator(self, const):
        assert isinstance(self.constrain, Unconstrained)
        s = copy(self)
        s.constrain = const
        return s
    
    def all_mask(self):
        return mask(self.bit_length())
    
    def bit_length(self):
        if isinstance(self.constrain, (int, float)):
            return int(self.constrain)
        elif isinstance(self.constrain, Unconstrained):
            try:
                return self.constrain.derivedWidth
            except AttributeError:
                return None
        else:
            w = self.constrain.staticEval()
            return abs(w.val[0].val - w.val[1].val) + 1 

    
    
    @classmethod
    def getConvertor(cls):
        from hwt.hdlObjects.types.bitsConversions import convertBits
        return convertBits
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.bitsVal import BitsVal 
            cls._valCls = BitsVal
            return cls._valCls

    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        c = self.constrain
        if isinstance(c, int):
            constr = "width:%d" % c
        elif isinstance(c, Unconstrained):
            try:
                constr = "derivedWidth:%d" % (c.derivedWidth)
            except AttributeError:
                constr = ""
        else:
            constr = VhdlSerializer.asHdl(self.constrain, onlyPrintDefaultValues)
        
        return "<HdlType %s, %s>" % (
            self.__class__.__name__, constr)

