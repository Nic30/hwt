"""
Serializer mode specifies if hdl objects derived from parent unit
should be serialized to target HDL or not

use serialize* methods to specify serialization mode for unit class

.. code-block:: python

    @serializeExclude
    class MyHwModule(HwModule):
        # ...
        pass

"""

from collections import namedtuple
from typing import Type

from hwt.doc_markers import internal


@internal
def freeze_dict(data):
    keys = sorted(data.keys())
    if keys:
        frozen_type = namedtuple(''.join(keys), keys)
    else:
        return tuple()
    return frozen_type(**data)


@internal
def hwParamsToValTuple(module: "HwModule"):
    # [TODO] check sub params
    d = {}
    for p in module._hwParams:
        v = p.get_value()
        d[p._name] = v
    return freeze_dict(d)


def serializeExclude(cls: Type["HwModule"]):
    """
    Never serialize HDL objects from this class
    """
    cls._serializeDecision = staticmethod(_serializeExclude_eval)
    return cls


def serializeOnce(cls: Type["HwModule"]):
    """
    Serialize HDL objects only once per class
    """
    cls._serializeDecision = staticmethod(_serializeOnce_eval)
    return cls


def serializeParamsUniq(cls: Type["HwModule"]):
    """
    Decide to serialize only when parameters are unique
    """
    cls._serializeDecision = staticmethod(_serializeParamsUniq_eval)
    return cls


@internal
def _serializeExclude_eval(parentModule: "HwModule", priv):
    """
    Always decide not to serialize obj

    :param priv: private data for this function first unit of this class
    :return: tuple (do serialize this object, next priv, replacement unit)
    """

    # do not use this :class:`hwt.hwModule.HwModule` instance and do not use any replacement
    # (useful when the :class:`hwt.hwModule.HwModule` instance is a placeholder for something
    #  which already exists in hdl word)
    if priv is None:
        priv = parentModule
        return False, priv, None
    else:
        return False, priv, priv


@internal
def _serializeOnce_eval(parentModule: "HwModule", priv):
    """
    Decide to serialize only first obj of it's class

    :param priv: private data for this function
        (first object with class == obj.__class__)

    :return: tuple (do serialize this object, next priv, replacement unit)
        where priv is private data for this function
        (first object with class == obj.__class__)
    """
    if priv is None:
        priv = parentModule
        serialize = True
        replacement = None
        # use this :class:`hwt.hwModule.HwModule` instance and store it for later use
    else:
        # use existing :class:`hwt.hwModule.HwModule` instance
        serialize = False
        replacement = priv

    return serialize, priv, replacement


@internal
def _serializeParamsUniq_eval(parentModule: "HwModule", priv):
    """
    Decide to serialize only objs with unique parameters and class

    :param priv: private data for this function
        ({frozen_params: obj})

    :return: tuple (do serialize this object, next priv, replacement unit)
    """

    params = hwParamsToValTuple(parentModule)

    if priv is None:
        priv = {}

    try:
        prevModule = priv[params]
    except KeyError:
        priv[params] = parentModule
        # serialize new
        return True, priv, None

    # use previous :class:`hwt.hwModule.HwModule` instance with same config
    return False, priv, prevModule
