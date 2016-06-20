#include "convertor.h"

Context * Convertor::parse(
		const char * _fileName,
		Langue _lang,
		bool _hierarchyOnly,
		bool _debug) {
	Convertor::fileName = _fileName;
	Convertor::lang = _lang;
	Convertor::hierarchyOnly = _hierarchyOnly;
	Convertor::debug = _debug;

	std::wifstream hdlFile(fileName);

	//// create a CharStream that reads from standard input
	ANTLRInputStream * input = new ANTLRInputStream(hdlFile);
	input->name = fileName;

	if (lang == VHDL) {
		vhdlParser * parser = initParser<vhdlLexer, vhdlParser>(input);
		// begin parsing at init rule
		Ref<vhdlParser::Design_fileContext> tree = parser->design_file();
		DesignFileParser * p = new DesignFileParser(hierarchyOnly);
		p->visitDesign_file(tree);
		return p->getContext();

	} else if (lang == VERILOG) {
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
