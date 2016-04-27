library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ARCHITECTURE rtl OF subunit0 IS
BEGIN
	a_ready <= b_ready;
	b_data  <= a_data;
	b_last  <= a_last;
	b_strb  <= a_strb;
	b_valid <= a_valid;
END ARCHITECTURE rtl;