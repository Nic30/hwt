#pragma once

enum Langue {
	VHDL, VERILOG
};

class Convertor {
public:
	Convertor(const char * fileName, Langue lang, bool hierarchyOnly, bool debug);
	 parse();
};
