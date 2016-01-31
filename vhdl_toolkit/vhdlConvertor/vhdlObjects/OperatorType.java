package vhdlObjects;

import vhdlParser.vhdlParser;

public enum OperatorType {
	RANGE, INDEX, DOWNTO, TO, UNMINUS, MINUS, PLUS, DIV, MUL, MOD, REM, AMPERSAND, DOUBLESTAR, ABS, NOT, AND, OR, NAND, NOR, XOR, XNOR, EQ, NEQ, LOWERTHAN, LE, GREATERTHAN, GE, SLL, SRL, SLA, SRA, ROL, ROR, DOT, CALL, ARROW;
	public String toString() {
		switch (this) {
			case RANGE :
				return "RANGE";
			case INDEX :
				return "INDEX";
			case DOWNTO :
				return "DOWNTO";
			case TO :
				return "TO";
			case UNMINUS :
				return "UNMINUS";
			case MINUS :
				return "MINUS";
			case PLUS :
				return "PLUS";
			case DIV :
				return "DIV";
			case MUL :
				return "MUL";
			case MOD :
				return "MOD";
			case REM :
				return "REM";
			case AMPERSAND :
				return "AMPERSAND";
			case DOUBLESTAR :
				return "DOUBLESTAR";
			case ABS :
				return "ABS";
			case NOT :
				return "NOT";
			case AND :
				return "AND";
			case OR :
				return "OR";
			case NAND :
				return "NAND";
			case NOR :
				return "NOR";
			case XOR :
				return "XOR";
			case XNOR :
				return "XNOR";
			case EQ :
				return "EQ";
			case NEQ :
				return "NEQ";
			case LOWERTHAN :
				return "LOWERTHAN";
			case LE :
				return "LE";
			case GREATERTHAN :
				return "GREATERTHAN";
			case GE :
				return "GE";
			case SLL :
				return "SLL";
			case SRL :
				return "SRL";
			case SLA :
				return "SLA";
			case SRA :
				return "SRA";
			case ROL :
				return "ROL";
			case ROR :
				return "ROR";
			case DOT :
				return "DOT";
			case CALL :
				return "CALL";
			default :
				assert (this == ARROW);
				return "ARROW";

		}
	}
	public int arity() {
		switch (this) {
			case CALL :
				return -1;
			case NOT :
			case UNMINUS :
			case ABS :
			case RANGE :
				return 1;
			default :
				return 2;
		}
	}
	public static OperatorType from(vhdlParser.Shift_operatorContext op) {
		// shift_operator
		// : SLL
		// | SRL
		// | SLA
		// | SRA
		// | ROL
		// | ROR
		// ;
		if (op.SLL() != null)
			return SLL;
		if (op.SRL() != null)
			return SRL;
		if (op.SLA() != null)
			return SLA;
		if (op.SRA() != null)
			return SRA;
		if (op.ROL() != null)
			return ROL;
		assert (op.ROR() != null);
		return ROR;

	}
	public static OperatorType from(vhdlParser.Relational_operatorContext op) {
		// relational_operator
		// : EQ
		// | NEQ
		// | LOWERTHAN
		// | LE
		// | GREATERTHAN
		// | GE
		// ;
		if (op.EQ() != null)
			return EQ;
		if (op.NEQ() != null)
			return NEQ;
		if (op.LOWERTHAN() != null)
			return LOWERTHAN;
		if (op.LE() != null)
			return LE;
		if (op.GREATERTHAN() != null)
			return GREATERTHAN;
		assert (op.GE() != null);
		return GE;
	}
	public static OperatorType from(vhdlParser.Logical_operatorContext op) {
		// logical_operator
		// : AND
		// | OR
		// | NAND
		// | NOR
		// | XOR
		// | XNOR
		// ;
		if (op.AND() != null)
			return AND;
		if (op.OR() != null)
			return OR;
		if (op.NAND() != null)
			return NAND;
		if (op.NOR() != null)
			return NOR;
		if (op.XOR() != null)
			return XOR;
		assert (op.XNOR() != null);
		return XNOR;

	}
}
