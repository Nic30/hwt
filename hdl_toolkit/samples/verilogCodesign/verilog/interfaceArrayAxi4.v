module ternOpInModul # (
   parameter integer C_NUM_SLAVE_SLOTS                = 1, 
   parameter integer C_NUM_MASTER_SLOTS               = 2, 
   parameter integer C_AXI_ID_WIDTH                   = 1, 
   parameter integer C_AXI_ADDR_WIDTH                 = 32, 
   parameter integer C_AXI_DATA_WIDTH                 = 32, 
   parameter integer C_AXI_PROTOCOL                   = 0 
)
(
   // Slave Interface Write Address Ports
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_ID_WIDTH-1:0]              s_axi_awid,
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_ADDR_WIDTH-1:0]            s_axi_awaddr,
	input  wire [C_NUM_SLAVE_SLOTS*((C_AXI_PROTOCOL == 1) ? 4 : 8)-1:0] s_axi_awlen,
	input  wire [C_NUM_SLAVE_SLOTS*3-1:0]                               s_axi_awsize,
	input  wire [C_NUM_SLAVE_SLOTS*2-1:0]                               s_axi_awburst,
	input  wire [C_NUM_SLAVE_SLOTS*((C_AXI_PROTOCOL == 1) ? 2 : 1)-1:0] s_axi_awlock,
	input  wire [C_NUM_SLAVE_SLOTS*4-1:0]                          s_axi_awcache,
	input  wire [C_NUM_SLAVE_SLOTS*3-1:0]                          s_axi_awprot,
	input  wire [C_NUM_SLAVE_SLOTS*4-1:0]                          s_axi_awqos,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_awvalid,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_awready,
	// Slave Interface Write Data Ports
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_ID_WIDTH-1:0]             s_axi_wid,
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_DATA_WIDTH-1:0]           s_axi_wdata,
	input  wire [C_NUM_SLAVE_SLOTS*(C_AXI_DATA_WIDTH/8)-1:0]       s_axi_wstrb,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_wlast,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_wvalid,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_wready,
	// Slave Interface Write Response Ports
	output wire [C_NUM_SLAVE_SLOTS*C_AXI_ID_WIDTH-1:0]             s_axi_bid,
	output wire [C_NUM_SLAVE_SLOTS*2-1:0]                          s_axi_bresp,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_bvalid,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_bready,
	// Slave Interface Read Address Ports
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_ID_WIDTH-1:0]             s_axi_arid,
	input  wire [C_NUM_SLAVE_SLOTS*C_AXI_ADDR_WIDTH-1:0]           s_axi_araddr,
	input  wire [C_NUM_SLAVE_SLOTS*((C_AXI_PROTOCOL == 1) ? 4 : 8)-1:0] s_axi_arlen,
	input  wire [C_NUM_SLAVE_SLOTS*3-1:0]                          s_axi_arsize,
	input  wire [C_NUM_SLAVE_SLOTS*2-1:0]                          s_axi_arburst,
	input  wire [C_NUM_SLAVE_SLOTS*((C_AXI_PROTOCOL == 1) ? 2 : 1)-1:0] s_axi_arlock,
	input  wire [C_NUM_SLAVE_SLOTS*4-1:0]                          s_axi_arcache,
	input  wire [C_NUM_SLAVE_SLOTS*3-1:0]                          s_axi_arprot,
	input  wire [C_NUM_SLAVE_SLOTS*4-1:0]                          s_axi_arqos,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_arvalid,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_arready,
	// Slave Interface Read Data Ports
	output wire [C_NUM_SLAVE_SLOTS*C_AXI_ID_WIDTH-1:0]             s_axi_rid,
	output wire [C_NUM_SLAVE_SLOTS*C_AXI_DATA_WIDTH-1:0]           s_axi_rdata,
	output wire [C_NUM_SLAVE_SLOTS*2-1:0]                          s_axi_rresp,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_rlast,
	output wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_rvalid,
	input  wire [C_NUM_SLAVE_SLOTS-1:0]                            s_axi_rready,
	
	
	
	
	
	  // Master Interface Write Address Port
   output wire [C_NUM_MASTER_SLOTS*C_AXI_ID_WIDTH-1:0]            m_axi_awid,
   output wire [C_NUM_MASTER_SLOTS*C_AXI_ADDR_WIDTH-1:0]          m_axi_awaddr,
   output wire [C_NUM_MASTER_SLOTS*((C_AXI_PROTOCOL == 1) ? 4 : 8)-1:0] m_axi_awlen,
   output wire [C_NUM_MASTER_SLOTS*3-1:0]                         m_axi_awsize,
   output wire [C_NUM_MASTER_SLOTS*2-1:0]                         m_axi_awburst,
   output wire [C_NUM_MASTER_SLOTS*((C_AXI_PROTOCOL == 1) ? 2 : 1)-1:0] m_axi_awlock,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_awcache,
   output wire [C_NUM_MASTER_SLOTS*3-1:0]                         m_axi_awprot,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_awregion,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_awqos,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_awvalid,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_awready,
   // Master Interface Write Data Ports
   output wire [C_NUM_MASTER_SLOTS*C_AXI_ID_WIDTH-1:0]            m_axi_wid,
   output wire [C_NUM_MASTER_SLOTS*C_AXI_DATA_WIDTH-1:0]          m_axi_wdata,
   output wire [C_NUM_MASTER_SLOTS*(C_AXI_DATA_WIDTH/8)-1:0]        m_axi_wstrb,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_wlast,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_wvalid,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_wready,
   // Master Interface Write Response Ports
   input  wire [C_NUM_MASTER_SLOTS*C_AXI_ID_WIDTH-1:0]            m_axi_bid,
   input  wire [C_NUM_MASTER_SLOTS*2-1:0]                         m_axi_bresp,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_bvalid,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_bready,
   // Master Interface Read Address Port
   output wire [C_NUM_MASTER_SLOTS*C_AXI_ID_WIDTH-1:0]            m_axi_arid,
   output wire [C_NUM_MASTER_SLOTS*C_AXI_ADDR_WIDTH-1:0]          m_axi_araddr,
   output wire [C_NUM_MASTER_SLOTS*((C_AXI_PROTOCOL == 1) ? 4 : 8)-1:0] m_axi_arlen,
   output wire [C_NUM_MASTER_SLOTS*3-1:0]                         m_axi_arsize,
   output wire [C_NUM_MASTER_SLOTS*2-1:0]                         m_axi_arburst,
   output wire [C_NUM_MASTER_SLOTS*((C_AXI_PROTOCOL == 1) ? 2 : 1)-1:0] m_axi_arlock,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_arcache,
   output wire [C_NUM_MASTER_SLOTS*3-1:0]                         m_axi_arprot,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_arregion,
   output wire [C_NUM_MASTER_SLOTS*4-1:0]                         m_axi_arqos,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_arvalid,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_arready,
   // Master Interface Read Data Ports
   input  wire [C_NUM_MASTER_SLOTS*C_AXI_ID_WIDTH-1:0]            m_axi_rid,
   input  wire [C_NUM_MASTER_SLOTS*C_AXI_DATA_WIDTH-1:0]          m_axi_rdata,
   input  wire [C_NUM_MASTER_SLOTS*2-1:0]                         m_axi_rresp,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_rlast,
   input  wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_rvalid,
   output wire [C_NUM_MASTER_SLOTS-1:0]                           m_axi_rready
);

endmodule
