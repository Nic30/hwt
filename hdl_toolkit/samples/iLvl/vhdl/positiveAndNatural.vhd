library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY PositiveAndNatural IS
	GENERIC(
		pos : positive := 1;
		nat : natural  := 2;
		int : integer  := 3
	);
	PORT(a : IN  STD_LOGIC;
		 b : OUT STD_LOGIC
	);
END SimpleUnit_b;
