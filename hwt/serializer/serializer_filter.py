from typing import Optional, Tuple

from hwt.serializer.mode import _serializeExclude_eval
from hwt.hwModule import HwModule


class SerializerFilter(object):
    """
    Base class for filters used to exclude some :class:`hwt.hwModule.HwModule` instances from
    target HDL (in order to prevent code duplication, archetype colisions etc.)

    This base implementation keeps track about others objects and calls
    _serializeDecision on the :class:`hwt.hwModule.HwModule` instance to decide if instance should be excluded.

    :ivar serializedClasses: dict {moduleCls : moduleObj}
    :ivar serializedConfiguredHwModules: (moduleCls, paramsValues) : moduleObj
            where paramsValues are named tuple name:value
    """
    def __init__(self):
        self.serializedClasses = {}  # type: Type[HwModule]: HwModule
        # (hwModuleCls, paramsValues) : unitObj
        # where paramsValues are dict name:value
        self.serializedConfiguredHwModules = {}

    def do_serialize(self, module: HwModule) -> Tuple[bool, Optional[HwModule]]:
        """
        Decide if this module should be serialized or not eventually fix name
        to fit same already serialized module

        :param module: object to serialize
        """
        assert isinstance(module, HwModule)
        sd = module._serializeDecision
        if sd is None:
            # the :class:`hwt.hwModule.HwModule` instance does not have any filter function
            return True, None
        else:
            # use HwModuleInstance filer function
            prevPriv = self.serializedClasses.get(module.__class__, None)
            do_serialize, nextPriv, replacement = sd(module, prevPriv)
            self.serializedClasses[module.__class__] = nextPriv
            return do_serialize, replacement


class SerializerFilterAll(SerializerFilter):
    """
    Ignore any serialization constraints and dump everything
    """
    def do_serialize(self, module: HwModule) -> bool:
        return True, None


class SerializerFilterDoNotExclude(SerializerFilter):
    """
    Use all serialization specifications except @serializeExclude
    Useful when it is required to dump all components for sim etc.
    """
    def do_serialize(self, module: HwModule) -> bool:
        orig = module._serializeDecision
        if orig is _serializeExclude_eval:
            module._serializeDecision = None
        try:
            return super(SerializerFilterDoNotExclude, self).do_serialize(module)
        finally:
            module._serializeDecision = orig
