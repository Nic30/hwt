package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public abstract class aPackage extends Jsonable {
	public String name;
	public List<Entity> components;
	public Vector<Function> functions;

	public aPackage() {
		components = new Vector<Entity>();
		functions = new Vector<Function>();
	}

	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject p = new JSONObject();
		p.put("name", name);
		addJsonObj(p, "components", components, c -> c.name);
		addJsonArr(p, "functions", functions);
		return p;
	}

}