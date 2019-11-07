from collections import namedtuple

from hwt.doc_markers import internal


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


@internal
def freeze_dict(data):
    keys = sorted(data.keys())
    frozen_type = namedtuple(''.join(keys), keys)
    return frozen_type(**data)


@internal
def paramsToValTuple(unit):
    # [TODO] check sub params
    d = {}
    for p in unit._params:
        v = p.get_value()
        d[p._name] = v
    return freeze_dict(d)


@internal
def prepareEntity(ent, name, templateUnit):
    ent.name = name
    ent.generics.sort(key=lambda x: x.hdl_name)
    ent.ports.sort(key=lambda x: x.name)
    # copy names
    if templateUnit is not None:
        # sort in python is stable, ports and generic were added in same order
        # templateUnit should have generic and ports sorted
        for gp, gch in zip(templateUnit._entity.generics, ent.generics):
            gch.hdl_name = gp.hdl_name
        for pp, pch in zip(templateUnit._entity.ports, ent.ports):
            pch.name = pp.name


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
def _serializeExclude_eval(parentUnit, obj, isDeclaration, priv):
    """
    Always decide not to serialize obj

    :param priv: private data for this function first unit of this class
    :return: tuple (do serialize this object, next priv)
    """
    if isDeclaration:
        # prepare entity which will not be serialized
        prepareEntity(obj, parentUnit.__class__.__name__, priv)

    if priv is None:
        priv = parentUnit

    return False, priv


@internal
def _serializeOnce_eval(parentUnit, obj, isDeclaration, priv):
    """
    Decide to serialize only first obj of it's class

    :param priv: private data for this function
        (first object with class == obj.__class__)

    :return: tuple (do serialize this object, next priv)
        where priv is private data for this function
        (first object with class == obj.__class__)
    """
    clsName = parentUnit.__class__.__name__

    if isDeclaration:
        obj.name = clsName

    if priv is None:
        priv = parentUnit
    elif isDeclaration:
        # prepare entity which will not be serialized
        prepareEntity(obj, clsName, parentUnit)

    serialize = priv is parentUnit

    return serialize, priv


@internal
def _serializeParamsUniq_eval(parentUnit, obj, isDeclaration, priv):
    """
    Decide to serialize only objs with uniq parameters and class

    :param priv: private data for this function
        ({frozen_params: obj})

    :return: tuple (do serialize this object, next priv)
    """

    params = paramsToValTuple(parentUnit)

    if priv is None:
        priv = {}

    if isDeclaration:
        try:
            prevUnit = priv[params]
        except KeyError:
            priv[params] = parentUnit
            return True, priv

        prepareEntity(obj, prevUnit._entity.name, prevUnit)
        return False, priv

    return priv[params] is parentUnit, priv
