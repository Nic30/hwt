#include "hdlConvertorModule.h"

int main(int argc, char *argv[]) {
	wchar_t *program = Py_DecodeLocale(argv[0], NULL);
	if (program == NULL) {
		fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
		exit(1);
	}

	/* Add a built-in module, before Py_Initialize */
	PyImport_AppendInittab("hdlConvertor", PyInit_hdlConvertor);

	/* Pass argv[0] to the Python interpreter */
	Py_SetProgramName(program);

	/* Initialize the Python interpreter.  Required. */
	Py_Initialize();

	/* Optionally import the module; alternatively,
	 import can be deferred until the embedded script
	 imports it. */
	PyImport_ImportModule("spam");

	//...

	PyMem_RawFree(program);
	return 0;
}
