-- A parameterized, inferable, true dual-port, dual-clock block RAM in VHDL.

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity bram_sp is
	generic(
		DATA_WIDTH : integer := 64;
		ADDR_WIDTH : integer := 9
	);
	port(
		-- Port A
		a_clk  : in  std_logic;
		a_we   : in  std_logic;
		a_en   : in  std_logic;
		a_addr : in  std_logic_vector(ADDR_WIDTH - 1 downto 0);
		a_din  : in  std_logic_vector(DATA_WIDTH - 1 downto 0);
		a_dout : out std_logic_vector(DATA_WIDTH - 1 downto 0)
	);
end bram_sp;

architecture rtl of bram_sp is
	-- Shared memory
	type mem_type is array ((2 ** ADDR_WIDTH) - 1 downto 0) of std_logic_vector(DATA_WIDTH - 1 downto 0);
	shared variable mem : mem_type;
begin

	-- Port A
	process(a_clk)
	begin
		if (a_clk'event and a_clk = '1') then
			if (a_we = '1' and a_en = '1') then
				mem(conv_integer(a_addr)) := a_din;
			end if;
			a_dout <= mem(conv_integer(a_addr));
		end if;
	end process;

end rtl;
