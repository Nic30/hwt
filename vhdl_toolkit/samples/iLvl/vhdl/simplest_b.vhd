
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY SimpleUnit_b IS
    PORT (a : IN STD_LOGIC;
        b : OUT STD_LOGIC
    );
END SimpleUnit_b;

ARCHITECTURE rtl OF SimpleUnit_b IS
    
BEGIN
    b <= a;
END ARCHITECTURE rtl;