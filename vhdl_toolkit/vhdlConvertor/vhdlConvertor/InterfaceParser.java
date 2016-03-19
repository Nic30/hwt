package vhdlConvertor;

import java.util.List;
import java.util.Vector;

import vhdlObjects.Direction;
import vhdlObjects.Expr;
import vhdlObjects.Port;
import vhdlObjects.Variable;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.Interface_constant_declarationContext;
import vhdlParser.vhdlParser.Interface_declarationContext;
import vhdlParser.vhdlParser.Interface_elementContext;
import vhdlParser.vhdlParser.Interface_file_declarationContext;
import vhdlParser.vhdlParser.Interface_listContext;
import vhdlParser.vhdlParser.Interface_quantity_declarationContext;
import vhdlParser.vhdlParser.Interface_signal_declarationContext;
import vhdlParser.vhdlParser.Interface_terminal_declarationContext;
import vhdlParser.vhdlParser.Interface_variable_declarationContext;

public class InterfaceParser {
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
	public static List<Port> visitInterface_port_declaration(
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
	public static List<Variable> visitInterface_constant_declaration(
			vhdlParser.Interface_constant_declarationContext ctx) {
		// interface_constant_declaration
		// : ( CONSTANT )? identifier_list COLON ( IN )? subtype_indication
		// ( VARASGN expression )?
		// ;
		return extractVariables(ctx.identifier_list(), ctx.subtype_indication(),
				ctx.expression());

	}
	public static List<Variable> visitInterface_signal_declaration(
			Interface_signal_declarationContext ctx) {
		// interface_signal_declaration
		// : SIGNAL identifier_list COLON subtype_indication
		// ( BUS )? ( VARASGN expression )?
		// ;
		return new Vector<Variable>();
	}
	public static List<Variable> visitInterface_variable_declaration(
			Interface_variable_declarationContext ctx) {
		// interface_variable_declaration
		// : ( VARIABLE )? identifier_list COLON
		// ( signal_mode )? subtype_indication ( VARASGN expression )?
		// ;
		NotImplementedLogger
				.print("InterfaceParser.visitInterface_variable_declaration");
		return new Vector<Variable>();
	}
	public static List<Variable> visitInterface_file_declaration(
			Interface_file_declarationContext ctx) {
		// interface_file_declaration
		// : FILE identifier_list COLON subtype_indication
		// ;
		NotImplementedLogger
				.print("InterfaceParser.visitInterface_file_declaration");
		return new Vector<Variable>();
	}
	public static List<Variable> visitInterface_terminal_declaration(
			Interface_terminal_declarationContext ctx) {
		// interface_terminal_declaration
		// : TERMINAL identifier_list COLON subnature_indication
		// ;
		NotImplementedLogger
				.print("InterfaceParser.visitInterface_terminal_declaration");
		return new Vector<Variable>();
	}
	public static List<Variable> visitInterface_quantity_declaration(
			Interface_quantity_declarationContext ctx) {
		// interface_quantity_declaration
		// : QUANTITY identifier_list COLON ( IN | OUT )? subtype_indication
		// ( VARASGN expression )?
		// ;
		NotImplementedLogger
				.print("InterfaceParser.visitInterface_quantity_declaration");
		return new Vector<Variable>();
	}
	public static List<Variable> visitInterface_declaration(
			Interface_declarationContext ctx) {
		// interface_declaration
		// : interface_constant_declaration
		// | interface_signal_declaration
		// | interface_variable_declaration
		// | interface_file_declaration
		// | interface_terminal_declaration
		// | interface_quantity_declaration
		// ;
		Interface_constant_declarationContext c = ctx
				.interface_constant_declaration();
		if (c != null) {
			return visitInterface_constant_declaration(c);
		}
		Interface_signal_declarationContext s = ctx
				.interface_signal_declaration();
		if (s != null) {
			return visitInterface_signal_declaration(s);
		}
		Interface_variable_declarationContext v = ctx
				.interface_variable_declaration();
		if (v != null) {
			return visitInterface_variable_declaration(v);
		}
		Interface_file_declarationContext f = ctx.interface_file_declaration();
		if (f != null) {
			return visitInterface_file_declaration(f);
		}
		Interface_terminal_declarationContext t = ctx
				.interface_terminal_declaration();
		if (t != null) {
			return visitInterface_terminal_declaration(t);
		} else {
			Interface_quantity_declarationContext q = ctx
					.interface_quantity_declaration();
			return visitInterface_quantity_declaration(q);
		}
	}
	public static List<Variable> visitInterface_list(
			Interface_listContext ctx) {
		// interface_list
		// : interface_element ( SEMI interface_element )*
		// ;
		List<Variable> elems = new Vector<Variable>();
		for (Interface_elementContext ie : ctx.interface_element()) {
			elems.addAll(visitInterface_element(ie));
		}
		return elems;
	}
	public static List<Variable> visitInterface_element(
			Interface_elementContext ctx) {
		// interface_element
		// : interface_declaration
		// ;
		return visitInterface_declaration(ctx.interface_declaration());
	}
}
