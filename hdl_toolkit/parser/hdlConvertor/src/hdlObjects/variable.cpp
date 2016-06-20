#include "variable.h"

PyObject* Variable::toJson() const {
	PyObject*d = Named::toJson();
	if (!type)
		throw "Variable has no type";

	PyDict_SetItemString(d, "type", type->toJson());

	if (value) {
		PyDict_SetItemString(d, "value", value->toJson());
	} else {
		Py_IncRef(Py_None);
		PyDict_SetItemString(d, "value", Py_None);
	}
	return d;
}
