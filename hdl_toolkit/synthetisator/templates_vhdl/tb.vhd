LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.std_logic_unsigned.all;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
use ieee.numeric_std.all;


ENTITY {{ entity_name }}_tb IS
END {{ entity_name }}_tb;

ARCHITECTURE behavior OF {{ entity_name }}_tb IS
    COMPONENT {{ entity_name }}
    PORT(
{{ entity_port }}
        );
    END COMPONENT;

   {{ entity_signals }}
   constant clk_period : time := 10 ns;
BEGIN
   uut: {{ entity_name }} 
   PORT MAP (
{{ entity_port_map }}
        );      

    {{ body }}

END;
