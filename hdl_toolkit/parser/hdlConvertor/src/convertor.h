#pragma once

#include <iostream>
#include <fstream>

#include "hdlObjects/context.h"
#include "antlr4-runtime.h"
#include "VhdlParser/vhdlParser.h"
#include "VhdlParser/vhdlLexer.h"
#include "VerilogParser/Verilog2001Parser.h"
#include "syntaxErrorLogger.h"
#include "langue.h"
#include "vhdlConvertor/designFileParser.h"


using namespace antlr4;
using namespace vhdl;

class Convertor {

public:
	static const char * fileName;
	static Langue lang;
	static bool hierarchyOnly;
	static bool debug;

	static Context * parse(
			const char * fileName,
			Langue lang,
			bool hierarchyOnly,
			bool debug);
	//Context * Convertor::parseString(
	//		const char * _str,
	//		Langue _lang,
	//		bool _hierarchyOnly,
	//		bool _debug);

};

template<class lexerT, class parserT>
parserT * initParser(ANTLRInputStream * input) {
	// create a lexer that feeds off of input CharStream
	lexerT * lexer = new vhdlLexer(input);
	// create a buffer of tokens pulled from the lexer

	//CommonTokenStream tokens;
	CommonTokenStream * tokens = new CommonTokenStream(lexer);
	// create a parser that feeds off the tokens buffer
	parserT * parser = new parserT(tokens);

	parser->removeErrorListeners();
	parser->addErrorListener(new SyntaxErrorLogger());
}
