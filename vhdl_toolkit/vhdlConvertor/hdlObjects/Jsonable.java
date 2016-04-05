package hdlObjects;

import java.util.List;
import java.util.function.Function;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public abstract class Jsonable implements iJsonable {

	static <T extends iJsonable> void addJsonArr(JSONObject parent, String name,
			List<T> objects) throws JSONException {
		JSONArray l = new JSONArray();
		for (T o : objects)
			l.put(o.toJson());
		parent.put(name, l);
	}
	static <T extends iJsonable> void addJsonObj(JSONObject parent, String name,
			List<T> objects, Function<T, String> key) throws JSONException {
		JSONObject container = new JSONObject();
		for (T o : objects)
			container.put(key.apply(o), o.toJson());
		parent.put(name, container);
	}

}
