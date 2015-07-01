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

   clk_process :process
   begin
        {{ clk_name }} <= '0';
        wait for clk_period/2;  --for 0.5 ns signal is '0'.
        {{ clk_name }} <= '1';
        wait for clk_period/2;  --for next 0.5 ns signal is '1'.
   end process;
   -- Stimulus process
  stim_proc: process
   begin
	{{ reset_name }} <='{{ reset_active_in }}';        
        wait for clk_period *5;
	{{ reset_name }} <='{{ reset_deactive_in }}';        
{{ process_stim }}
        wait;
  end process;

END;
