package hdlObjects;

import org.json.JSONException;

public interface iJsonable {
	public Object toJson() throws JSONException;
}
