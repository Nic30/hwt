module ternOpInModul # (
	parameter integer LEN       = 2, 
	parameter integer DW        = 32
)
(
	
    /*
     * AXI input
     */
    input  wire [LEN*DW-1:0]     input_axis_data,
    input  wire [LEN*(DW/8)-1:0] input_axis_strb,
    input  wire [LEN-1:0]        input_axis_valid,
    output wire [LEN-1:0]        input_axis_ready,
    input  wire [LEN-1:0]        input_axis_last
);

endmodule
