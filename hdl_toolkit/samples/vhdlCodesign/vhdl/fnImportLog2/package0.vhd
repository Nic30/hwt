library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

package package0 is
   -- Roundup logarithm with base 2 (first x that 2^x is larger or equal to given number)
   function log2 (n : integer) return integer;
end package0;

package body package0 is
   function log2 (n : integer) return integer is
      variable a, m : integer;
   begin
      if (n = 1) then
         return 0;
      end if;
      a := 0;
      m := 1;
      while m < n loop
         a := a + 1;
         m := m * 2;
      end loop;
      return a;
   end function;
end package0;
