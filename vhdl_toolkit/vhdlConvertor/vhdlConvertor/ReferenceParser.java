package vhdlConvertor;

import java.util.Iterator;

import org.antlr.v4.runtime.tree.TerminalNode;

import vhdlObjects.Expr;
import vhdlObjects.OperatorType;
import vhdlObjects.Reference;
import vhdlObjects.SymbolType;
import vhdlParser.vhdlParser;

public class ReferenceParser {
	public static Reference visitSelected_name(
			vhdlParser.Selected_nameContext ctx) {
		// selected_name
		// : identifier (DOT suffix)*
		// ;
		Reference r = new Reference();
		r.add(LiteralParser.visitIdentifier(ctx.identifier()));
		for (vhdlParser.SuffixContext s : ctx.suffix()) {
			r.add(visitSuffix(s));
		}
		return r;
	}
	public static Expr visitSuffix(vhdlParser.SuffixContext ctx) {
		// suffix
		// : identifier
		// | CHARACTER_LITERAL
		// | STRING_LITERAL
		// | ALL
		// ;
		vhdlParser.IdentifierContext id = ctx.identifier();
		if (id != null)
			return LiteralParser.visitIdentifier(id);

		TerminalNode n = ctx.CHARACTER_LITERAL();
		if (n != null)
			return LiteralParser.visitCHARACTER_LITERAL(n);
		n = ctx.STRING_LITERAL();
		if (n != null)
			return LiteralParser.visitSTRING_LITERAL(n);

		assert (ctx.ALL() != null);
		return new Expr(SymbolType.ALL, null);
	}
	public static Expr visitName(vhdlParser.NameContext ctx) {
		// name
		// : selected_name
		// | name_part ( DOT name_part)*
		// ;
		vhdlParser.Selected_nameContext sn = ctx.selected_name();
		if (sn != null)
			return new Expr(visitSelected_name(sn));

		Iterator<vhdlParser.Name_partContext> nIt = ctx.name_part().iterator();
		Expr op0 = visitName_part(nIt.next());
		while (nIt.hasNext()) {
			Expr op1 = visitName_part(nIt.next());
			op0 = new Expr(op0, OperatorType.DOT, op1);
		}
		return op0;
	}
	public static Expr visitName_part(vhdlParser.Name_partContext ctx) {
		// name_part
		// : selected_name (name_attribute_part |
		// name_function_call_or_indexed_part | name_slice_part)?
		// ;
		Expr sn = new Expr(visitSelected_name(ctx.selected_name()));

		vhdlParser.Name_attribute_partContext na = ctx.name_attribute_part();
		if (na != null) {
			// name_attribute_part
			// : APOSTROPHE attribute_designator ( expression ( COMMA expression
			// )* )?
			// ;
			NotImplementedLogger.print("ExprParser.Name_attribute_partContext");
			return null;
		}
		vhdlParser.Name_function_call_or_indexed_partContext callOrIndx = ctx
				.name_function_call_or_indexed_part();
		if (callOrIndx != null) {
			// name_function_call_or_indexed_part
			// : LPAREN actual_parameter_part? RPAREN
			// ;
			return new Expr(sn, OperatorType.CALL, ExprParser.visitActual_parameter_part(
					callOrIndx.actual_parameter_part()));
		}
		vhdlParser.Name_slice_partContext ns = ctx.name_slice_part();
		if (ns != null) {
			NotImplementedLogger.print("ExprParser.visitName_slice_partContext");
			return null;
		}
		return sn;
	}
}
