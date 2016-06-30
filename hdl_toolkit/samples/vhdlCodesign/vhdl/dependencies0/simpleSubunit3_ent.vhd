library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY SimpleSubunit3 IS
	GENERIC(
		DATA_WIDTH : INTEGER := 8
	);
	PORT(a0_data  : IN  STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
		 a0_last  : IN  STD_LOGIC;
		 a0_ready : OUT STD_LOGIC;
		 a0_strb  : IN  STD_LOGIC_VECTOR(1 - 1 DOWNTO 0);
		 a0_valid : IN  STD_LOGIC;
		 b0_data  : OUT STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
		 b0_last  : OUT STD_LOGIC;
		 b0_ready : IN  STD_LOGIC;
		 b0_strb  : OUT STD_LOGIC_VECTOR(1 - 1 DOWNTO 0);
		 b0_valid : OUT STD_LOGIC
	);
END SimpleSubunit3;