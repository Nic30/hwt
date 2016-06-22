#include "named.h"
#include <assert.h>

Named::Named() {
	name = NULL;
}

PyObject * Named::toJson() const {
	PyObject *d = PyDict_New();
	assert(name != NULL);
	PyDict_SetItemString(d, "name", PyUnicode_FromString(name));
	Py_IncRef(d);
	return d;
}

void Named::dump(int indent) const {
	mkIndent(indent) << "{\n";
	indent += INDENT_INCR;
	mkIndent(indent) << "\"name\":\"" << name << "\",\n" ;
}
