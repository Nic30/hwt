library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity EntityExample is
	generic(
		-- Width of S_AXI data bus
		C_S_AXI_DATA_WIDTH : integer := 32
	);
	port(
		-- Global Clock Signal
		S_AXI_ACLK  : in std_logic;
		-- Global Reset Signal. This Signal is Active LOW
		-- Write data (issued by master, acceped by Slave) 
		S_AXI_WDATA : in std_logic_vector(C_S_AXI_DATA_WIDTH - 1 downto 0);
		-- Write strobes. This signal indicates which byte lanes hold
		-- valid data. There is one write strobe bit for each eight
		-- bits of the write data bus.    
		S_AXI_WSTRB : in std_logic_vector((C_S_AXI_DATA_WIDTH / 8) - 1 downto 0)
	);
end EntityExample;