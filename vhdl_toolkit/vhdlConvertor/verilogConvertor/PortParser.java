package verilogConvertor;

import java.util.List;
import java.util.Vector;

import org.antlr.v4.runtime.tree.ParseTree;

import convertorApp.NotImplementedLogger;
import hdlObjects.Direction;
import hdlObjects.Expr;
import hdlObjects.Port;
import hdlObjects.Variable;
import verilogParser.Verilog2001Parser;
import verilogParser.Verilog2001Parser.Attribute_instanceContext;
import verilogParser.Verilog2001Parser.Constant_expressionContext;
import verilogParser.Verilog2001Parser.Inout_declarationContext;
import verilogParser.Verilog2001Parser.Input_declarationContext;
import verilogParser.Verilog2001Parser.Net_typeContext;
import verilogParser.Verilog2001Parser.Output_declarationContext;
import verilogParser.Verilog2001Parser.PortContext;
import verilogParser.Verilog2001Parser.Port_declarationContext;
import verilogParser.Verilog2001Parser.Port_identifierContext;
import verilogParser.Verilog2001Parser.Port_referenceContext;
import verilogParser.Verilog2001Parser.RangeContext;
import verilogParser.Verilog2001Parser.Range_expressionContext;

public class PortParser {
	public static List<Port> addTypeSpecToPorts(Direction direction,
			Net_typeContext net_type, boolean signed, RangeContext range,
			List<Port> ports) {
		// [TODO] signed, net_type
		Expr t = Utils.mkWireT(range);

		for (Port p : ports) {
			assert (p.variable.type == null);
			p.variable.type = t;
			p.direction = direction;
		}
		return ports;
	}
	public static List<Port> visitList_of_ports(
			Verilog2001Parser.List_of_portsContext ctx) {
		// list_of_ports : '(' port ( ',' port )* ')' ;
		List<Port> ports = new Vector<Port>();
		for (PortContext p : ctx.port()) {
			ports.addAll(visitPort(p));
		}
		return ports;
	}
	public static List<Port> visitPort(Verilog2001Parser.PortContext ctx) {
		// port: port_expression?
		// | '.' port_identifier '(' ( port_expression )? ')'
		// ;
		Port_identifierContext pi = ctx.port_identifier();
		if (pi != null) {
			NotImplementedLogger
					.print("Source_textParser.visitPort - port identifier");
			return new Vector<Port>();
		} else {
			return visitPort_expression(ctx.port_expression());
		}
	}
	public static List<Port> visitPort_expression(
			Verilog2001Parser.Port_expressionContext ctx) {
		// port_expression :
		// port_reference
		// | '{' port_reference ( ',' port_reference )* '}'
		// ;
		List<Port> ports = new Vector<Port>();
		for (Port_referenceContext pr : ctx.port_reference()) {
			ports.add(visitPort_reference(pr));
		}
		return ports;
	}
	public static Port visitPort_reference(
			Verilog2001Parser.Port_referenceContext ctx) {
		// port_reference :
		// port_identifier
		// | port_identifier '[' constant_expression ']'
		// | port_identifier '[' range_expression ']'
		// ;
		Port p = new Port();
		p.variable = new Variable();
		p.variable.name = ctx.port_identifier().identifier().getText();

		Constant_expressionContext c = ctx.constant_expression();
		if (c != null) {
			p.variable.type = ExpressionParser.visitConstant_expression(c);
		}
		Range_expressionContext r = ctx.range_expression();
		if (r != null)
			p.variable.type = ExpressionParser.visitRange_expression(r);

		// port_identifier : identifier ;
		return p;

	}
	public static List<Port> visitList_of_port_declarations(
			Verilog2001Parser.List_of_port_declarationsContext ctx) {
		// list_of_port_declarations
		// : '(' port_declaration ( ',' port_declaration )* ')'
		// | '(' ')'
		// ;
		List<Port> ports = new Vector<Port>();
		for (Port_declarationContext pd : ctx.port_declaration()) {
			ports.addAll(visitPort_declaration(pd));
		}
		return ports;
	}
	public static List<Port> visitPort_declaration(
			Verilog2001Parser.Port_declarationContext ctx) {
		// port_declaration :
		// attribute_instance* inout_declaration
		// | attribute_instance* input_declaration
		// | attribute_instance* output_declaration
		// ;

		// [TODO] signed, attribs
		List<Attribute_instanceContext> attribs = ctx.attribute_instance();
		if (attribs.size() > 0) {
			NotImplementedLogger.print(
					"ModuleParser.visitPort_declaration - attribs not implemented");
		}

		// inout_declaration : 'inout' ( net_type )? ( 'signed' )? ( range )?
		// list_of_port_identifiers ;
		Inout_declarationContext inout = ctx.inout_declaration();
		if (inout != null)
			return addTypeSpecToPorts(Direction.INOUT, inout.net_type(), false,
					inout.range(), visitList_of_port_identifiers(
							inout.list_of_port_identifiers()));

		// input_declaration : 'input' ( net_type )? ( 'signed' )? ( range )?
		// list_of_port_identifiers ;
		Input_declarationContext input = ctx.input_declaration();
		if (input != null)
			return addTypeSpecToPorts(Direction.IN, input.net_type(), false,
					input.range(), visitList_of_port_identifiers(
							input.list_of_port_identifiers()));

		// output_declaration :
		// 'output' ( net_type )? ( 'signed' )? ( range )?
		// list_of_port_identifiers
		// | 'output' ( 'reg' )? ( 'signed' )? ( range )?
		// list_of_port_identifiers
		// | 'output' 'reg' ( 'signed' )? ( range )?
		// list_of_variable_port_identifiers
		// | 'output' ( output_variable_type )? list_of_port_identifiers
		// | 'output' output_variable_type list_of_variable_port_identifiers
		// ;
		Output_declarationContext output = ctx.output_declaration();
		List<Port> ports;
		if (output.list_of_variable_port_identifiers() != null) {
			ports = visitList_of_variable_port_identifiers(
					output.list_of_variable_port_identifiers());
		} else {
			ports = visitList_of_port_identifiers(
					output.list_of_port_identifiers());
		}

		return addTypeSpecToPorts(Direction.OUT, output.net_type(), false,
				output.range(), ports);
	}
	public static List<Port> visitList_of_port_identifiers(
			Verilog2001Parser.List_of_port_identifiersContext ctx) {
		// list_of_port_identifiers :
		// port_identifier ( ',' port_identifier )*
		// ;
		List<Port> ports = new Vector<Port>();
		for (Port_identifierContext pi : ctx.port_identifier()) {
			ports.add(visitPort_identifier(pi));
		}
		return ports;
	}
	public static Port visitPort_identifier(
			Verilog2001Parser.Port_identifierContext ctx) {
		// port_identifier : identifier ;
		Variable v = new Variable();
		v.name = ctx.identifier().getText();

		Port p = new Port();
		p.variable = v;
		return p;
	}
	public static List<Port> visitList_of_variable_port_identifiers(
			Verilog2001Parser.List_of_variable_port_identifiersContext ctx) {
		// list_of_variable_port_identifiers :
		// port_identifier ( '=' constant_expression )? ( ',' port_identifier (
		// '=' constant_expression )? )* ;
		List<Port> ports = new Vector<Port>();
		Port last = null;
		for (ParseTree n : ctx.children) {
			if (n instanceof Constant_expressionContext) {
				Constant_expressionContext val = (Constant_expressionContext) n;
				last.variable.value = ExpressionParser
						.visitConstant_expression(val);
			} else {
				last = visitPort_identifier((Port_identifierContext) n);
				ports.add(last);
			}
		}
		return ports;
	}
}
