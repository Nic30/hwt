package vhdlConvertor;

import convertorApp.NotImplementedLogger;
import hdlObjects.Package;
import hdlObjects.aPackage;
import vhdlParser.vhdlParser;

public class PackageParser {
	Package p;
	boolean hierarchyOnly;
	public PackageParser(boolean _hierarchyOnly) {
		hierarchyOnly = _hierarchyOnly;
	}
	public Package visitPackage_body(vhdlParser.Package_bodyContext ctx) {
		p = new Package();
		// package_body
		// : PACKAGE BODY identifier IS
		// package_body_declarative_part
		// END ( PACKAGE BODY )? ( identifier )? SEMI
		// ;
		p.name = (String) LiteralParser
				.visitIdentifier(ctx.identifier(0)).literal.value;
		if (!hierarchyOnly) {
			visitPackage_body_declarative_part(p,
					ctx.package_body_declarative_part());
		}
		return p;
	}
	public void visitPackage_body_declarative_part(aPackage p,
			vhdlParser.Package_body_declarative_partContext ctx) {
		// package_body_declarative_part
		// : ( package_body_declarative_item )*
		// ;
		for (vhdlParser.Package_body_declarative_itemContext i : ctx
				.package_body_declarative_item()) {
			visitPackage_body_declarative_item(i);
		}
	}
	public void visitPackage_body_declarative_item(
			vhdlParser.Package_body_declarative_itemContext ctx) {
		// package_body_declarative_item
		// : subprogram_declaration
		// | subprogram_body
		// | type_declaration
		// | subtype_declaration
		// | constant_declaration
		// | variable_declaration
		// | file_declaration
		// | alias_declaration
		// | use_clause
		// | group_template_declaration
		// | group_declaration
		// ;
		NotImplementedLogger
				.print("PackageParser.visitPackage_body_declarative_item");
	}
	public void visitSubprogram_declaration(
			vhdlParser.Subprogram_declarationContext ctx) {
		// subprogram_declaration
		// : subprogram_specification SEMI
		// ;
		NotImplementedLogger.print("PackageParser.visitSubprogram_declaration");
	}

}
