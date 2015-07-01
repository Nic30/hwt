-- {{ axi_prefix }} responding on read req with data: {{ data }}
    {{ axi_prefix }}ARREADY <= '1';
    if {{ axi_prefix }}ARVALID /= '1' then 
        wait until {{ axi_prefix }}ARVALID = '1';
    end if;
    wait for clk_period;
    {{ axi_prefix }}ARREADY <= '0';

{% for d in data %}
    -- responding data index: {{ loop.index0 }}
    {{ axi_prefix }}RVALID <='1';
    {{ axi_prefix }}RDATA <= std_logic_vector(to_unsigned({{ d }}, {{ axi_prefix }}RDATA'length));
    {% if loop.last %}
         {{ axi_prefix }}RLAST <='1';
    {% else %}
         {{ axi_prefix }}RLAST <='0';
    {% endif %}
    if {{ axi_prefix }}RREADY /= '1' then 
        wait until {{ axi_prefix }}RREADY = '1';
    end if;
    wait for clk_period;
{% endfor %}

{{ axi_prefix }}RVALID <='0';
{{ axi_prefix }}RLAST  <='0';
wait for clk_period;
