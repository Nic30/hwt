#include "named.h"

Named::Named() {
	name = NULL;
}

PyObject * Named::toJson() const {
	PyObject *d = PyDict_New();
	PyDict_SetItemString(d, "name", PyUnicode_FromString(name));
	return d;
}
