#include "operator.h"

Operator::Operator() {
	operands = NULL;
	op0 = NULL;
	op1 = NULL;
	op = ARROW;
}

Operator::Operator(Expr* op0, OperatorType operatorType, Expr* op1) {
	this->op0 = op0;
	this->op = operatorType;
	this->op1 = op1;
	operands = NULL;
}
Operator * Operator::call(Expr* fn, std::vector<Expr*> * operands) {
	Operator * o = new Operator();
	o->op0 = fn;
	o->op = CALL;
	o->operands = operands;
	return o;
}
Operator * Operator::ternary(Expr* cond, Expr* ifTrue, Expr* ifFalse) {
	Operator * op = new Operator();
	op->op = TERNARY;
	op->op0 = cond;

	std::vector<Expr*> * ops = new std::vector<Expr*>(2);
	ops->push_back(ifTrue);
	ops->push_back(ifFalse);
	op->operands = ops;

	return op;
}
PyObject * Operator::toJson() const {
	PyObject *d = PyDict_New();
	PyDict_SetItemString(d, "op0", op0->toJson());
	PyDict_SetItemString(d, "operator",
			PyUnicode_FromString(OperatorType_toString(op)));

	int arity = OperatorType_arity(op);
	switch (arity) {
	case -1:
	case 3:
		addJsonArrP(d, "operands", *operands);
		break;
	case 1:
		break;
	case 2:
		PyDict_SetItemString(d, "op1", op1->toJson());
		break;
	default:
		throw "Invalid arity of operator";
	}
	return d;
}
