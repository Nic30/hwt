#pragma once
#include <Python.h>

typedef PyObject * BigInteger;

inline BigInteger BigInteger_fromStr(const char * str, int base) {
	return PyLong_FromString(str, NULL, base);
}
