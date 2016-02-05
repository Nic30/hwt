package vhdlConvertor;

import vhdlObjects.Package;
import vhdlObjects.aPackage;
import vhdlParser.vhdlParser;

public class PackageParser {
	Package p;
	public Package visitPackage_body(vhdlParser.Package_bodyContext ctx) {
		p = new Package();
		// package_body
		// : PACKAGE BODY identifier IS
		// package_body_declarative_part
		// END ( PACKAGE BODY )? ( identifier )? SEMI
		// ;
		p.name = (String) LiteralParser
				.visitIdentifier(ctx.identifier(0)).literal.value;
		visitPackage_body_declarative_part(p,
				ctx.package_body_declarative_part());
		return p;
	}
	public static void visitPackage_body_declarative_part(aPackage p,
			vhdlParser.Package_body_declarative_partContext ctx) {
		// package_body_declarative_part
		// : ( package_body_declarative_item )*
		// ;
		NotImplementedLogger.print("PackageParser.visitPackage_body_declarative_part");
	}
}
