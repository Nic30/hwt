library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity AxiLite_basic_slave2 is
	port(
		ap_clk            : IN  STD_LOGIC;
		ap_rst_n          : IN  STD_LOGIC;
		axilite_AR_ADDR_V : IN  STD_LOGIC_VECTOR(3 downto 0);
		axilite_AR_VALID  : IN  STD_LOGIC;
		axilite_AR_READY  : OUT STD_LOGIC;
		axilite_AW_ADDR_V : IN  STD_LOGIC_VECTOR(3 downto 0);
		axilite_AW_VALID  : IN  STD_LOGIC;
		axilite_AW_READY  : OUT STD_LOGIC;
		axilite_R_DATA_V  : OUT STD_LOGIC_VECTOR(31 downto 0);
		axilite_R_RESP_V  : OUT STD_LOGIC_VECTOR(1 downto 0);
		axilite_R_VALID   : OUT STD_LOGIC;
		axilite_R_READY   : IN  STD_LOGIC;
		axilite_W_DATA_V  : IN  STD_LOGIC_VECTOR(31 downto 0);
		axilite_W_STRB_V  : IN  STD_LOGIC_VECTOR(3 downto 0);
		axilite_W_VALID   : IN  STD_LOGIC;
		axilite_W_READY   : OUT STD_LOGIC;
		axilite_B_RESP_V  : OUT STD_LOGIC_VECTOR(1 downto 0);
		axilite_B_VALID   : OUT STD_LOGIC;
		axilite_B_READY   : IN  STD_LOGIC
	);
end;