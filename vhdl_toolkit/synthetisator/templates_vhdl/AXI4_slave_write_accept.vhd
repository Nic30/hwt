-- {{ axi_prefix }} responding on write req

{{ axi_prefix }}AWREADY <= '1';
if {{ axi_prefix }}AWVALID /= '1' then 
    wait until {{ axi_prefix }}AWVALID = '1';
end if;
wait for clk_period;
{{ axi_prefix }}AWREADY <= '0';

{% for d in data %}	
	-- accepting data index {{ loop.index0 }}
	{{ axi_prefix }}WREADY <='1';
	if {{ axi_prefix }}WVALID /= '1' then 
	    wait until {{ axi_prefix }}WVALID = '1';
	end if;
	{% if loop.last %}
	if {{ axi_prefix }}WLAST /= '1' then 
	    wait until {{ axi_prefix }}WLAST = '1';
	end if;
	{% endif %}
	wait for clk_period;
{% endfor %}
{{ axi_prefix }}WREADY <='0';
	
{{ axi_prefix }}BVALID <= '1';
{{ axi_prefix }}BRESP <= (others => '0'); -- OKAY
if {{ axi_prefix }}BREADY /= '1' then 
    wait until {{ axi_prefix }}BREADY = '1';
end if;
wait for clk_period;
{{ axi_prefix }}BVALID <= '0';
	
wait for clk_period;

