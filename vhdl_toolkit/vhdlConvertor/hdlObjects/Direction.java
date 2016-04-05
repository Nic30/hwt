package hdlObjects;

import vhdlParser.vhdlParser;

public enum Direction {
	IN, OUT, INOUT, BUFFER, LINKAGE;
	public String toString() {
		switch (this) {
			case IN :
				return "IN";
			case OUT :
				return "OUT";
			case INOUT :
				return "INOUT";
			case BUFFER :
				return "BUFFER";
			default :
				return "LINKAGE";
		}
	}
	public static Direction fromSignal_mode(vhdlParser.Signal_modeContext sm) {
		if (sm.IN() != null)
			return IN;
		else if (sm.OUT() != null)
			return OUT;
		else if (sm.INOUT() != null)
			return INOUT;
		else if (sm.BUFFER() != null)
			return BUFFER;
		else {
			assert (sm.LINKAGE() != null);
			return LINKAGE;
		}
	}

}
