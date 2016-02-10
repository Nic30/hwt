package vhdlObjects;

import java.math.BigInteger;
import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;

public class Expr {
	public Symbol literal;
	public Operator binOperator;
	public Expr(Expr op0, OperatorType operatorType, Expr op1) {
		this.binOperator = new Operator(op0, operatorType, op1);
	}
	public Expr(Expr op0, OperatorType operatorType, List<Expr> operands) {
		assert (operatorType == OperatorType.CALL);
		this.binOperator = new Operator(op0, operatorType, operands);
	}
	public Expr(SymbolType type, Object value) {
		literal = new Symbol(type, value);
	}
	public Expr(BigInteger value, int bits) {
		literal = new Symbol(value, bits);
	}
	public Expr(Reference ref) {
		literal = new Symbol(SymbolType.ID, ref);
	}
	public JSONObject toJson() throws JSONException {
		JSONObject e = new JSONObject();
		if (binOperator != null && literal == null) {
			e.put("binOperator", binOperator.toJson());
		} else if (binOperator == null && literal != null) {
			e.put("literal", literal.toJson());
		} else
			throw new JSONException("vhdlExpr is improperly initialized");
		return e;
	}
}
