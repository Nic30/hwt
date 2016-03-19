package vhdlObjects;

import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;

public class Function extends Jsonable {
	Expr name;
	boolean isOperator;
	Expr returnT;
	List<Variable> params;
	// [TODO] body

	public Function(Expr name, boolean isOperator, Expr returnT,
			List<Variable> params) {
		this.name = name;
		this.isOperator = isOperator;
		this.returnT = returnT;
		this.params = params;
	}

	@Override
	public Object toJson() throws JSONException {
		JSONObject f = new JSONObject();
		f.put("name", name.toJson());
		f.put("isOperator", isOperator);
		f.put("returnT", returnT.toJson());
		addJsonArr(f, "params", params);

		return f;
	}
}
