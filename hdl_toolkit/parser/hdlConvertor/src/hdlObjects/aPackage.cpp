#include "aPackage.h"
#include "jsonable.h"

using namespace std;

aPackage::aPackage() :
		Named() {
}

PyObject * aPackage::toJson() const {
	PyObject *d = Named::toJson();
	addJsonArrP(d, "components", components);
	addJsonArrP(d, "functions", functions);
	return d;
}
