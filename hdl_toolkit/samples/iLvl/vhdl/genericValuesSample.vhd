library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity genericValuesSample is
	generic(
		C_FAMILY   : string           := "zynq";
		C_BASEADDR : std_logic_vector := X"FFFFFFFF"
	);
	port(
		ACLK : in std_logic
	);
end entity;