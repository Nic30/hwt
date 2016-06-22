#include "hdlConvertorModule.h"
#include "convertor.h"
#include <Python.h>

int main(int argc, char *argv[]) {
	auto c = new Convertor();
	const char * f = "../../samples/iLvl/vhdl/clkRstEnt.vhd";
	Context * ctx = c->parse(f, VHDL, false, true);

	//PyObject* ctxDict = PyObject_Repr(ctx->toJson());
	//const char* s = PyUnicode_AsUTF8(ctxDict);
	if (ctx) {
		ctx->dump(0);
	} else {
		perror("Error");
	}
	delete c;
	delete ctx;
	return 0;
}
