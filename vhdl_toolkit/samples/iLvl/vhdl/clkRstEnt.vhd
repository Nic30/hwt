library ieee;
use ieee.std_logic_1164.all;

entity arbiter is
	port(
		ACLK    : in std_logic;
		ARESETN : in std_logic
	);
end entity;