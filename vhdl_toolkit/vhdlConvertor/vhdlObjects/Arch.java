package vhdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Arch extends Jsonable {
	public String entityName;
	public String name;
	public List<CompInstance> components;

	public Arch() {
		components = new Vector<CompInstance>();
	}
	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject o = new JSONObject();
		o.put("name", name);
		o.put("entityName", entityName);
		addJsonObj(o, "components", components, c -> c.name);
		return o;
	}

}
