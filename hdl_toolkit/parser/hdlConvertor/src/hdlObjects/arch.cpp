#include "arch.h"

PyObject * Arch::toJson() const {
	PyObject * o = Named::toJson();
	PyDict_SetItemString(o, "name", PyUnicode_FromString(name));
	PyDict_SetItemString(o, "entityName", PyUnicode_FromString(entityName));
	addJsonArr(o, "componentInstances", componentInstances);
	return o;
}
