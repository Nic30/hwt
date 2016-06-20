#include "expr.h"
#include "symbol.h"
#include "operator.h"

Expr::Expr() {
	data = NULL;
}

Expr::Expr(Expr op0, OperatorType operatorType, Expr op1) {
	data = new Operator(op0, operatorType, op1);
}
Expr::Expr(SymbolType type, LiteralVal value) {
	data = new Symbol(type, value);
}
Expr::Expr(BigInteger value, int bits) {
	data = new Symbol(value, bits);
}
Expr * Expr::ternary(Expr cond, Expr ifTrue, Expr ifFalse) {
	Expr * e = new Expr();
	e->data = Operator::ternary(cond, ifTrue, ifFalse);
	return e;
}
Expr * Expr::call(Expr fnId, std::vector<Expr> * operands) {
	Expr * e = new Expr();
	e->data = Operator::call(fnId, operands);
	return e;
}
PyObject * Expr::toJson() const {
	PyObject *d = PyDict_New();
	Operator * op = dynamic_cast<Operator*>(data);
	if (op) {
		PyDict_SetItemString(d, "binOperator", op->toJson());
	} else {
		Symbol * literal = dynamic_cast<Symbol*>(data);
		if (literal)
			PyDict_SetItemString(d, "literal", literal->toJson());
		else
			throw "vhdlExpr is improperly initialized";
	}
	return d;
}
