#include "symbol.h"

Symbol::Symbol(SymbolType type, LiteralVal value) {
	this->type = type;
	this->value = value;
	bits = -1;
}
Symbol::Symbol(BigInteger value, int bits) {
	type = symb_INT;
	this->value._int = value;
	this->bits = bits;
}
PyObject * Symbol::toJson() const {
	PyObject * d = PyDict_New();

	PyDict_SetItemString(d, "type",
			PyUnicode_FromString(SymbolType_toString(type)));

	PyObject * val;
	switch (type) {
	case symb_ID:
	case symb_STRING:
		val = PyUnicode_FromString(value._str);
		break;
	case symb_FLOAT:
		val = PyFloat_FromDouble(value._float);
		break;
	case symb_INT:
		val = value._int;
		if (bits > 0)
			PyDict_SetItemString(d, "bits", PyLong_FromLong(bits));
		break;
	case symb_OPEN:
	default:
		val = Py_None;
		break;
	}
	PyDict_SetItemString(d, "value", val);
	return d;
}
