from hwt.hdl.types.struct import HStructField, HStruct


def HStruct_selectFields(structT: HStruct, fieldsToUse):
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
