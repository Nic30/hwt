#pragma once

#include <Python.h>
#include <vector>
#include "named.h"
#include "entity.h"
#include "function.h"

class aPackage: public Named {
public:
	std::vector<Entity*> components;
	std::vector<Function*> functions;

	aPackage();

	PyObject * toJson() const;
};
