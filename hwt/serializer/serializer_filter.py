from hwt.synthesizer.unit import Unit
from hwt.serializer.mode import _serializeExclude_eval
from typing import Optional, Tuple


class SerializerFilter(object):
    """
    Base class for filters used to exclude some Unit instances from
    target HDL (in order to prevent code duplication, archetype colisions etc.)

    This base implementation keeps track about others objects and calls
    _serializeDecision on the Unit instance to decide if instance should be excluded.
    """
    def __init__(self):
        self.serializedClasses = {}  # type: Type[Unit]: Unit
        # (unitCls, paramsValues) : unitObj
        # where paramsValues are dict name:value
        self.serializedConfiguredUnits = {}

    def do_serialize(self, unit: Unit) -> Tuple[bool, Optional[Unit]]:
        """
        Decide if this unit should be serialized or not eventually fix name
        to fit same already serialized unit

        :param obj: object to serialize
        :param serializedClasses: dict {unitCls : unitobj}
        :param serializedConfiguredUnits: (unitCls, paramsValues) : unitObj
            where paramsValues are named tuple name:value
        """
        assert isinstance(unit, Unit)
        sd = unit._serializeDecision
        if sd is None:
            # the Unit instance does not have any filter function
            return True, None
        else:
            # use UnitInstance filer function
            prevPriv = self.serializedClasses.get(unit.__class__, None)
            do_serialize, nextPriv, replacement = sd(unit, prevPriv)
            self.serializedClasses[unit.__class__] = nextPriv
            return do_serialize, replacement


class SerializerFilterAll(SerializerFilter):
    """
    Ignore any serialization constraints and dump everything
    """
    def do_serialize(self, unit: Unit) -> bool:
        return True, None


class SerializerFilterDoNotExclude(SerializerFilter):
    """
    Use all serialization specifications except @serializeExclude
    Usefull when it is requred to dump all components for sim etc.
    """
    def do_serialize(self, unit: Unit) -> bool:
        orig = unit._serializeDecision
        if orig is _serializeExclude_eval:
            unit._serializeDecision = None
        try:
            return super(SerializerFilterDoNotExclude, self).do_serialize(unit)
        finally:
            unit._serializeDecision = orig
