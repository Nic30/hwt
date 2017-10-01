from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.struct import HStructField, HStruct
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.types.union import HUnion


def HStruct_selectFields(structT, fieldsToUse):
    """
    Select fields from structure (rest will become spacing)

    :param structT: HStruct type instance
    :param fieldsToUse: dict {name:{...}} or set of names to select,
        dictionary is used to select nested fields
        in HStruct or HUnion fields
        (f.e. {"struct1": {"field1", "field2"}, "field3":{}}
        will select field1 and 2 from struct1 and field3 from root)
    """

    template = []
    fieldsToUse = fieldsToUse
    foundNames = set()

    for f in structT.fields:
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
            fields = HStruct_selectFields(f.dtype, subfields)
            template.append(HStructField(fields, name))
        else:
            template.append(HStructField(f.dtype, name))

        if f.name is not None:
            foundNames.add(f.name)

    if isinstance(fieldsToUse, dict):
        fieldsToUse = set(fieldsToUse.keys())
    assert fieldsToUse.issubset(foundNames)

    return HStruct(*template)


def walkFlattenFields(sigOrVal, skipPadding=True):
    """
    Walk all simple values in HStruct or HArray
    """
    t = sigOrVal._dtype
    if isinstance(t, Bits):
        yield sigOrVal
    elif isinstance(t, HUnion):
        yield from walkFlattenFields(sigOrVal._val, skipPadding=skipPadding)
    elif isinstance(t, HStruct):
        for f in t.fields:
            isPadding = f.name is None
            if not isPadding or not skipPadding:
                if isPadding:
                    v = f.dtype.fromPy(None)
                else:
                    v = getattr(sigOrVal, f.name)

                yield from walkFlattenFields(v)

    elif isinstance(t, HArray):
        for item in sigOrVal:
            yield from walkFlattenFields(item)
    else:
        raise NotImplementedError(t)


def HStruct_unpack(structT, data, getDataFn=None, dataWidth=None):
    """
    opposite of packAxiSFrame
    """
    if getDataFn is None:
        assert dataWidth is not None

        def _getDataFn(x):
            return toHVal(x)._auto_cast(Bits(dataWidth))

        getDataFn = _getDataFn

    val = structT.fromPy(None)

    fData = iter(data)

    # actual is storage variable for items from frameData
    actualOffset = 0
    actual = None

    for v in walkFlattenFields(val, skipPadding=False):
        # walk flatten fields and take values from fData and parse them to field
        required = v._dtype.bit_length()

        if actual is None:
            actualOffset = 0
            try:
                actual = getDataFn(next(fData))
            except StopIteration:
                raise Exception("Input data too short")

            if dataWidth is None:
                dataWidth = actual._dtype.bit_length()
            actuallyHave = dataWidth
        else:
            actuallyHave = actual._dtype.bit_length() - actualOffset

        while actuallyHave < required:
            # collect data for this field
            try:
                d = getDataFn(next(fData))
            except StopIteration:
                raise Exception("Input data too short")

            actual = d._concat(actual)
            actuallyHave += dataWidth

        if actuallyHave >= required:
            # parse value of actual to field
            # skip padding
            _v = actual[(required + actualOffset): actualOffset]._auto_cast(v._dtype)
            v.val = _v.val
            v.vldMask = _v.vldMask
            v.updateTime = _v.updateTime

            # update slice out what was taken
            actuallyHave -= required
            actualOffset += required

        if actuallyHave == 0:
            actual = None

    if actual is not None:
        assert actual._dtype.bit_length() - actualOffset < dataWidth, "It should be just a padding at the end of frame"

    return val