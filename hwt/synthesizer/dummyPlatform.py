
class DummyPlatform():
    """
    :note: all processors has to be callable with only one parameter
        which is actual Unit/RtlNetlist instance
    """

    def __init__(self):
        self.beforeToRtl = []
        self.beforeToRtlImpl = []
        self.afterToRtlImpl = []

        self.beforeHdlArchGeneration = []
        self.afterToRtl = []

        from hwt.serializer.xdc.serializer import XdcSerializer
        self.constraint_serializer = [XdcSerializer, ]
