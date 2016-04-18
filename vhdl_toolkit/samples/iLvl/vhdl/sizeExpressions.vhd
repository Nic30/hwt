library ieee;
use ieee.std_logic_1164.all;

entity arbiter is
	generic(
		param_A : integer := 32;
		param_B : integer := 4
	);
	port(
		portA, portA1 : in  std_logic_vector(param_A - 1 downto 0);
		portB, portB1 : in  std_logic_vector((param_A - 1) downto 0);
		portC, portC1 : in  std_logic_vector((param_A / 8) - 1 downto 0);
		portD, portD1 : in  std_logic_vector(13 * (param_A / 8) - 1 downto 0);
		portE, portE1 : in  std_logic_vector(param_B * (param_A / 8) - 1 downto 0);
		portF, portF1 : in  std_logic_vector(param_B * param_A - 1 downto 0);
		portG, portG1 : in  std_logic_vector(param_B * (param_A - 4) - 1 downto 0);

		portH         : out std_logic
	);
end entity;
 