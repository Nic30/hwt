from vhdl_toolkit.parser import entityFromFile
from vivado_toolkit.ip_packager.packager import packageMultipleProjects


if __name__ == "__main__":
    ipRepo = "/home/nic30/Documents/ip_repo"
    workspace = "/home/nic30/Documents/vivado_hls/"
    packageMultipleProjects(workspace, 
                            {"superDMA": "superDMA",
                             "SuperDMA_inBuffer":"InputBuffer",
                             "MultiFIFO_test":"MultiFifo_top",
                             "DDM_test": "DDM_top",
                             "superDMA_axi_regs" : "axi_regs_with_def_value"
                             },
                             ipRepo)
    
    # e = entityFromFile("/home/nic30/Documents/vivado_hls/superDMA_axi_regs/solution1/syn/vhdl/axi_regs_with_def_value.vhd")
    # m = doesBusInterfFit(e, )
    # packageBD("/home/nic30/Documents/vivado/axi_trans_tester2/axi_trans_tester2.srcs/sources_1/bd/axi_tester_complex", ipRepo)
