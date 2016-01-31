package vhdlObjects;

import java.util.Vector;

import org.json.JSONArray;
import org.json.JSONException;

public class Reference extends Vector<Expr> implements iJsonable {
	private static final long serialVersionUID = 1L;

	public JSONArray toJson() throws JSONException {
		JSONArray a = new JSONArray();
		for (Expr e : this) {
			a.put(e.toJson());
		}
		return a;
	}

}
