#include "compInstance.h"

CompInstance::CompInstance(const char * name, Expr * _entityName) {
	entityName = _entityName;
	this->name = name;
}
PyObject * CompInstance::toJson() const {
	PyObject * d = PyDict_New();
	PyDict_SetItemString(d, "entityName", entityName->toJson());
	return d;
}
