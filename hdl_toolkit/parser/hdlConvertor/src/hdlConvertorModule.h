#pragma once

#include <Python.h>

static PyObject *
hdlConvertor_parse(PyObject *self, PyObject *args, PyObject *keywds);
PyMODINIT_FUNC PyInit_hdlConvertor(void);
