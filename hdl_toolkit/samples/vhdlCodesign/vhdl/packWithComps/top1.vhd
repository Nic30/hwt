----------------------------------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.package1.ALL;

entity top1 is
	port(
		clk     : in  std_logic;
		rst     : in  std_logic;
		en      : in  std_logic;
		top_sh  : in  std_logic;        -- for shift register
		top_in  : in  std_logic_vector(1 downto 0);
		top_out : out std_logic_vector(decWidth - 1 downto 0)
	);
end top1;

architecture struct of top1 is
	signal tmpReg2Sh, tmpSh2Enc : std_logic_vector(3 downto 0);
	signal tmpEnc2Dec           : std_logic_vector(1 downto 0);

begin

	-- I will use positional mapping here
	COMP1 : ckt_reg port map(clk, rst, en, top_in, tmpReg2Sh);
	COMP2 : shiftReg port map(clk, rst, en, top_sh, tmpReg2Sh, tmpSh2Enc);
	COMP3 : encode1 port map(tmpSh2Enc, tmpEnc2Dec);
	COMP4 : decode1 port map(clk, rst, tmpEnc2Dec, top_out);

end struct;
----------------------------------------------------------------------------------------------------------
