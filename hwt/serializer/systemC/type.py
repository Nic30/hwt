

class SystemCSerializer_type():
    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        
        w = typ.bit_length()
        
        if w <= 64:
            if typ.signed:
                typeBaseName = "int" 
            else:
                typeBaseName = "uint"
        else:
            if typ.signed:
                typeBaseName = "bigint" 
            else:
                typeBaseName = "biguint"
            
        return "sc_%s<%d>" % (typeBaseName, w)