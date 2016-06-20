#include "convertor_c.h"
#include "convertor.h"

PyObject * convertToPyDict(
		const char * fileName,
		Langue lang,
		bool hierarchyOnly,
		bool debug) {
	Context * c = Convertor::parse(fileName, lang, hierarchyOnly, debug);
	return c->toJson();
}
