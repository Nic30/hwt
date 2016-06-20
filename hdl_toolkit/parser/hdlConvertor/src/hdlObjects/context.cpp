#include "context.h"

PyObject * Context::toJson() const {
	PyObject * c = PyDict_New();
	addJsonArr(c, "imports", imports);
	addJsonArr(c, "entities", entities);
	addJsonArr(c, "architectures", architectures);
	addJsonArr(c, "packages", packages);
	addJsonArr(c, "packageHeaders", packageHeaders);
	return c;
}

