#include "notImplementedLogger.h"

void NotImplementedLogger::print(const char * msg) {
	if (Convertor::debug) {
		std::cerr << msg << "\n";
	}
}
