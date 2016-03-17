library ieee;
use ieee.std_logic_1164.all;

entity Axi_basic_slave is
	generic(
		DATA_WIDTH : integer := 13
	);
	port(
		data_vld  : in std_logic;
		data_data : in std_logic_vector(DATA_WIDTH - 1 downto 0)
	);
end Axi_basic_slave;