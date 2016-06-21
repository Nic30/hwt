#include "entity.h"

Entity::Entity() :
		Named() {
	//generics = new std::vector<Variable>();
	//ports = new std::vector<Port>();
}

PyObject * Entity::toJson() const {
	PyObject * d = Named::toJson();
	addJsonArrP(d, "generics", generics);
	addJsonArrP(d, "ports", ports);

	return d;
}
