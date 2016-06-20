#include "jsonable.h"



PyObject * addJsonArr_empty(PyObject * parent, const char * name) {
	PyObject * objList = PyList_New(1);
	PyDict_SetItem(parent, PyUnicode_FromString(name), objList);
	return objList;
}
