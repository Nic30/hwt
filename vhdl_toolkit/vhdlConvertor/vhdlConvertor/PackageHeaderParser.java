package vhdlConvertor;

import vhdlObjects.PackageHeader;
import vhdlParser.vhdlParser;

public class PackageHeaderParser {
	PackageHeader ph;

	public PackageHeader visitPackage_declaration(
			vhdlParser.Package_declarationContext ctx) {
		ph = new PackageHeader();
		// package_declaration
		// : PACKAGE identifier IS
		// package_declarative_part
		// END ( PACKAGE )? ( identifier )? SEMI
		// ;

		ph.name = (String) LiteralParser
				.visitIdentifier(ctx.identifier(0)).literal.value;
		visitPackage_declarative_part(ph, ctx.package_declarative_part());
		return ph;
	}
	void visitPackage_declarative_part(PackageHeader ph,
			vhdlParser.Package_declarative_partContext ctx) {
		// package_declarative_part
		// : ( package_declarative_item )*
		// ;
		NotImplementedLogger.print("PackageHeaderParser.visitPackage_declarative_part");
	}
}
