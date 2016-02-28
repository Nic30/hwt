package vhdlObjects;

import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;

public abstract class aPackage extends Jsonable {
	public String name;
	public List<Entity> components;

	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject p = new JSONObject();
		p.put("name", name);
		addJsonObj(p, "components", components, c -> c.name);
		return p;
	}

}
