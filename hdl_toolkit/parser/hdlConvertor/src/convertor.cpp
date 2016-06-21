#include "convertor.h"

const char * Convertor::fileName = NULL;
Langue Convertor::lang = VHDL;
bool Convertor::hierarchyOnly = false;
bool Convertor::debug = false;

Context * Convertor::parse(
		const char * _fileName,
		Langue _lang,
		bool _hierarchyOnly,
		bool _debug) {
	fileName = _fileName;
	lang = _lang;
	hierarchyOnly = _hierarchyOnly;
	debug = _debug;

	std::wifstream hdlFile(fileName);

	//// create a CharStream that reads from standard input
	ANTLRInputStream * input = new ANTLRInputStream(hdlFile);
	input->name = fileName;

	if (lang == VHDL) {
		vhdlParser * parser = initParser<vhdlLexer, vhdlParser>(input);
		// begin parsing at init rule
		Ref<vhdlParser::Design_fileContext> tree = parser->design_file();
		//DesignFileParser * p = new DesignFileParser(hierarchyOnly);
		//p->visitDesign_file(tree);
		//return p->getContext();
		return NULL;
	} else if (lang == VERILOG) {
		//verilogParser * parser = initParser<verilogLexer, verilogParser>(input);

		return NULL;
	} else {
		return NULL;
	}
}

//Context * Convertor::parseString(
//		const char * _str,
//		Langue _lang,
//		bool _hierarchyOnly,
//		bool _debug) {
//
//}
