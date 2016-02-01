package vhdlConvertor;

import java.util.List;
import java.util.Vector;

import vhdlObjects.CompInstance;
import vhdlObjects.Expr;
import vhdlParser.vhdlParser;

public class CompInstanceParser {
	public static CompInstance visitComponent_instantiation_statement(
			vhdlParser.Component_instantiation_statementContext ctx) {
		CompInstance ci = new CompInstance();
		// component_instantiation_statement
		// : label_colon instantiated_unit
		// ( generic_map_aspect )?
		// ( port_map_aspect )? SEMI
		// ;
		ci.name = visitLabel_colon(ctx.label_colon());
		ci.entityName = visitInstantiated_unit(ctx.instantiated_unit());
		vhdlParser.Generic_map_aspectContext gma = ctx.generic_map_aspect();
		if (gma != null) {
			for (Expr gm : visitGeneric_map_aspect(gma)) {
				ci.genericMap.add(gm);
			}
		}
		vhdlParser.Port_map_aspectContext pma = ctx.port_map_aspect();
		if (pma != null) {
			for (Expr pm : visitPort_map_aspect(pma)) {
				ci.portMap.add(pm);
			}
		}

		return ci;
	}
	public static List<Expr> visitPort_map_aspect(
			vhdlParser.Port_map_aspectContext ctx) {
		System.err.println(
				"NotImplemented CompInstanceParser.visitPort_map_aspect");
		return new Vector<Expr>();
	}
	public static String visitLabel_colon(vhdlParser.Label_colonContext ctx) {
		// label_colon
		// : identifier COLON
		// ;
		return (String) LiteralParser
				.visitIdentifier(ctx.identifier()).literal.value;
	}
	public static Expr visitInstantiated_unit(
			vhdlParser.Instantiated_unitContext ctx) {
		// instantiated_unit
		// : ( COMPONENT )? name
		// | ENTITY name ( LPAREN identifier RPAREN )?
		// | CONFIGURATION name
		// ;

		vhdlParser.IdentifierContext id = ctx.identifier();
		if (id != null) {
			System.err.println(
					"NotImplemented CompInstanceParser.visitInstantiated_unit - Identifier");
		}
		return ReferenceParser.visitName(ctx.name());
	}
	public static List<Expr> visitGeneric_map_aspect(
			vhdlParser.Generic_map_aspectContext ctx) {
		System.err.println(
				"NotImplemented CompInstanceParser.visitGeneric_map_aspect");
		return new Vector<Expr>();
	}
}
