package hdlObjects;

public enum SymbolType {
	ID, INT, FLOAT, STRING, OPEN, ALL, NULL;
	public static String asString(SymbolType t) {
		switch (t) {
			case ID :
				return "ID";
			case INT :
				return "INT";
			case FLOAT :
				return "FLOAT";
			case STRING :
				return "STRING";
			case OPEN :
				return "OPEN";
			case ALL :
				return "ALL";
			default :
				return "NULL";
		}
	}
}
