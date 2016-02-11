package vhdlConvertor;

import java.util.List;
import java.util.Vector;

import vhdlObjects.Direction;
import vhdlObjects.Entity;
import vhdlObjects.Expr;
import vhdlObjects.Port;
import vhdlObjects.Variable;
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

	// [TODO]
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
	static void visitEntity_header(Entity e,
			vhdlParser.Entity_headerContext ctx) {
		// entity_header
		// : ( generic_clause )?
		// ( port_clause )?
		// ;
		//

		vhdlParser.Generic_clauseContext g = ctx.generic_clause();
		if (g != null) {
			// generic_clause
			// : GENERIC LPAREN generic_list RPAREN SEMI
			// ;
			// generic_list
			// : interface_constant_declaration (SEMI
			// interface_constant_declaration)*
			// ;
			vhdlParser.Generic_listContext gl = g.generic_list();
			for (vhdlParser.Interface_constant_declarationContext ic : gl
					.interface_constant_declaration()) {
				List<Variable> vl = visitInterface_constant_declaration(ic);
				for (Variable v : vl)
					e.generics.put(v.name, v);
			}
		}
		vhdlParser.Port_clauseContext pc = ctx.port_clause();
		if (pc != null) {
			// port_clause
			// : PORT LPAREN port_list RPAREN SEMI
			// ;
			// port_list
			// : interface_port_list
			// ;
			vhdlParser.Port_listContext pl = pc.port_list();
			vhdlParser.Interface_port_listContext ipl = pl
					.interface_port_list();
			// interface_port_list
			// : interface_port_declaration ( SEMI interface_port_declaration )*
			// ;

			for (vhdlParser.Interface_port_declarationContext ipd : ipl
					.interface_port_declaration()) {
				for (Port p : visitInterface_port_declaration(ipd))
					e.ports.put(p.variable.name, p);
			}
		}

	}
	static List<Variable> visitInterface_constant_declaration(
			vhdlParser.Interface_constant_declarationContext ctx) {
		// interface_constant_declaration
		// : ( CONSTANT )? identifier_list COLON ( IN )? subtype_indication
		// ( VARASGN expression )?
		// ;
		return extractVariables(ctx.identifier_list(), ctx.subtype_indication(),
				ctx.expression());

	}
	static List<Variable> extractVariables(
			vhdlParser.Identifier_listContext identifier_list,
			vhdlParser.Subtype_indicationContext subType,
			vhdlParser.ExpressionContext _expr) {
		List<Variable> vl = new Vector<Variable>();
		Expr type = ExprParser.visitSubtype_indication(subType);
		Expr expr = null;
		if (_expr != null)
			expr = ExprParser.visitExpression(_expr);
		for (vhdlParser.IdentifierContext i : identifier_list.identifier()) {
			// identifier_list
			// : identifier ( COMMA identifier )*
			// ;
			Variable v = new Variable();
			v.name = i.getText();
			v.type = type;
			v.value = expr;
			vl.add(v);
		}
		return vl;
	}
	static List<Port> visitInterface_port_declaration(
			vhdlParser.Interface_port_declarationContext ctx) {
		List<Port> pl = new Vector<Port>();
		// interface_port_declaration
		// : identifier_list COLON signal_mode subtype_indication
		// ( BUS )? ( VARASGN expression )?
		// ;
		List<Variable> vl = extractVariables(ctx.identifier_list(),
				ctx.subtype_indication(), ctx.expression());
		// signal_mode
		// : IN
		// | OUT
		// | INOUT
		// | BUFFER
		// | LINKAGE
		// ;
		Direction d = Direction.fromSignal_mode(ctx.signal_mode());
		for (Variable v : vl) {
			Port p = new Port();
			p.direction = d;
			p.variable = v;
			pl.add(p);
		}
		return pl;
	}

	// [TODO]
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
