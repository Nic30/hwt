module  SimpleParamMod # (
   parameter integer param_int = 3,
   parameter         param_str = "rtl",
   parameter integer  WIDTH_WIDTH = 32, 
   parameter [WIDTH_WIDTH-1:0] C_WIDTH = 32'H000c
)(
   input wire  [WIDTH_WIDTH-1:0] d_in, 
   output wire [WIDTH_WIDTH-1:0] d_out      
);

endmodule 


