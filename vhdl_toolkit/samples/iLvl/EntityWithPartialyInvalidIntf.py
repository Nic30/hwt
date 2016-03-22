from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource

class EntityWithPartialyInvalidIntf(UnitWithSource):
    _hdlSources = "../../samples/iLvl/vhdl/entityWithPartialyInvalidIntf.vhd"
    

if __name__ == "__main__":
    u = EntityWithPartialyInvalidIntf()
    [ s for s in u._synthesise()]
    print(u._entity)
    assert(u.descrBM_w_wr_addr_V_123._parent == u)
    assert(u.descrBM_w_wr_din_V._parent == u)
    assert(u.descrBM_w_wr_dout_V._parent == u)
    assert(u.descrBM_w_wr_en._parent == u)
    assert(u.descrBM_w_wr_we._parent == u)
    assert(len(u._interfaces.keys()) == len(u._entity.ports))