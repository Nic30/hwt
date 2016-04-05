module  SimpleParamMod # (
   parameter integer param_int = 3,
   parameter         param_str = "rtl",
   parameter [32-1:0] C_M_AXI_ADDR_WIDTH = 32'H000c
)(
   input wire d_in      , 
   output wire d_out      
);

endmodule 


