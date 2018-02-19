from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.hdl.process import HWProcess
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.resourceAnalyzer.resourceTypes import Unconnected, \
    ResourceMUX, ResourceLatch, ResourceLatchWithMux, ResourceRAM,\
    ResourceAsyncRAM, ResourceFF
from hwt.serializer.resourceAnalyzer.utils import ResourceContext
from hwt.hdl.types.array import HArray


class ResourceAnalyzer(GenericSerializer):
    """
    Serializer which does not products any output just collect informations
    about used resources

    :attention: Use instance of ResourceAnalyzer instead of class
    """
    _keywords_dict = {}

    def __init__(self):
        self.context = ResourceContext(None)

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx: ResourceContext) -> None:
        """
        Gues resource usage by HWProcess
        """
        for stm in proc.body:
            encl = stm._enclosed_for
            full_ev_dep = stm._is_completly_event_dependent
            now_ev_dep = stm._now_is_event_dependent
            ev_dep = full_ev_dep or now_ev_dep

            for o in stm._outputs:
                if isinstance(o._dtype, HArray):
                    # write port
                    if ev_dep:
                        res = ResourceRAM()
                    else:
                        res = ResourceAsyncRAM()
                elif ev_dep:
                    res = ResourceFF()
                elif o not in encl:
                    res = ResourceLatch()
                elif stm.rank > 0:
                    res = ResourceMUX()
                else:
                    # just a connection
                    continue
                ctx.register(o, res)

    @classmethod
    def Entity(cls, ent: Entity, ctx: ResourceContext) -> None:
        """
        Entity is just header, we do not need to inspect it for resources
        """
        return

    def getBaseContext(self) -> ResourceContext:
        """
        Return context for collecting of resource informatins
        prepared on this instance
        """
        return self.context

    @classmethod
    def Architecture(cls, arch: Architecture, ctx: ResourceContext) -> None:
        for c in arch.componentInstances:
            raise NotImplementedError()

        for proc in arch.processes:
            cls.HWProcess(proc, ctx)

        # [TODO] constant to ROMs

        ctx.finalize()

    def report(self):
        return self.context.resources
