package vhdlConvertor;

import java.util.List;

import vhdlObjects.Entity;
import vhdlObjects.Expr;
import vhdlObjects.Function;
import vhdlObjects.PackageHeader;
import vhdlObjects.Variable;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.Alias_declarationContext;
import vhdlParser.vhdlParser.Attribute_declarationContext;
import vhdlParser.vhdlParser.Attribute_specificationContext;
import vhdlParser.vhdlParser.Component_declarationContext;
import vhdlParser.vhdlParser.Constant_declarationContext;
import vhdlParser.vhdlParser.DesignatorContext;
import vhdlParser.vhdlParser.Disconnection_specificationContext;
import vhdlParser.vhdlParser.File_declarationContext;
import vhdlParser.vhdlParser.Formal_parameter_listContext;
import vhdlParser.vhdlParser.Function_specificationContext;
import vhdlParser.vhdlParser.Group_declarationContext;
import vhdlParser.vhdlParser.Group_template_declarationContext;
import vhdlParser.vhdlParser.Nature_declarationContext;
import vhdlParser.vhdlParser.Procedure_specificationContext;
import vhdlParser.vhdlParser.Signal_declarationContext;
import vhdlParser.vhdlParser.Subnature_declarationContext;
import vhdlParser.vhdlParser.Subprogram_declarationContext;
import vhdlParser.vhdlParser.Subprogram_specificationContext;
import vhdlParser.vhdlParser.Subtype_declarationContext;
import vhdlParser.vhdlParser.Terminal_declarationContext;
import vhdlParser.vhdlParser.Type_declarationContext;
import vhdlParser.vhdlParser.Use_clauseContext;
import vhdlParser.vhdlParser.Variable_declarationContext;

public class PackageHeaderParser {
	PackageHeader ph;
	boolean hierarchyOnly;
	public PackageHeaderParser(boolean _hierarchyOnly) {
		hierarchyOnly = _hierarchyOnly;
	}

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
		for (vhdlParser.Package_declarative_itemContext i : ctx
				.package_declarative_item()) {
			visitPackage_declarative_item(i);
		}
	}
	public static Function visitSubprogram_declaration(
			Subprogram_declarationContext ctx) {
		// subprogram_declaration
		// : subprogram_specification SEMI
		// ;
		return visitSubprogram_specification(ctx.subprogram_specification());
	}
	public static Function visitSubprogram_specification(
			Subprogram_specificationContext ctx) {
		// subprogram_specification
		// : procedure_specification
		// | function_specification
		// ;

		Procedure_specificationContext p = ctx.procedure_specification();
		if (p != null)
			return visitProcedure_specification(p);
		else
			return visitFunction_specification(ctx.function_specification());
	}

	public static Function visitProcedure_specification(
			Procedure_specificationContext ctx) {
		// procedure_specification
		// : PROCEDURE designator ( LPAREN formal_parameter_list RPAREN )?
		// ;
		DesignatorContext designator = ctx.designator();
		Expr returnT = null;
		boolean isOperator = LiteralParser.isStrDesignator(designator);
		Expr name = LiteralParser.visitDesignator(designator);
		List<Variable> paramList = visitFormal_parameter_list(
				ctx.formal_parameter_list());

		return new Function(name, isOperator, returnT, paramList);
	}
	public static Function visitFunction_specification(
			Function_specificationContext ctx) {
		// function_specification
		// : ( PURE | IMPURE )? FUNCTION designator
		// ( LPAREN formal_parameter_list RPAREN )? RETURN subtype_indication
		// ;
		DesignatorContext designator = ctx.designator();
		Expr returnT = ExprParser
				.visitSubtype_indication(ctx.subtype_indication());
		boolean isOperator = LiteralParser.isStrDesignator(designator);
		Expr name = LiteralParser.visitDesignator(designator);
		List<Variable> paramList = visitFormal_parameter_list(
				ctx.formal_parameter_list());

		return new Function(name, isOperator, returnT, paramList);
	}

	public static List<Variable> visitFormal_parameter_list(
			Formal_parameter_listContext ctx) {
		// formal_parameter_list
		// : interface_list
		// ;
		return InterfaceParser.visitInterface_list(ctx.interface_list());
	}

	public void visitPackage_declarative_item(
			vhdlParser.Package_declarative_itemContext ctx) {
		// package_declarative_item
		// : subprogram_declaration
		// | type_declaration
		// | subtype_declaration
		// | constant_declaration
		// | signal_declaration
		// | variable_declaration
		// | file_declaration
		// | alias_declaration
		// | component_declaration
		// | attribute_declaration
		// | attribute_specification
		// | disconnection_specification
		// | use_clause
		// | group_template_declaration
		// | group_declaration
		// | nature_declaration
		// | subnature_declaration
		// | terminal_declaration
		// ;
		Subprogram_declarationContext sp = ctx.subprogram_declaration();
		if (sp != null) {
			ph.functions.add(visitSubprogram_declaration(sp));
			return;
		}
		Type_declarationContext td = ctx.type_declaration();
		if (td != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitType_declaration");
		}
		Subtype_declarationContext st = ctx.subtype_declaration();
		if (st != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitSubtype_declaration");
		}
		Constant_declarationContext constd = ctx.constant_declaration();
		if (constd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitConstant_declaration");
		}
		Signal_declarationContext sd = ctx.signal_declaration();
		if (sd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitSignal_declaration");
		}
		Variable_declarationContext vd = ctx.variable_declaration();
		if (vd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitVariable_declaration");
		}
		File_declarationContext fd = ctx.file_declaration();
		if (fd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitFile_declaration");
		}
		Alias_declarationContext aliasd = ctx.alias_declaration();
		if (aliasd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitAlias_declaration");
		}
		Component_declarationContext compd = ctx.component_declaration();
		if (compd != null) {
			ph.components.add(visitComponent_declaration(compd));
		}
		Attribute_declarationContext atrd = ctx.attribute_declaration();
		if (atrd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitAttribute_declaration");
		}
		Attribute_specificationContext as = ctx.attribute_specification();
		if (as != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitAttribute_specification");
		}
		Disconnection_specificationContext discs = ctx
				.disconnection_specification();
		if (discs != null) {
			NotImplementedLogger.print(
					"PackageHeaderParser.visitDisconnection_specification");
		}
		Use_clauseContext uc = ctx.use_clause();
		if (uc != null) {
			NotImplementedLogger.print("PackageHeaderParser.visitUse_clause");
		}
		Group_template_declarationContext gtd = ctx
				.group_template_declaration();
		if (gtd != null) {
			NotImplementedLogger.print(
					"PackageHeaderParser.visitGroup_template_declaration");
		}
		Group_declarationContext gd = ctx.group_declaration();
		if (gd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitGroup_declaration");
		}
		Nature_declarationContext nd = ctx.nature_declaration();
		if (nd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitNature_declaration");
		}
		Subnature_declarationContext snd = ctx.subnature_declaration();
		if (snd != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitSubnature_declaration");
		}
		Terminal_declarationContext tdc = ctx.terminal_declaration();
		if (tdc != null) {
			NotImplementedLogger
					.print("PackageHeaderParser.visitTerminal_declaration");
		}
	}
	public Entity visitComponent_declaration(
			vhdlParser.Component_declarationContext ctx) {
		// component_declaration
		// : COMPONENT identifier ( IS )?
		// ( generic_clause )?
		// ( port_clause )?
		// END COMPONENT ( identifier )? SEMI
		// ;
		Entity e = new Entity();
		e.name = ctx.identifier(0).getText();
		if (!hierarchyOnly) {
			EntityParser.visitGeneric_clause(ctx.generic_clause(), e.generics);
			EntityParser.visitPort_clause(ctx.port_clause(), e.ports);
		}
		return e;
	}

}
