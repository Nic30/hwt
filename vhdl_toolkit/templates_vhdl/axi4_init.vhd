-- init {{ axi_prefix }}ar 
{{ axi_prefix }}arburst <= (others => '0');
{{ axi_prefix }}arcache <= std_logic_vector(to_unsigned(2, {{ axi_prefix }}arcache'length));
{{ axi_prefix }}arlen  <= (others => '0');
{{ axi_prefix }}arlock <= (others => '0');
{{ axi_prefix }}arprot <= (others => '0');
{{ axi_prefix }}arqos  <= (others => '0');
{{ axi_prefix }}arregion <= (others => '0');
{{ axi_prefix }}arsize <= std_logic_vector(to_unsigned(5, {{ axi_prefix }}arsize'length));

-- init {{ axi_prefix }}aw
{{ axi_prefix }}awburst <= (others => '0');
{{ axi_prefix }}awcache <= std_logic_vector(to_unsigned(5, {{ axi_prefix }}awcache'length));
{{ axi_prefix }}awlen  <= std_logic_vector(to_unsigned(1, {{ axi_prefix }}awlen'length));
{{ axi_prefix }}awlock <= (others => '0');
{{ axi_prefix }}awprot <= (others => '0');
{{ axi_prefix }}awqos  <= (others => '0');
{{ axi_prefix }}awregion <= (others => '0');
{{ axi_prefix }}awsize <=  std_logic_vector(to_unsigned(5, {{ axi_prefix }}awsize'length));

{{ axi_prefix }}bready <= '1';

