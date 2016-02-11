package vhdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Arch extends Jsonable {
	public String entityName;
	public String name;
	public List<CompInstance> componentInstances;

	public Arch() {
		componentInstances = new Vector<CompInstance>();
	}
	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject o = new JSONObject();
		o.put("name", name);
		o.put("entityName", entityName);
		// comp. inst. name (label) is optional
		addJsonArr(o, "componentInstances", componentInstances);
		return o;
	}

}
