

class ResourceError(Exception):
    """
    An error which means that the resource of this kind
    does not exists in current hardware.
    """


class RtlResourceType():
    """
    A base class for resource type descriptions.
    """


class ResourceMUX(RtlResourceType):

    def __init__(self, bitWidth, inputs):
        self.bitWidth = bitWidth
        self.inputs = inputs

    def __repr__(self):
        return f"<{self.__class__.__name__:s} {self.bitWidth:d} bits, {self.inputs} inputs>"


class ResourceFF(RtlResourceType):
    pass


class ResourceLatch(RtlResourceType):
    pass


class ResourceRAM(RtlResourceType):
    """
    Specifier of type of RAM like memory
    """

    def __init__(self, width, items,
                 rwSync: int, rSync: int, wSync: int, rSync_wAsync: int,
                 rwAsync: int, rAsync: int, wAsync: int, rAsync_wSync: int):
        """
        :param width: width of word in RAM/ROM
        :param items: number of words in RAM/ROM
        :param rwSync: count of read + write synchronous ports
        :param rSync: count of read only synchronous ports
        :param wSync: count of write only synchronous ports
        :param rSync_wAsync: count of synchronous read + asynchronous write ports
        :param rwAsync: count of read + write asynchronous ports
        :param rAsync: count of read only asynchronous ports
        :param wAsync: count of write only asynchronous ports
        :param rAsync_wSync: count of asynchronous read + synchronous write ports
        """
        self.width = width
        self.items = items
        self.rwSync = rwSync
        self.rSync = rSync
        self.wSync = wSync
        self.rSync_wAsync = rSync_wAsync
        self.rwAsync = rwAsync
        self.rAsync = rAsync
        self.wAsync = wAsync
        self.rAsync_wSync = rAsync_wSync

    def __hash__(self):
        return hash((
            self.width, self.items,
            self.rwSync, self.rSync, self.wSync,
            self.rSync_wAsync,
            self.rwAsync, self.rAsync, self.wAsync,
            self.rAsync_wSync))

    def __eq__(self, other):
        return isinstance(other, ResourceRAM) and (
            self.width == other.width and
            self.items == other.items and
            self.rwSync == other.rwSync and
            self.rSync == other.rSync and
            self.wSync == other.wSync and
            self.rSync_wAsync == other.rSync_wAsync and
            self.rwAsync == other.rwAsync and
            self.rAsync == other.rAsync and
            self.wAsync == other.wAsync and
            self.rAsync_wSync == other.rAsync_wSync
        )

    def __repr__(self):
        return ("<%s, %dbit x %d, syncPorts: (rw:%d, r:%d, w:%d), asyncPorts:"
                " (rw:%d, r:%d, w:%d), rSync_wAsyncPorts: %d,"
                " rAsync_wSyncPorts: %d>") % (
            self.__class__.__name__, self.width, self.items,
            self.rwSync, self.rSync, self.wSync,
            self.rwAsync, self.rAsync, self.wAsync,
            self.rSync_wAsync, self.rAsync_wSync
        )
