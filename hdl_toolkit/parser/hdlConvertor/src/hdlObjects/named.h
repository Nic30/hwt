#pragma once

#include <Python.h>
#include "jsonable.h"

class Named {
public:
	const char * name;
	Named();
	PyObject * toJson() const;
};
