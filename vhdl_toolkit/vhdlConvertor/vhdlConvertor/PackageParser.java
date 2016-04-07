package vhdlConvertor;

import java.util.List;
import java.util.Vector;

import convertorApp.NotImplementedLogger;
import hdlObjects.Function;
import hdlObjects.Package;
import hdlObjects.Statement;
import hdlObjects.Variable;
import hdlObjects.aPackage;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.Package_bodyContext;
import vhdlParser.vhdlParser.Package_body_declarative_itemContext;
import vhdlParser.vhdlParser.Package_body_declarative_partContext;
import vhdlParser.vhdlParser.Sequential_statementContext;
import vhdlParser.vhdlParser.Subprogram_bodyContext;
import vhdlParser.vhdlParser.Subprogram_declarationContext;
import vhdlParser.vhdlParser.Subprogram_declarative_itemContext;
import vhdlParser.vhdlParser.Subprogram_declarative_partContext;
import vhdlParser.vhdlParser.Subprogram_statement_partContext;
import vhdlParser.vhdlParser.Variable_declarationContext;

public class PackageParser {
	Package p;
	boolean hierarchyOnly;
	public PackageParser(boolean _hierarchyOnly) {
		hierarchyOnly = _hierarchyOnly;
	}
	public Package visitPackage_body(Package_bodyContext ctx) {
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
			Package_body_declarative_partContext ctx) {
		// package_body_declarative_part
		// : ( package_body_declarative_item )*
		// ;
		for (vhdlParser.Package_body_declarative_itemContext i : ctx
				.package_body_declarative_item()) {
			visitPackage_body_declarative_item(i);
		}
	}
	public void visitPackage_body_declarative_item(
			Package_body_declarative_itemContext ctx) {
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
		Subprogram_declarationContext sd = ctx.subprogram_declaration();
		if (sd != null) {
			visitSubprogram_declaration(sd);
			return;
		}

		Subprogram_bodyContext sb = ctx.subprogram_body();
		if (sb != null) {
			p.functions.add(visitSubprogram_body(sb));
			return;
		}

		NotImplementedLogger
				.print("PackageParser.visitPackage_body_declarative_item");
	}
	public static Function visitSubprogram_body(
			vhdlParser.Subprogram_bodyContext ctx) {
		// subprogram_body :
		// subprogram_specification IS
		// subprogram_declarative_part
		// BEGIN
		// subprogram_statement_part
		// END ( subprogram_kind )? ( designator )? SEMI
		// ;
		Function f = PackageHeaderParser
				.visitSubprogram_specification(ctx.subprogram_specification());
		for (Variable v : visitSubprogram_declarative_part(
				ctx.subprogram_declarative_part())) {
			f.locals.add(v);
		}
		for (Statement s : visitSubprogram_statement_part(
				ctx.subprogram_statement_part())) {
			f.body.add(s);
		}
		return f;
	}
	public static List<Variable> visitSubprogram_declarative_part(
			Subprogram_declarative_partContext ctx) {
		// subprogram_declarative_part
		// : ( subprogram_declarative_item )*
		// ;
		List<Variable> vars = new Vector<Variable>();
		for (Subprogram_declarative_itemContext sd : ctx
				.subprogram_declarative_item()) {
			vars.addAll(visitSubprogram_declarative_item(sd));
		}

		return vars;

	}
	public static List<Variable> visitSubprogram_declarative_item(
			Subprogram_declarative_itemContext ctx) {
		// subprogram_declarative_item
		// : subprogram_declaration
		// | subprogram_body
		// | type_declaration
		// | subtype_declaration
		// | constant_declaration
		// | variable_declaration
		// | file_declaration
		// | alias_declaration
		// | attribute_declaration
		// | attribute_specification
		// | use_clause
		// | group_template_declaration
		// | group_declaration
		// ;
		Variable_declarationContext vd = ctx.variable_declaration();
		if (vd != null) {
			return visitVariable_declaration(vd);
		}

		NotImplementedLogger
				.print("PackageParser.visitSubprogram_declarative_item");
		return new Vector<Variable>();
	}

	public static List<Variable> visitVariable_declaration(
			Variable_declarationContext ctx) {
		// variable_declaration :
		// ( SHARED )? VARIABLE identifier_list COLON
		// subtype_indication ( VARASGN expression )? SEMI
		// ;
		if (ctx.SHARED() != null)
			NotImplementedLogger
					.print("PackageParser.visitVariable_declaration - SHARED");

		List<Variable> vl = InterfaceParser.extractVariables(
				ctx.identifier_list(), ctx.subtype_indication(),
				ctx.expression());
		return vl;
	}

	public void visitSubprogram_declaration(Subprogram_declarationContext ctx) {
		// subprogram_declaration
		// : subprogram_specification SEMI
		// ;
		NotImplementedLogger.print("PackageParser.visitSubprogram_declaration");
	}

	public static List<Statement> visitSubprogram_statement_part(
			Subprogram_statement_partContext ctx) {
		// subprogram_statement_part
		// : ( sequential_statement )*
		// ;
		List<Statement> statements = new Vector<Statement>();
		for (Sequential_statementContext s : ctx.sequential_statement()) {
			statements.add(StatementParser.visitSequential_statement(s));
		}
		return statements;
	}

}
