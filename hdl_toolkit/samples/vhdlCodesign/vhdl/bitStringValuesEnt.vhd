library ieee;
use ieee.std_logic_1164.all;


entity BitStringValuesEnt is
	generic(
                C_1     : std_logic := '1';
                C_0     : std_logic := '0';
                C_1b1   : std_logic_vector := "1";
                C_1b0   : std_logic_vector := "0";
		C_16b1  : std_logic_vector := X"0000FFFF";
		C_32b0  : std_logic_vector := X"00000000";
		C_32b1  : std_logic_vector := X"FFFFFFFF";
		C_128b1 : std_logic_vector := X"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"

	);
	port(
		ACLK : in std_logic
	);
end BitStringValuesEnt;
