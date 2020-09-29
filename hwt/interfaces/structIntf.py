from typing import Tuple, Union

from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.struct import HStruct
from hwt.interfaces.agents.structIntf import StructIntfAgent
from hwt.synthesizer.interface import Interface
from pycocotb.hdlSimulator import HdlSimulator
from hwt.synthesizer.typePath import TypePath


class StructIntf(Interface):
    """
    Create dynamic interface based on HStruct or HUnion description

    :ivar ~._fieldsToInterfaces: dictionary {field_path: sub interface for it}
        field path is a tuple of HStructFields which leads to this interface
    :ivar ~._structT: HStruct instance used as template for this interface
    :param _instantiateFieldFn: function(FieldTemplateItem instance)
        return interface instance
    :attention: _instantiateFieldFn should also share _fieldsToInterfaces
        with all other instances of StructIntf on this interface
    """

    def __init__(self, structT: HStruct,
                 field_path: TypePath,
                 instantiateFieldFn,
                 masterDir=DIRECTION.OUT,
                 loadConfig=True):
        Interface.__init__(self,
                           masterDir=masterDir,
                           loadConfig=loadConfig)
        if not field_path:
            field_path = TypePath()
        else:
            assert isinstance(field_path, TypePath), field_path
        self._field_path = field_path
        self._structT = structT
        self._instantiateFieldFn = instantiateFieldFn
        self._fieldsToInterfaces = {}

    def _declr(self):
        _t = self._structT
        if isinstance(_t, HStruct):
            fields = _t.fields
        else:
            fields = _t.fields.values()

        self._fieldsToInterfaces[self._field_path] = self

        for field in fields:
            # skip padding
            if field.name is not None:
                # generate interface based on struct field
                intf = self._instantiateFieldFn(self, field)
                p = self._field_path / field.name
                assert p not in self._fieldsToInterfaces, p
                self._fieldsToInterfaces[p] = intf

                setattr(self, field.name, intf)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = StructIntfAgent(sim, self)

