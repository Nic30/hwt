package hdlObjects;

import java.math.BigInteger;
import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Expr implements iJsonable {
	public Symbol literal;
	public Operator binOperator;
	Expr() {
	}

	public Expr(Expr op0, OperatorType operatorType, Expr op1) {
		this.binOperator = new Operator(op0, operatorType, op1);
	}
	public Expr(SymbolType type, Object value) {
		literal = new Symbol(type, value);
	}
	public Expr(BigInteger value, int bits) {
		literal = new Symbol(value, bits);
	}
	public static Expr ternary(Expr cond, Expr ifTrue, Expr ifFalse) {
		Expr e = new Expr();
		List<Expr> ops = new Vector<Expr>();
		ops.add(ifTrue);
		ops.add(ifFalse);
		e.binOperator = new Operator(cond, OperatorType.TERNARY, ops);
		return e;
	}
	public static Expr call(Expr fnId, List<Expr> operands) {
		Expr e = new Expr();
		e.binOperator = new Operator(fnId, OperatorType.CALL, operands);
		return e;
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
