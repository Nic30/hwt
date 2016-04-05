package verilogConvertor;

import java.util.List;
import java.util.Vector;

import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNodeImpl;

import convertorApp.NotImplementedLogger;
import hdlObjects.Context;
import hdlObjects.Entity;
import hdlObjects.Expr;
import hdlObjects.OperatorType;
import hdlObjects.Port;
import hdlObjects.Variable;
import verilogParser.Verilog2001Parser;
import verilogParser.Verilog2001Parser.Attribute_instanceContext;
import verilogParser.Verilog2001Parser.List_of_port_declarationsContext;
import verilogParser.Verilog2001Parser.List_of_portsContext;
import verilogParser.Verilog2001Parser.Module_itemContext;
import verilogParser.Verilog2001Parser.Module_parameter_port_listContext;
import verilogParser.Verilog2001Parser.Non_port_module_itemContext;
import verilogParser.Verilog2001Parser.Param_assignmentContext;
import verilogParser.Verilog2001Parser.Parameter_declaration_Context;
import verilogParser.Verilog2001Parser.RangeContext;

public class ModuleParser {
	Context context;
	boolean hierarchyOnly;
	Entity ent;
	ModuleParser(Context context, boolean hierarchyOnly) {
		this.context = context;
		this.hierarchyOnly = hierarchyOnly;
	}

	void visitModule_declaration(
			Verilog2001Parser.Module_declarationContext ctx) {
		// module_declaration
		// : attribute_instance* module_keyword module_identifier
		// ( module_parameter_port_list )? ( list_of_ports )? ';' module_item*
		// 'endmodule'
		// | attribute_instance* module_keyword module_identifier
		// ( module_parameter_port_list )? ( list_of_port_declarations )? ';'
		// non_port_module_item*
		// 'endmodule'
		// ;
		ent = new Entity();
		ent.name = ctx.module_identifier().identifier().getText();
		for (Attribute_instanceContext a : ctx.attribute_instance()) {
			for (Variable v : AttributeParser.visitAttribute_instance(a))
				ent.generics.put(v.name, v);
		}
		Module_parameter_port_listContext mppl = ctx
				.module_parameter_port_list();
		if (mppl != null)
			for (Variable v : visitModule_parameter_port_list(mppl))
				ent.generics.put(v.name, v);

		List_of_portsContext lop = ctx.list_of_ports();
		if (lop != null)
			for (Port p : PortParser.visitList_of_ports(lop)) {
				ent.ports.put(p.variable.name, p);
			}

		for (Module_itemContext mi : ctx.module_item())
			visitModule_item(mi);

		List_of_port_declarationsContext lpd = ctx.list_of_port_declarations();
		if (lpd != null)
			for (Port p : PortParser.visitList_of_port_declarations(lpd)) {
				ent.ports.put(p.variable.name, p);
			}

		for (Non_port_module_itemContext npmi : ctx.non_port_module_item())
			visitNon_port_module_item(npmi);

		context.entities.add(ent);
	}

	static List<Variable> visitModule_parameter_port_list(
			Verilog2001Parser.Module_parameter_port_listContext ctx) {
		// module_parameter_port_list : '#' '(' parameter_declaration_ ( ','
		// parameter_declaration_ )* ')' ;
		List<Variable> vars = new Vector<Variable>();
		for (Parameter_declaration_Context pd : ctx.parameter_declaration_()) {
			vars.addAll(visitParameter_declaration_(pd));
		}

		return vars;
	}

	static List<Variable> visitParameter_declaration_(
			Verilog2001Parser.Parameter_declaration_Context ctx) {
		//// split out semi on end. spec grammar is wrong. It won't allow
		//// #(parameter B=8) since it wants a ';' in (...). Rule
		//// module_parameter_port_list calls this one.

		// parameter_declaration_ :
		// 'parameter' ( 'signed' )? ( range )? list_of_param_assignments
		// |'parameter' 'integer' list_of_param_assignments
		// |'parameter' 'real' list_of_param_assignments
		// |'parameter' 'realtime' list_of_param_assignments
		// |'parameter' 'time' list_of_param_assignments
		// ;

		// [TODO] signed

		Expr t = Utils.mkWireT();
		ParseTree typeStr = ctx.getChild(1);
		if (typeStr instanceof TerminalNodeImpl) {
			t = Utils.mkId(typeStr.getText());
		}

		RangeContext r = ctx.range();
		if (r != null) {
			List<Expr> operands = new Vector<Expr>();
			operands.add(ExpressionParser.visitRange(r));
			t = new Expr(t, OperatorType.CALL, operands);
		}

		List<Variable> params = visitList_of_param_assignments(
				ctx.list_of_param_assignments());
		for (Variable v : params)
			v.type = t;
		return params;
	}
	static List<Variable> visitList_of_param_assignments(
			Verilog2001Parser.List_of_param_assignmentsContext ctx) {
		// list_of_param_assignments :
		// param_assignment ( ',' param_assignment )*
		// ;
		List<Variable> params = new Vector<Variable>();
		for (Param_assignmentContext pa : ctx.param_assignment())
			params.add(visitParam_assignment(pa));
		return params;

	}
	static Variable visitParam_assignment(
			Verilog2001Parser.Param_assignmentContext ctx) {
		// param_assignment : parameter_identifier '=' constant_expression ;
		Variable p = new Variable();
		p.name = ctx.parameter_identifier().identifier().getText();
		p.value = ExpressionParser
				.visitConstant_expression(ctx.constant_expression());
		return p;
	}

	void visitModule_item(Verilog2001Parser.Module_itemContext ctx) {
		// module_item :
		// module_or_generate_item
		// | port_declaration ';'
		// | attribute_instance* generated_instantiation
		// | attribute_instance* local_parameter_declaration
		// | attribute_instance* parameter_declaration
		// | attribute_instance* specify_block
		// | attribute_instance* specparam_declaration
		// ;
		NotImplementedLogger.print("ModuleParser.visitModule_item");
	}
	void visitNon_port_module_item(
			Verilog2001Parser.Non_port_module_itemContext ctx) {
		NotImplementedLogger.print("ModuleParser.visitNon_port_module_item");
		// non_port_module_item :
		// attribute_instance* generated_instantiation
		// | attribute_instance* local_parameter_declaration
		// | attribute_instance* module_or_generate_item
		// | attribute_instance* parameter_declaration
		// | attribute_instance* specify_block
		// | attribute_instance* specparam_declaration
		// ;
	}

}
