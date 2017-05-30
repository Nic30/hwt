from hwt.hdlObjects.types.struct import HStructField, HStruct


# [TODO] rename to BusFieldMeta
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

