from _ast import Expression

def setReset(name):
    activeInStr = "ACTIVE_"
    if name.lower().endswith("_n"):
        activeInStr += "LOW"
    else:
        activeInStr += "HIGH"
    return """
    ipx::add_bus_interface {0} [ipx::current_core]
    set_property abstraction_type_vlnv xilinx.com:signal:reset_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property bus_type_vlnv xilinx.com:signal:reset:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property display_name {0} [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    ipx::add_port_map RST [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0} [ipx::get_port_maps RST -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_bus_parameter POLARITY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property value {1} [ipx::get_bus_parameters POLARITY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    """.format(name, activeInStr)
    
def setFifo_slave(name, rw='r'):
    if rw == 'r':
        return """
        ipx::add_bus_interface {0} [ipx::current_core]
        set_property abstraction_type_vlnv xilinx.com:interface:fifo_read_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property bus_type_vlnv xilinx.com:interface:fifo_read:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property display_name {0} [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        ipx::add_port_map RD_DATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_dout_V [ipx::get_port_maps RD_DATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map RD_EN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_rd_en [ipx::get_port_maps RD_EN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map EMPTY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_empty [ipx::get_port_maps EMPTY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        """.format(name)
    elif rw == 'w':
        return """
        ipx::add_bus_interface {0} [ipx::current_core]
        set_property abstraction_type_vlnv xilinx.com:interface:fifo_write_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property bus_type_vlnv xilinx.com:interface:fifo_write:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property display_name {0} [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        ipx::add_port_map WR_DATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_din_V [ipx::get_port_maps WR_DATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map WR_EN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_wr_en [ipx::get_port_maps WR_EN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map FULL [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_full [ipx::get_port_maps FULL -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        """.format(name)
    else:
        raise Expression("rw supports only r or w")
    
def setACC_FIFO_master(name, rw='r'):
    if rw == 'r':
        return """#{0} to acc_fifo_read
        ipx::add_bus_interface {0} [ipx::current_core]
        set_property abstraction_type_vlnv xilinx.com:interface:acc_fifo_read_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property bus_type_vlnv xilinx.com:interface:acc_fifo_read:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property interface_mode master [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        ipx::add_port_map RD_DATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_rd_data [ipx::get_port_maps RD_DATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map RD_EN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_rd_en [ipx::get_port_maps RD_EN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map EMPTY_N [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_empty_n [ipx::get_port_maps EMPTY_N -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        """.format(name)
    elif rw == 'w':
        return """
        ipx::add_bus_interface {0} [ipx::current_core]
        set_property abstraction_type_vlnv xilinx.com:interface:acc_fifo_write_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property bus_type_vlnv xilinx.com:interface:acc_fifo_write:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property interface_mode master [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property display_name {0} [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        ipx::add_port_map WR_DATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_wr_data [ipx::get_port_maps WR_DATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map WR_EN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_wr_en [ipx::get_port_maps WR_EN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        ipx::add_port_map FULL_N [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
        set_property physical_name {0}_V_full_n [ipx::get_port_maps FULL_N -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
        """.format(name)
    else:
        raise Exception("rw supports only r or w")
    

def fixPorts():
    """
    ipx::update_ip_instances -delete_project true
    ipx::edit_ip_in_project -upgrade true -name axi_native_intf_v1_0_project -directory /home/nic30/Documents/vivado_hls/axi_ch_a/solution1/impl/ip/axi_native_intf_v1_0_project /home/nic30/Documents/vivado_hls/axi_ch_a/solution1/impl/ip/component.xml

#in opened window
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1
ipx::remove_all_port [ipx::current_core]
ipx::add_ports_from_hdl [ipx::current_core] -top_level_hdl_file /home/nic30/Documents/vivado_hls/axi_ch_a/solution1/impl/ip/hdl/vhdl/axi_native_intf.vhd -top_module_name axi_native_intf

ipx::remove_bus_interface {0}_AW_ID_V [ipx::current_core]
current_project axi_phy
ipx::remove_bus_interface {0}_AW_ADDR_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_LEN_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_SIZE_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_BURST_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_LOCK_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_CACHE_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_PROT_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_QOS_V [ipx::current_core]
ipx::remove_bus_interface {0}_AW_VALID [ipx::current_core]
ipx::remove_bus_interface {0}_AW_READY [ipx::current_core]
ipx::remove_bus_interface {0}_AR_ID_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_ADDR_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_LEN_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_SIZE_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_BURST_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_LOCK_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_CACHE_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_PROT_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_QOS_V [ipx::current_core]
ipx::remove_bus_interface {0}_AR_VALID [ipx::current_core]
ipx::remove_bus_interface {0}_AR_READY [ipx::current_core]
ipx::remove_bus_interface {0}_W_ID_V [ipx::current_core]
ipx::remove_bus_interface {0}_W_DATA_V [ipx::current_core]
ipx::remove_bus_interface {0}_W_STRB_V [ipx::current_core]
ipx::remove_bus_interface {0}_W_LAST [ipx::current_core]
ipx::remove_bus_interface {0}_W_VALID [ipx::current_core]
ipx::remove_bus_interface {0}_W_READY [ipx::current_core]
ipx::remove_bus_interface {0}_R_ID_V [ipx::current_core]
ipx::remove_bus_interface {0}_R_DATA_V [ipx::current_core]
ipx::remove_bus_interface {0}_R_RESP_V [ipx::current_core]
ipx::remove_bus_interface {0}_R_LAST [ipx::current_core]
ipx::remove_bus_interface {0}_R_VALID [ipx::current_core]
ipx::remove_bus_interface {0}_R_READY [ipx::current_core]
ipx::remove_bus_interface {0}_B_ID_V [ipx::current_core]
ipx::remove_bus_interface {0}_B_RESP_V [ipx::current_core]
ipx::remove_bus_interface {0}_B_VALID [ipx::current_core]
ipx::remove_bus_interface {0}_B_READY [ipx::current_core]



    """
def setAxiM(name):
    return """
    current_project axi_native_intf_v1_0_project
    ipx::add_bus_interface {0} [ipx::current_core]
    set_property abstraction_type_vlnv xilinx.com:interface:aximm_rtl:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property bus_type_vlnv xilinx.com:interface:aximm:1.0 [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property interface_mode master [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property display_name {0} [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    ipx::add_port_map WLAST [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_LAST [ipx::get_port_maps WLAST -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map BREADY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_B_READY [ipx::get_port_maps BREADY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWLEN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_LEN_V [ipx::get_port_maps AWLEN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWQOS [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_QOS_V [ipx::get_port_maps AWQOS -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWREADY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_READY [ipx::get_port_maps AWREADY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARBURST [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_BURST_V [ipx::get_port_maps ARBURST -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWPROT [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_PROT_V [ipx::get_port_maps AWPROT -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RRESP [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_RESP_V [ipx::get_port_maps RRESP -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARPROT [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_PROT_V [ipx::get_port_maps ARPROT -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RVALID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_VALID [ipx::get_port_maps RVALID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARLOCK [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_LOCK_V [ipx::get_port_maps ARLOCK -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_ID_V [ipx::get_port_maps AWID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RLAST [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_LAST [ipx::get_port_maps RLAST -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_ID_V [ipx::get_port_maps ARID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWCACHE [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_CACHE_V [ipx::get_port_maps AWCACHE -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map WREADY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_READY [ipx::get_port_maps WREADY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map WSTRB [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_STRB_V [ipx::get_port_maps WSTRB -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map BRESP [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_B_RESP_V [ipx::get_port_maps BRESP -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map BID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_B_ID_V [ipx::get_port_maps BID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARLEN [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_LEN_V [ipx::get_port_maps ARLEN -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARQOS [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_QOS_V [ipx::get_port_maps ARQOS -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RDATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_DATA_V [ipx::get_port_maps RDATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map BVALID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_B_VALID [ipx::get_port_maps BVALID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARCACHE [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_CACHE_V [ipx::get_port_maps ARCACHE -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RREADY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_READY [ipx::get_port_maps RREADY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWVALID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_VALID [ipx::get_port_maps AWVALID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARSIZE [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_SIZE_V [ipx::get_port_maps ARSIZE -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map WDATA [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_DATA_V [ipx::get_port_maps WDATA -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWSIZE [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_SIZE_V [ipx::get_port_maps AWSIZE -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map RID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_R_ID_V [ipx::get_port_maps RID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARADDR [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_ADDR_V [ipx::get_port_maps ARADDR -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map WID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_ID_V [ipx::get_port_maps WID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWADDR [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_ADDR_V [ipx::get_port_maps AWADDR -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARREADY [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_READY [ipx::get_port_maps ARREADY -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map WVALID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_W_VALID [ipx::get_port_maps WVALID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map ARVALID [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AR_VALID [ipx::get_port_maps ARVALID -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWLOCK [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_LOCK_V [ipx::get_port_maps AWLOCK -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    ipx::add_port_map AWBURST [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]
    set_property physical_name {0}_AW_BURST_V [ipx::get_port_maps AWBURST -of_objects [ipx::get_bus_interfaces {0} -of_objects [ipx::current_core]]]
    """.format(name)




if __name__ == "__main__":
    print(setReset("ap_rst"))
    print(setACC_FIFO_master("rd_req"))
    print(setACC_FIFO_master("wr_req"))
    print(setACC_FIFO_master("data_in"))
    print(setACC_FIFO_master("data_out", 'w'))
    