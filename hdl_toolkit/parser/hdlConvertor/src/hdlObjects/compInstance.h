#pragma once
#include <vector>
#include "named.h"
#include "expr.h"

class CompInstance: Named {
public:
	Expr * entityName;
	const char * name;
	std::vector<Expr> genericMap;
	std::vector<Expr> portMap;

	CompInstance(const char * name, Expr * _entityName);
	PyObject * toJson() const;
};
