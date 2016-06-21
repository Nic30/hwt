#pragma once

#include <Python.h>
#include <vector>

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
	static Expr * ternary(Expr * cond, Expr * ifTrue, Expr * ifFalse);
	static Expr * call(Expr * fnId, std::vector<Expr*> * operands);
	static Expr * all();
	static Expr * null();
	PyObject * toJson() const;

};
