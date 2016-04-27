module parameterSizeFromParameter # (
   parameter integer A = 1, 
   parameter integer B = 2,
   parameter [A*B*64-1:0] aMultBMult64 = 128'h00000000001000000000000000000000,
   parameter [A*32-1:0] aMult32 = 32'h00000000
   )(
   	   input  wire                                                    aclk
   );
endmodule
