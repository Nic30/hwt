package vhdlObjects;

import java.util.HashMap;
import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;

public class Entity implements iJsonable {
	public String name;
	public Map<String, Variable> generics;
	public Map<String, Port> ports;
	public Entity() {
		generics = new HashMap<String, Variable>();
		ports = new HashMap<String, Port>();
	}
	public JSONObject toJson() throws JSONException {

		JSONObject _generics = new JSONObject();
		for (Variable g : generics.values()) {
			_generics.put(g.name, g.toJson());
		}

		JSONObject _ports = new JSONObject();
		for (Port p : ports.values()) {
			_ports.put(p.variable.name, p.toJson());
		}

		JSONObject e = new JSONObject();
		e.put("name", name);
		e.put("generics", _generics);
		e.put("ports", _ports);

		return e;
	}
}
