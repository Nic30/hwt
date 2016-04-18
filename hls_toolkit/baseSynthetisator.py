
class BaseHlsSynthetisator():
    def __init__(self, iLvUnit, ctx, hlsFn):
        """
        @param iLvUnit: interface level unit where is this hlsFn placed
        @param ctx: signal level context where all synthesised object will be placed
        @param hlsFn: function which is template for synthesis
        """
        self.iLvUnit = iLvUnit
        self.ctx = ctx
        self.hlsFn = hlsFn
        
    def allInterfaces(self):
        """
        @return: iterator over all interfaces and subinterfaces in this iLvUnit
        """
        def forIntf(intf):
            yield intf
            for _, subInt in intf._subInterfaces.items():
                forIntf(subInt)
        for _, intf in self.iLvUnit._interfaces.items():
            yield from forIntf(intf)
            
    def allNodes(self):
        """
        @return: iterator over all hls operations in this iLvUnit
        """
        for intf in self.allInterfaces():
            yield from intf._hlsNodes
        
    def _synthesise(self):
        """
        dump all operations to signal level context
        """
        for intf in self.allInterfaces():
            intf._hlsNodes = []
        # self.hlsFn(self.iLvUnit)
        fn = self.hlsFn

        c = fn.__code__
        print(c.code)
        # Modify the byte code
        c.code[0] = (LOAD_CONST, 1000)
        fn.func_code = c.to_code()
        print(c.code)

        for n in self.allNodes():
            n.rValid._sig.assignFrom(n.lValid._sig)
            n.lReady._sig.assignFrom(n.rReady._sig)
            n.rData._sig.assignFrom(n.ldata._sig)
            renderHlsContainers(n)


def renderHlsContainers(n):
    def assig(a, b):
        print("%s <= %s" % (a, b))
        
    assig(n.rValid._getFullName(), n.lValid._getFullName())
    assig(n.lReady._getFullName(), n.rReady._getFullName())

def hls(fn):
    """
    hls function marker
    """
    fn._synthetisator = BaseHlsSynthetisator
    return fn
