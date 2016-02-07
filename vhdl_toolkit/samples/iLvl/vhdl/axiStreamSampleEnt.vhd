library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity AxiStreamSampleEnt is
generic (
	C_DATA_WIDTH       : positive := 32;
	C_USER_WIDTH       : positive := 2
);
port (
	RX0_ETH_TDATA  : in  std_logic_vector(C_DATA_WIDTH - 1 downto 0);
	RX0_ETH_TKEEP  : in  std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0);
	RX0_ETH_TUSER  : in  std_logic_vector(C_USER_WIDTH - 1 downto 0);
	RX0_ETH_TLAST  : in  std_logic;
	RX0_ETH_TVALID : in  std_logic;
	RX0_ETH_TREADY : out std_logic;

	RX0_CTL_TDATA  : in  std_logic_vector(31 downto 0);
	RX0_CTL_TLAST  : in  std_logic;
	RX0_CTL_TVALID : in  std_logic;
	RX0_CTL_TREADY : out std_logic;

	TX0_ETH_TDATA  : out std_logic_vector(C_DATA_WIDTH - 1 downto 0);
	TX0_ETH_TKEEP  : out std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0);
	TX0_ETH_TUSER  : out std_logic_vector(C_USER_WIDTH - 1 downto 0);
	TX0_ETH_TLAST  : out std_logic;
	TX0_ETH_TVALID : out std_logic;
	TX0_ETH_TREADY : in  std_logic;

	TX0_CTL_TDATA  : out std_logic_vector(31 downto 0);
	TX0_CTL_TLAST  : out std_logic;
	TX0_CTL_TVALID : out std_logic;
	TX0_CTL_TREADY : in  std_logic
);
end entity;