-- {{ axi_prefix }} write to addr : {{ addr }}
{{ axi_prefix }}awaddr <= std_logic_vector(to_unsigned({{ addr }}, {{ axi_prefix }}awaddr'length));
{{ axi_prefix }}awvalid <= '1';
if {{ axi_prefix }}awready /= '1' then 
    wait until {{ axi_prefix }}awready = '1';
end if;
wait for clk_period;
{{ axi_prefix }}awvalid  <= '0';

{{ axi_prefix }}wdata <= std_logic_vector(to_unsigned({{ data }}, {{ axi_prefix }}wdata'length));
{{ axi_prefix }}wvalid <= '1';
if {{ axi_prefix }}wready /= '1' then 
    wait until {{ axi_prefix }}wready = '1';
end if;
wait for clk_period;
{{ axi_prefix }}wvalid <= '0';
{{ axi_prefix }}bready <= '1';
wait for clk_period;
