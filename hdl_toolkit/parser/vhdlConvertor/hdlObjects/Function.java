package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Function extends Jsonable {
	String name;
	boolean isOperator;
	Expr returnT;
	List<Variable> params;
	public List<Variable> locals;
	public List<Statement> body;

	public Function(String name, boolean isOperator, Expr returnT,
			List<Variable> params) {
		this.name = name;
		this.isOperator = isOperator;
		this.returnT = returnT;
		this.params = params;
		locals = new Vector<Variable>();
		body = new Vector<Statement>();
	}

	@Override
	public Object toJson() throws JSONException {
		JSONObject f = new JSONObject();
		f.put("name", name);
		f.put("isOperator", isOperator);
		if (returnT != null)
			f.put("returnT", returnT.toJson());
		else
			f.put("returnT", JSONObject.NULL);
		addJsonArr(f, "params", params);
		addJsonArr(f, "locals", locals);
		addJsonArr(f, "body", body);

		return f;
	}
}
