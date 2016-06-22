#include "arch.h"

PyObject * Arch::toJson() const {
	PyObject * o = Named::toJson();
	PyDict_SetItemString(o, "name", PyUnicode_FromString(name));
	PyDict_SetItemString(o, "entityName", PyUnicode_FromString(entityName));
	addJsonArrP(o, "componentInstances", componentInstances);
	Py_INCREF(o);
	return o;
}
