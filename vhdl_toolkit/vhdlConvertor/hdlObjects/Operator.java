package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Operator {
	Expr op0;
	OperatorType operator;
	Expr op1;
	List<Expr> operands;
	public Operator(Expr op0, OperatorType operatorType, Expr op1) {
		this.op0 = op0;
		this.operator = operatorType;
		this.op1 = op1;
	}
	public Operator(Expr op0, OperatorType operatorType, List<Expr> operands) {
		assert (operatorType == OperatorType.CALL);
		this.op0 = op0;
		this.operator = operatorType;
		this.operands = operands;

	}
	public JSONObject toJson() throws JSONException {
		JSONObject o = new JSONObject();
		o.put("op0", op0.toJson());
		o.put("operator", operator.toString());
		int arity = operator.arity();
		switch (arity) {
			case -1 :
				List<JSONObject> opList = new Vector<JSONObject>();
				for (Expr e : operands)
					opList.add(e.toJson());
				o.put("operands", opList);
				break;
			case 1 :
				break;
			case 2 :
				o.put("op1", op1.toJson());
				break;
			default :
				System.err.println(
						String.format("Invalid arity of operator %s  (%d)",
								operator.toString(), arity));
		}
		return o;
	}
}
