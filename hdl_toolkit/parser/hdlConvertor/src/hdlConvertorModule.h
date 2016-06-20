#pragma once

#include <string.h>
#include <Python.h>

#include "langue.h"
#include "convertor_c.h"

static PyObject *
hdlConvertor_parse(PyObject *self, PyObject *args, PyObject *keywds);
PyMODINIT_FUNC PyInit_hdlConvertor(void);
