"""
Serializer mode specifies if hdl objects derived from parent unit
should be serialized to target HDL or not

use serialize* methods to specify serialization mode for unit class

.. code-block:: python

    @serializeExclude
    class MyUnit(Unit):
        # ...
        pass

"""

from collections import namedtuple

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
def paramsToValTuple(unit):
    # [TODO] check sub params
    d = {}
    for p in unit._params:
        v = p.get_value()
        d[p._name] = v
    return freeze_dict(d)


def serializeExclude(cls):
    """
    Never serialize HDL objects from this class
    """
    cls._serializeDecision = staticmethod(_serializeExclude_eval)
    return cls


def serializeOnce(cls):
    """
    Serialize HDL objects only once per class
    """
    cls._serializeDecision = staticmethod(_serializeOnce_eval)
    return cls


def serializeParamsUniq(cls):
    """
    Decide to serialize only when parameters are unique
    """
    cls._serializeDecision = staticmethod(_serializeParamsUniq_eval)
    return cls


@internal
def _serializeExclude_eval(parentUnit, priv):
    """
    Always decide not to serialize obj

    :param priv: private data for this function first unit of this class
    :return: tuple (do serialize this object, next priv, replacement unit)
    """

    # do not use this :class:`hwt.synthesizer.unit.Unit` instance and do not use any prelacement
    # (useful when the :class:`hwt.synthesizer.unit.Unit` instance is a placeholder for something
    #  which already exists in hdl word)
    if priv is None:
        priv = parentUnit
        return False, priv, None
    else:
        return False, priv, priv


@internal
def _serializeOnce_eval(parentUnit, priv):
    """
    Decide to serialize only first obj of it's class

    :param priv: private data for this function
        (first object with class == obj.__class__)

    :return: tuple (do serialize this object, next priv, replacement unit)
        where priv is private data for this function
        (first object with class == obj.__class__)
    """
    if priv is None:
        priv = parentUnit
        serialize = True
        replacement = None
        # use this :class:`hwt.synthesizer.unit.Unit` instance and store it for later use
    else:
        # use existing :class:`hwt.synthesizer.unit.Unit` instance
        serialize = False
        replacement = priv

    return serialize, priv, replacement


@internal
def _serializeParamsUniq_eval(parentUnit, priv):
    """
    Decide to serialize only objs with uniq parameters and class

    :param priv: private data for this function
        ({frozen_params: obj})

    :return: tuple (do serialize this object, next priv, replacement unit)
    """

    params = paramsToValTuple(parentUnit)

    if priv is None:
        priv = {}

    try:
        prevUnit = priv[params]
    except KeyError:
        priv[params] = parentUnit
        # serialize new
        return True, priv, None

    # use previous :class:`hwt.synthesizer.unit.Unit` instance with same config
    return False, priv, prevUnit
