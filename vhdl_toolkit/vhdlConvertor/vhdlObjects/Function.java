package vhdlObjects;

import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;

public class Function extends Jsonable {
	String name;
	boolean isOperator;
	Expr returnT;
	List<Variable> params;
	// [TODO] body

	public Function(String name, boolean isOperator, Expr returnT,
			List<Variable> params) {
		this.name = name;
		this.isOperator = isOperator;
		this.returnT = returnT;
		this.params = params;
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

		return f;
	}
}
