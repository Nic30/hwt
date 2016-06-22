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
	Py_INCREF(d);
	return d;
}

void aPackage::dump(int indent) const {
	Named::dump(indent);
	indent += INDENT_INCR;
	dumpArrP("components", indent, components) << "\n,";
	dumpArrP("functions", indent, functions) << "\n";
	indent -= INDENT_INCR;
	mkIndent(indent) << "}";

}
