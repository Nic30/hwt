package vhdlObjects;

import org.json.JSONException;
import org.json.JSONObject;

public abstract class aPackage extends Jsonable {
	public String name;

	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject p = new JSONObject();
		p.put("name", name);

		return p;
	}

}
