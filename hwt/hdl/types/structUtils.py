from copy import copy
from typing import Union, Dict, Sequence

from hwt.hdl.const import HConst
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.stream import HStream
from hwt.hdl.types.struct import HStructField, HStruct
from hwt.synthesizer.typePath import TypePath

filed_filter_t = Dict[Union[int, str], "filed_filter_t"]


def HdlType_select(t: HStruct, fieldsToUse: filed_filter_t):
    """
    Select fields from type structure (rest will become padding)

    :param t: HdlType type instance
    :param fieldsToUse: dict {name:{...}} or set of names to select,
        dictionary is used to select nested fields
        in HStruct/HUnion fields/array items
        (f.e. {"struct1": {"field1", "field2"}, "field3":{}}
        will select field1 and 2 from struct1 and field3 from root)
    """

    template = []
    fieldsToUse = fieldsToUse
    foundNames = set()
    if isinstance(t, (HArray, HStream)):
        assert len(fieldsToUse) <= 1, ("select only on item 0, because it has to be same for all array items", fieldsToUse)
        k, v = list(fieldsToUse.items())[0]
        assert k == 0
        new_t = copy(t)
        new_t.elment = HdlType_select(t.element_t, v)
        return new_t
    elif isinstance(t, (HBits, HEnum)):
        # scalar
        return t
    else:
        # struct/Union
        for f in t.fields:
            name = None
            subfields = []

            if f.name is not None:
                try:
                    if isinstance(fieldsToUse, dict):
                        subfields = fieldsToUse[f.name]
                        name = f.name
                    else:
                        if f.name in fieldsToUse:
                            name = f.name
                except KeyError:
                    name = None

            if name is not None and subfields:
                new_t = HdlType_select(f.dtype, subfields)
                template.append(HStructField(new_t, name))
            else:
                template.append(HStructField(f.dtype, name))

            if f.name is not None:
                foundNames.add(f.name)

        if isinstance(fieldsToUse, dict):
            fieldsToUse = set(fieldsToUse.keys())
        assert fieldsToUse.issubset(foundNames)

        return t.__class__(*template)


def field_path_get_type(root: HdlType, field_path: TypePath):
    """
    Get a data type of element using field path
    """
    t = root
    for p in field_path:
        if isinstance(p, int):
            t = t.element_t
        else:
            assert isinstance(p, str), p
            t = t.field_by_name[p].dtype
    return t


def HStruct_tuple_to_dict(t: HdlType, v: tuple, call_to_py_on_scalars=True) -> dict:
    """
    Convert a tuple of items for HStruct field to a dictionary field name to field value,
    recursively.
    """
    if isinstance(t, HStruct):
        assert len(v) == len(t.fields), (len(v), t)
        return {f.name: HStruct_tuple_to_dict(f.dtype, vItem, call_to_py_on_scalars=call_to_py_on_scalars)
                for f, vItem in zip(t.fields, v)}
    elif isinstance(t, HArray):
        assert len(v) == t.size, (len(v), t)
        elmT = t.element_t
        return [HStruct_tuple_to_dict(elmT, vItem, call_to_py_on_scalars=call_to_py_on_scalars)
                for vItem in v]
    else:
        assert t.isScalar(), t
        if call_to_py_on_scalars:
            return v.to_py()
        else:
            return v


def HStruct_dict_to_tuple(t: HdlType, v: tuple, call_to_py_on_scalars=True) -> dict:
    if isinstance(t, HStruct):
        assert len(v) == len(t.fields), (len(v), t)
        return tuple(HStruct_dict_to_tuple(field.dtype, v[field.name], call_to_py_on_scalars=call_to_py_on_scalars) for field in t.fields)
    elif isinstance(t, HArray):
        assert len(v) == t.size, (len(v), t)
        elmT = t.element_t
        return tuple(HStruct_dict_to_tuple(elmT, _v, call_to_py_on_scalars=call_to_py_on_scalars) for _v in v)
    else:
        assert t.isScalar(), t
        if call_to_py_on_scalars:
            return v.to_py()
        else:
            return v


def HConst_to_tuples(T: HdlType, v: Union[HConst, Sequence], call_to_py_on_scalars=True) -> tuple:
    if isinstance(T, HStruct):
        assert len(v) == len(T.fields), (len(v), T)
        return tuple(HConst_to_tuples(field.dtype, d, call_to_py_on_scalars=call_to_py_on_scalars)
                     for field, d in zip(T.fields, v))
    elif isinstance(T, HArray):
        assert len(v) == T.size, (len(v), T)
        elmT = T.element_t
        return tuple(HConst_to_tuples(elmT, d, call_to_py_on_scalars=call_to_py_on_scalars)
                     for d in v)
    else:
        assert T.isScalar(), T
        if call_to_py_on_scalars:
            return v.to_py()
        else:
            return v
    
