#include "port.h"

PyObject * Port::toJson() const {
	PyObject *d = PyDict_New();
	PyDict_SetItemString(d, "direction",
			PyUnicode_FromString(Direction_toString(direction)));
	PyDict_SetItemString(d, "variable", variable->toJson());
	return d;
}
