from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStructField, HStruct
from hwt.hdlObjects.types.typeCast import toHVal


# [TODO] remove
class BusFieldInfo(object):
    def __init__(self, access="rw", fieldInterface=None, disolveArray=False):
        """
        :param access: "r", "w" or "rw" describes access mode from bus side
        :param fieldInterface: interface for which this field was generated
        :param disolveArray: interpret this array interface as bunch of items
            instead of single memory space
        """
        assert access in ['r', 'w', 'rw']
        self.access = access
        self.fieldInterface = fieldInterface
        self.disolveArray = disolveArray


def HStruct_selectFields(structT, fieldsToUse):
    """
    Select fields from structure (rest will become spacing)

    :param structT: HStruct type instance
    :param fieldsToUse: dict {name:{...}} or set of names to select, dictionary is used to select nested fields
        in HStruct or HUnion fields (f.e. {"struct1": {"field1", "field2"}, "field3":{}}
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
            template.append(HStructField(HStruct_selectFields(f.dtype, subfields), name))
        else:
            template.append(HStructField(f.dtype, name))

        if f.name is not None:
            foundNames.add(f.name)

    if isinstance(fieldsToUse, dict):
        fieldsToUse = set(fieldsToUse.keys())
    assert fieldsToUse.issubset(foundNames)

    return HStruct(*template)


def walkFlattenFields(structVal, skipPadding=True):
    """
    Walk all simple values in HStruct or Array
    """
    t = structVal._dtype
    if isinstance(t, Bits):
        yield structVal
    elif isinstance(t, HStruct):
        for f in t.fields:
            isPadding = f.name is None
            if not isPadding  or not skipPadding:
                if isPadding:
                    v = f.dtype.fromPy(None)
                else:
                    v = getattr(structVal, f.name)

                yield from walkFlattenFields(v)

    elif isinstance(t, Array):
        for item in structVal:
            yield from walkFlattenFields(item)
    else:
        raise NotImplementedError()


def HStruct_unpack(structT, data, getDataFn=None, dataWidth=None):
    """
    opposite of packAxiSFrame
    """
    if getDataFn is None:
        assert dataWidth is not None
        def _getDataFn(x):
            return toHVal(x)._convert(Bits(dataWidth))

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
            _v = actual[(required + actualOffset): actualOffset]._convert(v._dtype)
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