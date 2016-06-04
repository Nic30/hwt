package hdlObjects;

import java.util.List;
import java.util.Vector;

import org.json.JSONException;
import org.json.JSONObject;

public class Context extends Jsonable {
	public List<Expr> imports;
	public List<Entity> entities;
	public List<Arch> architectures;
	public List<Package> packages;
	public List<PackageHeader> packageHeaders;

	public Context() {
		imports = new Vector<Expr>();
		entities = new Vector<Entity>();
		architectures = new Vector<Arch>();
		packages = new Vector<Package>();
		packageHeaders = new Vector<PackageHeader>();
	}

	public JSONObject toJson() throws JSONException {
		JSONObject c = new JSONObject();
		addJsonArr(c, "imports", imports);
		addJsonObj(c, "entities", entities, e -> e.name);
		addJsonArr(c, "architectures", architectures);
		addJsonObj(c, "packages", packages, p -> p.name);
		addJsonObj(c, "packageHeaders", packageHeaders, ph -> ph.name);
		return c;
	}

}
