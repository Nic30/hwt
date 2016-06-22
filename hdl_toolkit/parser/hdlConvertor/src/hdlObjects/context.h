#pragma once

#include <vector>
#include <iostream>
#include "jsonable.h"
#include "expr.h"
#include "entity.h"
#include "arch.h"
#include "package.h"
#include "packageHeader.h"

class Context {
public:
	std::vector<Expr*> imports;
	std::vector<Entity*> entities;
	std::vector<Arch*> architectures;
	std::vector<Package*> packages;
	std::vector<PackageHeader*> packageHeaders;

	PyObject * toJson() const;
	void dump(int indent) const;
};
