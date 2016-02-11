library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ARCHITECTURE rtl OF SimpleSubunit3 IS
	SIGNAL sig_subunit0_a_data  : STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
	SIGNAL sig_subunit0_a_last  : STD_LOGIC;
	SIGNAL sig_subunit0_a_ready : STD_LOGIC;
	SIGNAL sig_subunit0_a_strb  : STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
	SIGNAL sig_subunit0_a_valid : STD_LOGIC;
	SIGNAL sig_subunit0_b_data  : STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
	SIGNAL sig_subunit0_b_last  : STD_LOGIC;
	SIGNAL sig_subunit0_b_ready : STD_LOGIC;
	SIGNAL sig_subunit0_b_strb  : STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
	SIGNAL sig_subunit0_b_valid : STD_LOGIC;

	COMPONENT subunit0 IS
		GENERIC(
			DATA_WIDTH : INTEGER
		);
		PORT(
			a_data  : IN  STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
			a_last  : IN  STD_LOGIC;
			a_ready : OUT STD_LOGIC;
			a_strb  : IN  STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
			a_valid : IN  STD_LOGIC;
			b_data  : OUT STD_LOGIC_VECTOR(64 - 1 DOWNTO 0);
			b_last  : OUT STD_LOGIC;
			b_ready : IN  STD_LOGIC;
			b_strb  : OUT STD_LOGIC_VECTOR(8 - 1 DOWNTO 0);
			b_valid : OUT STD_LOGIC
		);
	END COMPONENT;

BEGIN
	subunit0_140508271342704 : COMPONENT subunit0
		GENERIC MAP(
			DATA_WIDTH => DATA_WIDTH
		)
		PORT MAP(
			a_data  => sig_subunit0_a_data,
			a_last  => sig_subunit0_a_last,
			a_ready => sig_subunit0_a_ready,
			a_strb  => sig_subunit0_a_strb,
			a_valid => sig_subunit0_a_valid,
			b_data  => sig_subunit0_b_data,
			b_last  => sig_subunit0_b_last,
			b_ready => sig_subunit0_b_ready,
			b_strb  => sig_subunit0_b_strb,
			b_valid => sig_subunit0_b_valid
		);

	a0_ready <= sig_subunit0_a_ready;

	b0_data <= sig_subunit0_b_data;

	b0_last <= sig_subunit0_b_last;

	b0_strb <= sig_subunit0_b_strb;

	b0_valid <= sig_subunit0_b_valid;

	sig_subunit0_a_data <= a0_data;

	sig_subunit0_a_last <= a0_last;

	sig_subunit0_a_strb <= a0_strb;

	sig_subunit0_a_valid <= a0_valid;

	sig_subunit0_b_ready <= b0_ready;

END ARCHITECTURE rtl;