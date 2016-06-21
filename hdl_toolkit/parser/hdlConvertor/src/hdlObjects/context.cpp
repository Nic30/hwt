#include "context.h"

PyObject * Context::toJson() const {
	PyObject * c = PyDict_New();
	addJsonArrP(c, "imports", imports);
	addJsonArrP(c, "entities", entities);
	addJsonArrP(c, "architectures", architectures);
	addJsonArrP(c, "packages", packages);
	addJsonArrP(c, "packageHeaders", packageHeaders);
	return c;
}

