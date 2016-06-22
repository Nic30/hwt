#pragma once

#include <Python.h>
#include <vector>
#include <iostream>

#define INDENT_INCR 2

PyObject * addJsonArr_empty(PyObject * parent, const char * name);

template<typename T>
void addJsonArr(
		PyObject * parent,
		const char * name,
		std::vector<T> const & objects) {
	PyObject * objList = PyList_New(objects.size());

	for (auto it : objects) {
		PyObject * o = it.toJson();
		PyList_Append(objList, o);
	}
	Py_INCREF(objList);
	PyDict_SetItem(parent, PyUnicode_FromString(name), objList);
}

template<typename T>
void addJsonArrP(
		PyObject * parent,
		const char * name,
		std::vector<T> const & objects) {
	PyObject * objList = PyList_New(objects.size());

	for (auto i : objects) {
		PyObject * o = i->toJson();
		assert(o);
		Py_IncRef(o);
		PyList_Append(objList, o);
	}
	Py_INCREF(objList);
	PyDict_SetItem(parent, PyUnicode_FromString(name), objList);
}

inline std::ostream& mkIndent(int indent) {
	for (int i = 0; i < indent; i++) {
		std::cout << ' ';
	}
	return std::cout;
}

template<typename T>
std::ostream & dumpArrP(
		const char * name,
		int indent,
		std::vector<T> const & objects) {
	std::cout << "\"" << name << "\":[";
	indent += INDENT_INCR;
	for (auto it : objects) {
		it->dump(indent);
		std::cout << ",\n";
	}
	mkIndent(indent - INDENT_INCR);
	std::cout << "]";
	return std::cout;
}

template<typename T>
std::ostream & dumpItemP(const char * name, int indent, T const & object) {
	mkIndent(indent) << "\"" << name << "\":";
	object->dump(indent);
	return std::cout;
}
inline std::ostream & dumpKey(const char * key, int indent) {
	return mkIndent(indent) << "\"" << key << "\":";
}
template<typename T>
std::ostream & dumpVal(const char * key, int indent, T val) {
	return dumpKey(key, indent) << "\"" << val << "\"";
}

