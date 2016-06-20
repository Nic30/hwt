#pragma once

#include "named.h"
#include "expr.h"

class Variable: public Named {
public:
	Expr * type;
	Expr * value;

	PyObject * toJson() const;
};
