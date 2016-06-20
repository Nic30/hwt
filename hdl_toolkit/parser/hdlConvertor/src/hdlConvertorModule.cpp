#include "hdlConvertorModule.h"

#include <iostream>

static PyMethodDef hdlConvertorMethods[] =
		{
				{ "parse", (PyCFunction)hdlConvertor_parse,
				METH_VARARGS | METH_KEYWORDS,
						"parse(filename, language, lexErrorHandler=lambda..., hierarchyOnly=False, debug=False)"
								"@param filename: name of file to parse\n"
								"@param language: vhdl|verilog\n"
								"@param syntaxErrorHandler: syntax error callback params (filename, line, row, errDescriptionStr)\n"
								"                       If lexical error occurs this callback is called and then parsing\n"
								"                       process continues. \n"
								"                       Default is "
								"                       def f(filename, line, row, errDescriptionStr):"
								"                            sys.stderr.write(\"LEX_ERROR:%s:%d:%d:%s\"\n"
								"                                     %(filename, line, row, errDescriptionStr))     "
								"@param hierarchyOnly: If this flag is set only only items which are affecting hierarchy\n"
								"              are parsed that means only name and presence of entity, package/packageHeader,\n"
								"              architecture and name and presence of component instances inside "
								"              and all includes. \n"
								"@param debug: If this flag is set internal Error/NotImplemented/Unexpected exceptions"
								"              are printed on stderr\n" }, {
						NULL, NULL, 0, NULL } /* Sentinel */
		};

static struct PyModuleDef hdlConvertor = {
	PyModuleDef_HEAD_INIT,
	"hdlConvertor", /* name of module */
	NULL, //spam_doc, /* module documentation, may be NULL */
	-1, /* size of per-interpreter state of the module,
	 or -1 if the module keeps state in global variables. */
	hdlConvertorMethods };

PyObject *
hdlConvertor_parse(PyObject *self, PyObject *args, PyObject *keywds) {
	const char *filename, *langue;
	bool debug, hierarchyOnly;
	PyObject * syntaxErrorHandler, *_debug, *_hierarchyOnly;

	static char *kwlist[] = { "filename", "language", "syntaxErrorHandler",
			"hierarchyOnly", "debug", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, keywds, "ss|OOO", kwlist, &filename,
			&langue, &syntaxErrorHandler, &_hierarchyOnly, &_debug))
		return NULL;
	hierarchyOnly = PyObject_IsTrue(_hierarchyOnly);
	debug = PyObject_IsTrue(_debug);
	if (debug)
		std::cout << "debug is on";

	return PyLong_FromLong(0);
}

PyMODINIT_FUNC PyInit_hdlConvertor(void)
{
	return PyModule_Create(&hdlConvertor);
}

