module sizeExprssions # (
		 parameter integer paramA = 32,
		 parameter integer paramB = 4
)
(
		input  wire [paramA - 1:0]                portA,
		input  wire [(paramA - 1):0]              portB,
		input  wire [(paramA / 8) - 1:0]          portC,
		input  wire [13 * (paramA / 8) - 1:0]     portD,
		input  wire [paramB * (paramA / 8) - 1:0] portE,
		input  wire [paramB * paramA - 1:0]       portF,
		input  wire [paramB * (paramA - 4) - 1:0] portG
);
endmodule
 