from vhdl_toolkit.testbench_generator import tb_fromEntFile, formatVhdl, fifo, delay, hs
from vivado_toolkit.vivado_ip_wrap_fix import fix_wraper_to_downto

  

if __name__ == "__main__":
    wraperFn = "/home/nic30/Documents/vivado/srb_stream_buffer_simple/srb_stream_buffer_simple.srcs/sources_1/bd/top/hdl/top_wrapper.vhd"
    fix_wraper_to_downto(wraperFn)
    tb = tb_fromEntFile(wraperFn)
    tb.addClkProcess()
    sp = tb.addStimProcess(5)
    wr_req = fifo("wr_req_V")
    rd_req = fifo("rd_req_V")
    aw = hs("aw_V")
    ar = hs("ar_V")
    r = hs("r_V")
    w = hs("w_V")
    
    sp.bodyBuff += [
                    delay(5),
                    wr_req.write(255),
                    rd_req.write(255),
                    aw.read(),
                    ar.read(),
                    delay(1),
                    
                        ]
    s = formatVhdl(tb.render())
    print(s)
    with open("/home/nic30/Documents/vivado/srb_stream_buffer_simple/srb_stream_buffer_simple.srcs/sim_1/new/top_tb.vhd", 'w') as f:
        f.write(s)
