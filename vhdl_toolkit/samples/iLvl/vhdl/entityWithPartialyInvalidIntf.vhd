library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity superDMA is
	port(
		descrBM_w_wr_addr_V_123 : OUT STD_LOGIC_VECTOR(8 downto 0);
		descrBM_w_wr_din_V      : OUT STD_LOGIC_VECTOR(63 downto 0);
		descrBM_w_wr_dout_V     : IN  STD_LOGIC_VECTOR(63 downto 0);
		descrBM_w_wr_en         : OUT STD_LOGIC;
		descrBM_w_wr_we         : OUT STD_LOGIC);
end;