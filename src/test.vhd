--Copyright 1986-2014 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2014.4 (lin64) Build 1067303 Wed Nov 12 17:03:13 MST 2014
--Date        : Fri Apr 10 12:54:17 2015
--Host        : nic30-Precision-M4800 running 64-bit Ubuntu 14.04.2 LTS
--Command     : generate_target design_1_wrapper.bd
--Design      : design_1_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity design_1_wrapper is
  port (
    ap_clk : in STD_LOGIC;
    ap_rst_n : in STD_LOGIC;
    data_input_tdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    data_input_tlast : in STD_LOGIC_VECTOR ( 0 downto 0 );
    data_input_tready : out STD_LOGIC;
    data_input_tstrb : in STD_LOGIC_VECTOR ( 3 downto 0 );
    data_input_tvalid : in STD_LOGIC;
    data_output_tdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    data_output_tlast : out STD_LOGIC_VECTOR ( 0 downto 0 );
    data_output_tready : in STD_LOGIC;
    data_output_tstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    data_output_tvalid : out STD_LOGIC;
    s_axi_sbus_araddr : in STD_LOGIC_VECTOR ( 5 downto 0 );
    s_axi_sbus_arready : out STD_LOGIC;
    s_axi_sbus_arvalid : in STD_LOGIC;
    s_axi_sbus_awaddr : in STD_LOGIC_VECTOR ( 5 downto 0 );
    s_axi_sbus_awready : out STD_LOGIC;
    s_axi_sbus_awvalid : in STD_LOGIC;
    s_axi_sbus_bready : in STD_LOGIC;
    s_axi_sbus_bresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_sbus_bvalid : out STD_LOGIC;
    s_axi_sbus_rdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_sbus_rready : in STD_LOGIC;
    s_axi_sbus_rresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_sbus_rvalid : out STD_LOGIC;
    s_axi_sbus_wdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_sbus_wready : out STD_LOGIC;
    s_axi_sbus_wstrb : in STD_LOGIC_VECTOR ( 3 downto 0 );
    s_axi_sbus_wvalid : in STD_LOGIC
  );
end design_1_wrapper;

architecture STRUCTURE of design_1_wrapper is
  component design_1 is
  port (
    ap_clk : in STD_LOGIC;
    ap_rst_n : in STD_LOGIC;
    s_axi_sbus_awaddr : in STD_LOGIC_VECTOR ( 5 downto 0 );
    s_axi_sbus_awvalid : in STD_LOGIC;
    s_axi_sbus_awready : out STD_LOGIC;
    s_axi_sbus_wdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_sbus_wstrb : in STD_LOGIC_VECTOR ( 3 downto 0 );
    s_axi_sbus_wvalid : in STD_LOGIC;
    s_axi_sbus_wready : out STD_LOGIC;
    s_axi_sbus_bresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_sbus_bvalid : out STD_LOGIC;
    s_axi_sbus_bready : in STD_LOGIC;
    s_axi_sbus_araddr : in STD_LOGIC_VECTOR ( 5 downto 0 );
    s_axi_sbus_arvalid : in STD_LOGIC;
    s_axi_sbus_arready : out STD_LOGIC;
    s_axi_sbus_rdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    s_axi_sbus_rresp : out STD_LOGIC_VECTOR ( 1 downto 0 );
    s_axi_sbus_rvalid : out STD_LOGIC;
    s_axi_sbus_rready : in STD_LOGIC;
    data_output_tvalid : out STD_LOGIC;
    data_output_tready : in STD_LOGIC;
    data_output_tdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    data_output_tlast : out STD_LOGIC_VECTOR ( 0 downto 0 );
    data_output_tstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    data_input_tvalid : in STD_LOGIC;
    data_input_tready : out STD_LOGIC;
    data_input_tdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    data_input_tlast : in STD_LOGIC_VECTOR ( 0 downto 0 );
    data_input_tstrb : in STD_LOGIC_VECTOR ( 3 downto 0 )
  );
  end component design_1;
begin
design_1_i: component design_1
    port map (
      ap_clk => ap_clk,
      ap_rst_n => ap_rst_n,
      data_input_tdata(31 downto 0) => data_input_tdata(31 downto 0),
      data_input_tlast(0) => data_input_tlast(0),
      data_input_tready => data_input_tready,
      data_input_tstrb(3 downto 0) => data_input_tstrb(3 downto 0),
      data_input_tvalid => data_input_tvalid,
      data_output_tdata(31 downto 0) => data_output_tdata(31 downto 0),
      data_output_tlast(0) => data_output_tlast(0),
      data_output_tready => data_output_tready,
      data_output_tstrb(3 downto 0) => data_output_tstrb(3 downto 0),
      data_output_tvalid => data_output_tvalid,
      s_axi_sbus_araddr(5 downto 0) => s_axi_sbus_araddr(5 downto 0),
      s_axi_sbus_arready => s_axi_sbus_arready,
      s_axi_sbus_arvalid => s_axi_sbus_arvalid,
      s_axi_sbus_awaddr(5 downto 0) => s_axi_sbus_awaddr(5 downto 0),
      s_axi_sbus_awready => s_axi_sbus_awready,
      s_axi_sbus_awvalid => s_axi_sbus_awvalid,
      s_axi_sbus_bready => s_axi_sbus_bready,
      s_axi_sbus_bresp(1 downto 0) => s_axi_sbus_bresp(1 downto 0),
      s_axi_sbus_bvalid => s_axi_sbus_bvalid,
      s_axi_sbus_rdata(31 downto 0) => s_axi_sbus_rdata(31 downto 0),
      s_axi_sbus_rready => s_axi_sbus_rready,
      s_axi_sbus_rresp(1 downto 0) => s_axi_sbus_rresp(1 downto 0),
      s_axi_sbus_rvalid => s_axi_sbus_rvalid,
      s_axi_sbus_wdata(31 downto 0) => s_axi_sbus_wdata(31 downto 0),
      s_axi_sbus_wready => s_axi_sbus_wready,
      s_axi_sbus_wstrb(3 downto 0) => s_axi_sbus_wstrb(3 downto 0),
      s_axi_sbus_wvalid => s_axi_sbus_wvalid
    );
end STRUCTURE;
