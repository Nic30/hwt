
class ResourceError(Exception):
    """
    Resource of this kind does not exists in current hardware
    """


class Unconnected():
    pass


class ResourceMUX():
    def __init__(self, bitWidth, inputs):
        self.bitWidth = bitWidth
        self.inputs = inputs


class ResourceFF():
    pass


class ResourceFFwithMux():
    pass


class ResourceLatch():
    pass


class ResourceLatchWithMux():
    pass


class ResourceAsyncRAM():
    pass


class ResourceAsyncROM():
    pass


class ResourceRAM():
    """
    Specifier of type of RAM like memory
    """

    def __init__(self, width, items,
                 rwSyncPorts, rSyncPorts, wSyncPorts,
                 rwAsyncPorts, rAsyncPorts, wAsyncPorts):
        self.width = width
        self.items = items
        self.rwSyncPorts = rwSyncPorts
        self.rSyncPorts = rSyncPorts
        self.wSyncPorts = wSyncPorts
        self.rwAsyncPorts = rwAsyncPorts
        self.rAsyncPorts = rAsyncPorts
        self.wAsyncPorts = wAsyncPorts

    def __hash__(self):
        return hash((self.width, self.items,
                     self.rwSyncPorts, self.rSyncPorts,
                     self.wSyncPorts,
                     self.rwAsyncPorts, self.rAsyncPorts,
                     self.wAsyncPorts))

    def __eq__(self, other):
        return (
            self.width == other.width and
            self.items == other.items and
            self.rwSyncPorts == other.rwSyncPorts and
            self.rSyncPorts == other.rSyncPorts and
            self.wSyncPorts == other.wSyncPorts and
            self.rwAsyncPorts == other.rwAsyncPorts and
            self.rAsyncPorts == other.rAsyncPorts and
            self.wAsyncPorts == other.wAsyncPorts
        )

    def __repr__(self):
        return ("<%s, %dbx%d, syncPorts: (rw:%d, r:%d, w:%d), asyncPorts:"
                " (rw:%d, r:%d, w:%d)>") % (
            self.__class__.__name__, self.width, self.items,
            self.rwSyncPorts, self.rSyncPorts, self.wSyncPorts,
            self.rwAsyncPorts, self.rAsyncPorts, self.wAsyncPorts
        )


class ResourceROM():
    pass
