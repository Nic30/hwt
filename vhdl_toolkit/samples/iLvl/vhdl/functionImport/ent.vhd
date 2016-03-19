library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.package0.max;

entity ent is
	port(
		sig : out std_logic_vector(max(10, 20) - 1 downto 0)
	);
end entity ent;

