package vhdlConvertor;

import java.util.List;

import convertorApp.NotImplementedLogger;
import hdlObjects.Entity;
import hdlObjects.Port;
import hdlObjects.Variable;
import vhdlParser.vhdlParser;

public class EntityParser {
	boolean hierarchyOnly;
	public EntityParser(boolean _hierarchyOnly) {
		hierarchyOnly = _hierarchyOnly;
	}
	public Entity visitEntity_declaration(
			vhdlParser.Entity_declarationContext ctx) {

		// entity_declaration
		// : ENTITY identifier IS entity_header
		// entity_declarative_part
		// ( BEGIN entity_statement_part )?
		// END ( ENTITY )? ( identifier )? SEMI
		// ;
		Entity e = new Entity();
		e.name = ctx.identifier(0).getText();
		// entity_declarative_part
		// : ( entity_declarative_item )*
		// ;
		if (!hierarchyOnly) {
			visitEntity_header(e, ctx.entity_header());
			for (vhdlParser.Entity_declarative_itemContext d : ctx
					.entity_declarative_part().entity_declarative_item()) {
				visitEntity_declarative_item(d);
			}
		}
		return e;
	}

	static void visitEntity_declarative_item(
			vhdlParser.Entity_declarative_itemContext ctx) {
		// entity_declarative_item
		// : subprogram_declaration
		// | subprogram_body
		// | type_declaration
		// | subtype_declaration
		// | constant_declaration
		// | signal_declaration
		// | variable_declaration
		// | file_declaration
		// | alias_declaration
		// | attribute_declaration
		// | attribute_specification
		// | disconnection_specification
		// | step_limit_specification
		// | use_clause
		// | group_template_declaration
		// | group_declaration
		// | nature_declaration
		// | subnature_declaration
		// | quantity_declaration
		// | terminal_declaration
		// ;

		NotImplementedLogger.print("EntityParser.visitEntity_declarative_item");
	}
	public static void visitGeneric_clause(vhdlParser.Generic_clauseContext ctx,
			List<Variable> generics) {
		if (ctx != null) {
			// generic_clause
			// : GENERIC LPAREN generic_list RPAREN SEMI
			// ;
			// generic_list
			// : interface_constant_declaration (SEMI
			// interface_constant_declaration)*
			// ;
			vhdlParser.Generic_listContext gl = ctx.generic_list();
			for (vhdlParser.Interface_constant_declarationContext ic : gl
					.interface_constant_declaration()) {
				List<Variable> vl = InterfaceParser
						.visitInterface_constant_declaration(ic);
				for (Variable v : vl)
					generics.add(v);
			}
		}
	}
	public static void visitPort_clause(vhdlParser.Port_clauseContext ctx,
			List<Port> ports) {
		if (ctx != null) {
			// port_clause
			// : PORT LPAREN port_list RPAREN SEMI
			// ;
			// port_list
			// : interface_port_list
			// ;
			vhdlParser.Port_listContext pl = ctx.port_list();
			vhdlParser.Interface_port_listContext ipl = pl
					.interface_port_list();
			// interface_port_list
			// : interface_port_declaration ( SEMI interface_port_declaration )*
			// ;

			for (vhdlParser.Interface_port_declarationContext ipd : ipl
					.interface_port_declaration()) {
				for (Port p : InterfaceParser
						.visitInterface_port_declaration(ipd))
					ports.add(p);
			}
		}
	}
	static void visitEntity_header(Entity e,
			vhdlParser.Entity_headerContext ctx) {
		// entity_header
		// : ( generic_clause )?
		// ( port_clause )?
		// ;
		//
		vhdlParser.Generic_clauseContext g = ctx.generic_clause();
		visitGeneric_clause(g, e.generics);
		vhdlParser.Port_clauseContext pc = ctx.port_clause();
		visitPort_clause(pc, e.ports);
	}
	void visitEntity_statement_part(
			vhdlParser.Entity_statement_partContext ctx) {
		if (ctx == null)
			return;
		// entity_statement_part
		// : ( entity_statement )*
		// ;
		NotImplementedLogger.print("EntityParser.visitEntity_statement_part");
	}
}
