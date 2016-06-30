library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.package0.log2;

entity ent is
	port(
		sig2 : out std_logic_vector(log2(2) - 1 downto 0);
		sig4 : out std_logic_vector(log2(4) - 1 downto 0);
		sig64 : out std_logic_vector(log2(64) - 1 downto 0);
		sig13 : out std_logic_vector(log2(13) - 1 downto 0)
	);
end entity ent;

