#pragma once
#include <Python.h>
#include "langue.h"


PyObject * convertToPyDict(
		const char * _fileName,
	    enum Langue _lang,
		int _hierarchyOnly,
		int _debug);
