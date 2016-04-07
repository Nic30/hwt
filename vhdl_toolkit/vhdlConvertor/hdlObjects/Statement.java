package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Statement extends Jsonable {
	StatementType type;
	public List<List<Statement>> ops;
	Expr op0; // expr, cond, return, dst
	Expr op1; // src

	Statement(StatementType type) {
		this.type = type;
		ops = new Vector<List<Statement>>();
	}

	public static Statement EXPR(Expr e) {
		Statement s = new Statement(StatementType.EXPR);
		s.op0 = e;
		return s;
	}
	public static Statement IF(Expr cond, List<Statement> ifTrue) {
		Statement s = new Statement(StatementType.IF);
		s.op0 = cond;
		s.ops.add(ifTrue);

		return s;
	}
	public static Statement IF(Expr cond, List<Statement> ifTrue,
			List<Statement> ifFalse) {
		Statement s = IF(cond, ifTrue);
		s.ops.add(ifFalse);

		return s;
	}
	public static Statement RETURN(Expr val) {
		Statement s = RETURN();
		s.op0 = val;
		return s;
	}
	public static Statement RETURN() {
		return new Statement(StatementType.RETURN);
	}
	public static Statement ASSIG(Expr dst, Expr src) {
		Statement s = new Statement(StatementType.ASSIGMENT);
		List<Statement> v = new Vector<Statement>();
		v.add(Statement.EXPR(dst));
		v.add(Statement.EXPR(src));
		s.ops.add(v);

		return s;
	}
	public static Statement WHILE(Expr cond, List<Statement> body) {
		Statement s = new Statement(StatementType.WHILE);
		List<Statement> c = new Vector<Statement>();
		c.add(Statement.EXPR(cond));

		s.ops.add(c);
		s.ops.add(body);
		return s;

	}

	@Override
	public Object toJson() throws JSONException {
		JSONObject o = new JSONObject();
		o.put("type", type.name());

		switch (type) {
			case EXPR :
				return op0.toJson();
			case IF :
				o.put("cond", op0.toJson());
				addJsonArr(o, "ifTrue", ops.get(0));
				addJsonArr(o, "ifFalse", ops.get(1));
				break;
			case RETURN :
				o.put("val", op0.toJson());
				break;
			case ASSIGMENT :
				o.put("dst", op0.toJson());
				o.put("src", op1.toJson());
				break;
			default :
				throw new JSONException(
						String.format("Invalid StatementType %s", type.name()));
		}

		return o;
	}
}
