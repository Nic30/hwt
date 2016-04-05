package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class CompInstance implements iJsonable {
	public Expr entityName;
	public String name;
	public List<Expr> genericMap;
	public List<Expr> portMap;

	public CompInstance(Expr _entityName) {
		entityName = _entityName;
		genericMap = new Vector<Expr>();
		portMap = new Vector<Expr>();
	}
	@Override
	public JSONObject toJson() throws JSONException {
		JSONObject o = new JSONObject();
		o.put("name", name);
		o.put("entityName", entityName.toJson());
		return o;
	}

}
