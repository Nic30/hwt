library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY subunit0 IS
	GENERIC(
		DATA_WIDTH : INTEGER := 8
	);
	PORT(a_data  : IN  STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
		 a_last  : IN  STD_LOGIC;
		 a_ready : OUT STD_LOGIC;
		 a_strb  : IN  STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
		 a_valid : IN  STD_LOGIC;
		 b_data  : OUT STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
		 b_last  : OUT STD_LOGIC;
		 b_ready : IN  STD_LOGIC;
		 b_strb  : OUT STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
		 b_valid : OUT STD_LOGIC
	);
END subunit0;