library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY InterfaceArraySample IS
	GENERIC(
		DATA_WIDTH : INTEGER := 8
	);
	PORT(a_data : IN  STD_LOGIC_VECTOR(DATA_WIDTH * 3 - 1 DOWNTO 0);
		 a_vld  : IN  STD_LOGIC_VECTOR(2 DOWNTO 0);
		 b_data : OUT STD_LOGIC_VECTOR(DATA_WIDTH * 3 - 1 DOWNTO 0);
		 b_vld  : OUT STD_LOGIC_VECTOR(2 DOWNTO 0)
	);
END InterfaceArraySample;

ARCHITECTURE rtl OF InterfaceArraySample IS
BEGIN
	b_data <= a_data;

	b_vld <= a_vld;

END ARCHITECTURE rtl;
