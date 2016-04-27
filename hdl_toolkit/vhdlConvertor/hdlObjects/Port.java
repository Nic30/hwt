package hdlObjects;

import org.json.JSONException;
import org.json.JSONObject;

public class Port implements iJsonable {
	public Direction direction;
	public Variable variable;

	public JSONObject toJson() throws JSONException {
		JSONObject v = new JSONObject();
		v.put("direction", direction);
		v.put("variable", variable.toJson());
		return v;
	}
}
