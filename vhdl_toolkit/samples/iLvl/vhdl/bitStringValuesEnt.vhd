library ieee;
use ieee.std_logic_1164.all;


entity BitStringValuesEnt is
	generic(
		C_128b1 : std_logic_vector := X"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF";
		C_16b1  : std_logic_vector := X"0000FFFF";
		C_32b1  : std_logic_vector := X"FFFFFFFF";
		C_32b0  : std_logic_vector := X"00000000"
	);
	port(
		ACLK : in std_logic
	);
end BitStringValuesEnt;