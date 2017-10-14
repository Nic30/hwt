from hwt.serializer.vhdl.serializer import VhdlSerializer


class VivadoTclExpressionSerializer(VhdlSerializer):
    # disabled because this code is not reachable in current implemetation
    @staticmethod
    def SignalItem(si, declaration=False):
        raise NotImplementedError()
