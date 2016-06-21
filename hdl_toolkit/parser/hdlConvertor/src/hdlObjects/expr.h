#pragma once

#include <Python.h>
#include <vector>
#include <string>

#include "bigInteger.h"
#include "symbolType.h"
#include "operatorType.h"
#include "exprItem.h"

class Expr {
public:
	ExprItem * data;
	Expr();

	Expr(Expr * op0, OperatorType operatorType, Expr * op1);
	Expr(SymbolType type, LiteralVal value);
	Expr(BigInteger value, int bits);
	Expr(BigInteger value);

	static Expr * id(const char * value);
	static Expr * id(std::string value);
	static Expr * INT(long long val);
	static Expr * INT(std::string strVal, int base = 10);
	static Expr * INT(const char * strVal, int base=10);
	static Expr * FLOAT(double val);
	static Expr * STR(std::string strVal);
	static Expr * OPEN();
	static Expr * ternary(Expr * cond, Expr * ifTrue, Expr * ifFalse);
	static Expr * call(Expr * fnId, std::vector<Expr*> * operands);
	static Expr * all();
	static Expr * null();
	const char * extractStr();
	PyObject * toJson() const;

};
