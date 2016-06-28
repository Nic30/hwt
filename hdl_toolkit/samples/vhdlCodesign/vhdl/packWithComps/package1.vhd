----------------------------------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

package package1 is

	-- *********************
	-- here's the 4-bit register
	-- *********************
	component ckt_reg is
		Port(clk     : in  STD_LOGIC;
			 rst     : in  STD_LOGIC;
			 loadEn  : in  STD_LOGIC;
			 reg_in  : in  STD_LOGIC_VECTOR(regCount - 1 downto 0);
			 reg_out : out STD_LOGIC_VECTOR(regCount - 1 downto 0)
		);
	end component;

	-- **************************
	-- here's the 4-bit shift register
	-- **************************
	component shiftReg is
		Port(clk       : in  STD_LOGIC;
			 rst       : in  STD_LOGIC;
			 shiftEn   : in  STD_LOGIC;
			 sh_in     : in  STD_LOGIC;
			 shReg_in  : in  STD_LOGIC_VECTOR(3 downto 0);
			 shReg_out : out STD_LOGIC_VECTOR(3 downto 0));
	end component;

	-- *****************
	-- here's the encoder
	-- *****************
	component encode1 is
		Port(enc_in  : in  std_logic_vector(3 downto 0);
			 enc_out : out std_logic_vector(1 downto 0));
	end component;

	-- *****************
	-- here's the decoder
	-- *****************
	component decode1 is
		Port(clk     : in  std_logic;
			 rst     : in  std_logic;
			 dec_in  : in  std_logic_vector(1 downto 0);
			 dec_out : out std_logic_vector(7 downto 0));
	end component;

end package1;

