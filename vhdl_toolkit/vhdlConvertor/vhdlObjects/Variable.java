package vhdlObjects;

import org.json.JSONException;
import org.json.JSONObject;

public class Variable {
	public String name;
	public Expr type;
	public Expr value;

	public JSONObject toJson() throws JSONException {
		JSONObject v = new JSONObject();
		v.put("name", name);
		if (type == null)
			throw new JSONException(
					String.format("Variable %s has no type", name));
		v.put("type", type.toJson());
		if (value == null)
			v.put("value", JSONObject.NULL);
		else
			v.put("value", value.toJson());
		return v;
	}

}
