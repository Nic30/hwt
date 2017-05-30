from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.types.struct import HStruct

class StructIntf(Interface):
    """
    Create dynamic interface based on HStruct description
    """
    def __init__(self, structT, instantiateFieldFn, masterDir=DIRECTION.OUT, multipliedBy=None, loadConfig=True):
        """
        :param structT: HStruct instance used as template for this interface
        :param instantiateFieldFn: function(FieldTemplateItem instance) used to instantiate fields
            (is called only on fields which have different type than HStruct)
        """
        Interface.__init__(self, masterDir=masterDir, multipliedBy=multipliedBy, loadConfig=loadConfig)
        self._structT = structT
        self._instantiateFieldFn = instantiateFieldFn
    
    def _declr(self):
        for field in self._structT.fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                t = field.dtype
                if isinstance(t, HStruct):
                    intf = StructIntf(t, self._instantiateFieldFn)
                else:
                    intf = self._instantiateFieldFn(field)
                
                setattr(self, field.name, intf)