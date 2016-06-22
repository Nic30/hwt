#include "convertor.h"

const char * Convertor::fileName = NULL;
Langue Convertor::lang = VHDL;
bool Convertor::hierarchyOnly = false;
bool Convertor::debug = false;

inline bool file_exists(const char * name) {
	if (FILE *file = fopen(name, "r")) {
		fclose(file);
		return true;
	} else {
		return false;
	}
}

Context * Convertor::parse(
		const char * _fileName,
		Langue _lang,
		bool _hierarchyOnly,
		bool _debug) {
	fileName = _fileName;
	lang = _lang;
	hierarchyOnly = _hierarchyOnly;
	debug = _debug;
	Context * c = NULL;
	// create a CharStream that reads from standard input
	if (!file_exists(fileName))
		return NULL;
	ANTLRFileStream * input = new ANTLRFileStream(fileName);
	//input->ANTLRFileStreamname = fileName;

	if (lang == VHDL) {
		vhdlParser * parser = initParser<vhdlLexer, vhdlParser>(input);
		// begin parsing at init rule
		Ref<vhdlParser::Design_fileContext> tree = parser->design_file();
		DesignFileParser * p = new DesignFileParser(hierarchyOnly);
		p->visitDesign_file(tree);
		c = p->getContext();
		delete p;
		delete parser;

	} else if (lang == VERILOG) {
		//verilogParser * parser = initParser<verilogLexer, verilogParser>(input);
	} else {
	}
	return c;
}

//Context * Convertor::parseString(
//		const char * _str,
//		Langue _lang,
//		bool _hierarchyOnly,
//		bool _debug) {
//
//}
