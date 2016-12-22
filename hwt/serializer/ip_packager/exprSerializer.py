from hwt.serializer.vhdl.serializer import VhdlSerializer


class VivadoTclExpressionSerializer(VhdlSerializer):
    @staticmethod
    def SignalItem(si, declaration=False):
        assert(declaration == False)
        if si.hidden:
            return VhdlSerializer.asHdl(si.origin)
        else:
            return "spirit:decode(id('MODELPARAM_VALUE.%s'))" % (si.name)

