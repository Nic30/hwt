-- {{ axi_prefix }} read from addr : {{ addr }}
{{ axi_prefix }}araddr <= std_logic_vector(to_unsigned({{ addr }}, {{ axi_prefix }}araddr'length));
if {{ axi_prefix }}arready /= '1' then 
    wait until {{ axi_prefix }}arready = '1';
end if;
wait for clk_period;
{{ axi_prefix }}arvalid <= '1';
{{ axi_prefix }}rready <='1';
if {{ axi_prefix }}rvalid /= '1' then 
    wait until {{ axi_prefix }}rvalid = '1';
end if;
wait for clk_period;
{{ axi_prefix }}arvalid <= '0';
wait for clk_period;
