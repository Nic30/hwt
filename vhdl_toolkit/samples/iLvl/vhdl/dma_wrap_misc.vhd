
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package misc_pkg is
	type array_of_natural  is array(natural range <>) of natural;
	function zeros(count : natural; width : natural) return std_logic_vector;
	function zeros(count : natural) return std_logic_vector;
end package;

package body misc_pkg is
	function zeros(count : natural; width : natural) return std_logic_vector
	is
		constant vec : std_logic_vector(count * width - 1 downto 0) := (others => '0');
	begin
		return vec;
	end function;

	function zeros(count : natural) return std_logic_vector
	is begin
		return zeros(count, 1);
	end function;
end package body;
