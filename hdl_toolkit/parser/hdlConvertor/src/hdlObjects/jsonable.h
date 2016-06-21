#pragma once

#include <Python.h>
#include <vector>

PyObject * addJsonArr_empty(PyObject * parent, const char * name);

template<typename T>
void addJsonArr(
		PyObject * parent,
		const char * name,
		std::vector<T> const & objects) {
	PyObject * objList = PyList_New(objects.size());

	for (auto it = objects.begin(); it < objects.end(); it++) {
		PyObject * o = it->toJson();
		PyList_Append(objList, o);
	}

	PyDict_SetItem(parent, PyUnicode_FromString(name), objList);
}

template<typename T>
void addJsonArrP(
		PyObject * parent,
		const char * name,
		std::vector<T> const & objects) {
	PyObject * objList = PyList_New(objects.size());

	for (auto it = objects.begin(); it < objects.end(); it++) {
		PyObject * o = (*it)->toJson();
		PyList_Append(objList, o);
	}

	PyDict_SetItem(parent, PyUnicode_FromString(name), objList);
}
