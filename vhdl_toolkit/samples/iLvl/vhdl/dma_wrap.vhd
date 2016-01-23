library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.misc_pkg.all;
use work.conf_pkg.all;
use work.conf_pkg_common.all;
use work.rsoc_pkg.all;

entity rsoc_dma is
	generic(
		C_BASE                : string           := "default";
		C_ID                  : array_of_natural := (0 => 0);
		C_CTRL_COUNT          : positive         := 1;
		C_MBUS_MAX_ID_WIDTH   : natural          := 12
	port(
		CTRL_INFO    : out std_logic_vector(zeros(C_CTRL_COUNT, 32)'range)
	);
end entity;

