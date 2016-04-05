package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Context extends Jsonable {
	public List<Reference> libaries;
	public List<Reference> usings;
	public List<Entity> entities;
	public List<Arch> architectures;
	public List<Package> packages;
	public List<PackageHeader> packageHeaders;

	public Context() {
		libaries = new Vector<Reference>();
		usings = new Vector<Reference>();
		entities = new Vector<Entity>();
		architectures = new Vector<Arch>();
		packages = new Vector<Package>();
		packageHeaders = new Vector<PackageHeader>();
	}

	public JSONObject toJson() throws JSONException {
		JSONObject c = new JSONObject();
		addJsonArr(c, "libaries", libaries);
		addJsonArr(c, "usings", usings);
		addJsonObj(c, "entities", entities, e -> e.name);
		addJsonArr(c, "architectures", architectures);
		addJsonObj(c, "packages", packages, p -> p.name);
		addJsonObj(c, "packageHeaders", packageHeaders, ph -> ph.name);
		return c;
	}

}
