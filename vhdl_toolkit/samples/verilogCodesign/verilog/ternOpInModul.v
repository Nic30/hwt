module ternOpInModul # (
   parameter integer CONDP                 = 0 
)
(
   input  wire [((CONDP == 1) ? 4 : 8)-1:0] a,
   input  wire [((CONDP == 1) ? 2 : 1)-1:0] b
);

endmodule
