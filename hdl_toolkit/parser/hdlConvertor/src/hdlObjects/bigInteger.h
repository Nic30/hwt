#pragma once
#include <Python.h>
#include <string>

typedef PyObject * BigInteger;

inline BigInteger BigInteger_fromStr(const char * str, int base) {
	return PyLong_FromString(str, NULL, base);
}
inline BigInteger BigInteger_fromStr(std::string str, int base) {
	return PyLong_FromString(str.c_str(), NULL, base);
}
inline BigInteger BigInteger_fromLong(long long val){
	return PyLong_FromLongLong(val);
}
