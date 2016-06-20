#include "aPackage.h"
#include "jsonable.h"

using namespace std;

aPackage::aPackage() :
		Named() {
}

PyObject * aPackage::toJson() const {
	PyObject *d = Named::toJson();
	addJsonArr(d, "components", components);
	addJsonArr(d, "functions", functions);
	return d;
}
