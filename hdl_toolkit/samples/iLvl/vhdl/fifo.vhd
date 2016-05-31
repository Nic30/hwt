LIBRARY IEEE; 
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
 
entity Fifo is
	Generic (
		constant DATA_WIDTH  : positive := 64;
		constant DEPTH	: positive := 200
	);
	Port ( 
		clk		: in  STD_LOGIC;
		rst_n		: in  STD_LOGIC;

		data_in_en	: in  STD_LOGIC;
		data_in_data     : in  STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0);
		data_in_wait	: out STD_LOGIC;

		data_out_en	: in  STD_LOGIC;
		data_out_data	: out STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0);
		data_out_wait	: out STD_LOGIC
	);
end Fifo;
 
architecture Behavioral of Fifo is
 
begin
 
	-- Memory Pointer Process
	fifo_proc : process (clk)
		type FIFO_Memory is array (0 to DEPTH - 1) of STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0);
		variable Memory : FIFO_Memory;
		
		variable Head : natural range 0 to DEPTH - 1;
		variable Tail : natural range 0 to DEPTH - 1;
		
		variable Looped : boolean;
	begin
		if rising_edge(clk) then
			if rst_n = '0' then
				Head := 0;
				Tail := 0;
				
				Looped := false;
				
				data_in_wait  <= '0';
				data_out_wait <= '1';
			else
				if (data_out_en = '1') then
					if ((Looped = true) or (Head /= Tail)) then
						-- Update data output
						data_out_data <= Memory(Tail);
						
						-- Update Tail pointer as needed
						if (Tail = DEPTH - 1) then
							Tail := 0;
							
							Looped := false;
						else
							Tail := Tail + 1;
						end if;
						
						
					end if;
				end if;
				
				if (data_in_en = '1') then
					if ((Looped = false) or (Head /= Tail)) then
						-- Write Data to Memory
						Memory(Head) := data_in_data;
						
						-- Increment Head pointer as needed
						if (Head = DEPTH - 1) then
							Head := 0;
							
							Looped := true;
						else
							Head := Head + 1;
						end if;
					end if;
				end if;
				
				-- Update Empty and Full flags
				if (Head = Tail) then
					if Looped then
						data_in_wait <= '1';
					else
						data_out_wait <= '1';
					end if;
				else
					data_out_wait	<= '0';
					data_in_wait	<= '0';
				end if;
			end if;
		end if;
	end process;
		
end Behavioral;
