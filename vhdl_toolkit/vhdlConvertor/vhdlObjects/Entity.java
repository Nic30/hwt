package vhdlObjects;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;

public class Entity extends Jsonable {
	public String name;
	public Map<String, Variable> generics;
	public Map<String, Port> ports;
	public Entity() {
		generics = new HashMap<String, Variable>();
		ports = new HashMap<String, Port>();
	}
	public JSONObject toJson() throws JSONException {

		JSONObject e = new JSONObject();
		e.put("name", name);

		addJsonObj(e, "generics", new ArrayList<Variable>(generics.values()),
				g -> g.name);
		addJsonObj(e, "ports", new ArrayList<Port>(ports.values()),
				g -> g.variable.name);

		return e;
	}
}
