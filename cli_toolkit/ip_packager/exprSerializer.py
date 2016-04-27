from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer


class VivadoTclExpressionSerializer(VhdlSerializer):
    @staticmethod
    def SignalItem(si, declaration=False):
        assert(declaration == False)
        if VhdlSerializer.isSignalHiddenInExpr(si):
            return VhdlSerializer.asHdl(si.origin)
        else:
            return "spirit:decode(id('MODELPARAM_VALUE.%s'))" % (si.name)

