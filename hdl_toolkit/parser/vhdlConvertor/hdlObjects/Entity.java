package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Entity extends Jsonable {
	public String name;
	public List<Variable> generics;
	public List<Port> ports;
	public Entity() {
		generics = new Vector<Variable>();
		ports = new Vector<Port>();
	}
	public JSONObject toJson() throws JSONException {

		JSONObject e = new JSONObject();
		e.put("name", name);

		addJsonArr(e, "generics", generics);
		addJsonArr(e, "ports", ports);

		return e;
	}
}
