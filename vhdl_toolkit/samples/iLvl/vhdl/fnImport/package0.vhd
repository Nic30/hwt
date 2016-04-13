library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

package package0 is
	function max(l, r : integer) return integer;
end package0;

package body package0 is
	function max(l, r : integer) return integer is
	begin
		if l > r then
			return l;
		else
			return r;
		end if;
	end;
end package0;