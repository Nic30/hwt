package hdlObjects;

import vhdlParser.vhdlParser;

public enum OperatorType {
	INVALID, RANGE, INDEX, DOWNTO, TO, UN_MINUS, UN_PLUS, SUB, ADD, DIV, MUL, MOD, REM, CONCAT, POW, ABS, NOT, LOG_AND, LOG_OR, AND, OR, NAND, NOR, XOR, XNOR, EQ, NEQ, LOWERTHAN, LE, GREATERTHAN, GE, SLL, SRL, SLA, SRA, ROL, ROR, TERNARY, DOT, CALL, ARROW;
	public String toString() {
		return this.name();
	}
	public int arity() {
		switch (this) {
			case CALL :
				return -1;
			case NOT :
			case UN_MINUS :
			case UN_PLUS :
			case ABS :
			case RANGE :
				return 1;
			case TERNARY :
				return 3;
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
