package verilogConvertor;

import java.util.Iterator;

import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;

import convertorApp.NotImplementedLogger;
import hdlObjects.Expr;
import hdlObjects.OperatorType;
import verilogParser.Verilog2001Parser.Attribute_instanceContext;
import verilogParser.Verilog2001Parser.Binary_operatorContext;
import verilogParser.Verilog2001Parser.ConcatenationContext;
import verilogParser.Verilog2001Parser.Constant_expressionContext;
import verilogParser.Verilog2001Parser.Constant_function_callContext;
import verilogParser.Verilog2001Parser.Escaped_hierarchical_branchContext;
import verilogParser.Verilog2001Parser.Escaped_hierarchical_identifierContext;
import verilogParser.Verilog2001Parser.ExpressionContext;
import verilogParser.Verilog2001Parser.Function_callContext;
import verilogParser.Verilog2001Parser.Hierarchical_identifierContext;
import verilogParser.Verilog2001Parser.Mintypmax_expressionContext;
import verilogParser.Verilog2001Parser.Multiple_concatenationContext;
import verilogParser.Verilog2001Parser.NumberContext;
import verilogParser.Verilog2001Parser.PrimaryContext;
import verilogParser.Verilog2001Parser.RangeContext;
import verilogParser.Verilog2001Parser.Range_expressionContext;
import verilogParser.Verilog2001Parser.Simple_hierarchical_branchContext;
import verilogParser.Verilog2001Parser.Simple_hierarchical_identifierContext;
import verilogParser.Verilog2001Parser.System_function_callContext;
import verilogParser.Verilog2001Parser.TermContext;
import verilogParser.Verilog2001Parser.Unary_operatorContext;

public class ExpressionParser {
	public static Expr visitConstant_expression(
			Constant_expressionContext ctx) {
		// constant_expression : expression ;
		return visitExpression(ctx.expression());
	}
	public static Expr visitRange_expression(Range_expressionContext ctx) {
		// range_expression :
		// expression
		// | msb_constant_expression ':' lsb_constant_expression
		// | base_expression '+:' width_constant_expression
		// | base_expression '-:' width_constant_expression
		// ;

		// msb_constant_expression : constant_expression ;
		// lsb_constant_expression : constant_expression ;
		// width_constant_expression : constant_expression ;
		// base_expression : expression ;
		NotImplementedLogger.print("ExpressionParser.visitRange_expression");
		return null;
	}
	public static Expr visitRange(RangeContext ctx) {
		// range : '[' msb_constant_expression ':' lsb_constant_expression ']' ;
		// msb_constant_expression : constant_expression ;
		// lsb_constant_expression : constant_expression ;
		return new Expr(
				visitConstant_expression(
						ctx.msb_constant_expression().constant_expression()),
				OperatorType.DOWNTO, visitConstant_expression(
						ctx.lsb_constant_expression().constant_expression()));

	}
	public static OperatorType visitBinary_operator(
			Binary_operatorContext ctx) {
		// binary_operator : '+' | '-' | '*' | '/' | '%' | '==' | '!=' | '===' |
		// '!==' | '&&' | '||' | '**' | '<' | '<=' | '>' | '>=' | '&' | '|' |
		// '^' | '^~' | '~^' | '>>' | '<<' | '>>>' | '<<<' ;
		// [TODO] log eq, neq
		String op = ctx.getText();
		switch (op) {
			case "+" :
				return OperatorType.PLUS;
			case "-" :
				return OperatorType.MINUS;
			case "*" :
				return OperatorType.MUL;
			case "/" :
				return OperatorType.DIV;
			case "%" :
				return OperatorType.MOD;
			case "==" :
			case "===" :
				return OperatorType.EQ;
			case "!=" :
			case "!==" :
				return OperatorType.NEQ;
			case "&&" :
				return OperatorType.LOG_AND;
			case "||" :
				return OperatorType.LOG_OR;
			case "**" :
				return OperatorType.DOUBLESTAR;
			case "<" :
				return OperatorType.LOWERTHAN;
			case "<=" :
				return OperatorType.LE;
			case ">" :
				return OperatorType.GREATERTHAN;
			case ">=" :
				return OperatorType.GE;
			case "&" :
				return OperatorType.AND;
			case "|" :
				return OperatorType.OR;
			case "^" :
				return OperatorType.XOR;
			case "^~" :
			case "~^" :
			case ">>" :
				return OperatorType.SRL;
			case "<<" :
				return OperatorType.SLL;
			case ">>>" :
				return OperatorType.SRA;
			case "<<<" :
				return OperatorType.SLA;
			default :
				return OperatorType.INVALID;
		}

	}
	public static Expr visitExpression(ExpressionContext ctx) {
		// expression:
		// term
		// (
		// binary_operator attribute_instance* term
		// | '?' attribute_instance* expression ':' term
		// )*
		// ;
		ParseTree ch;
		ParseTree ch2 = null;
		Iterator<ParseTree> childs = ctx.children.iterator();
		Expr top = visitTerm((TermContext) (childs.next()));

		// skip attribs
		while (childs.hasNext()) {
			ch = childs.next();
			if (ch instanceof Binary_operatorContext) {

				while (true) {
					ch2 = childs.next();
					if (ch2 instanceof Attribute_instanceContext) {
						AttributeParser.visitAttribute_instance(
								(Attribute_instanceContext) ch2);
					} else {
						break;
					}
				}
				top = new Expr(top,
						visitBinary_operator((Binary_operatorContext) ch),
						visitTerm((TermContext) ch2));
			} else {
				NotImplementedLogger
						.print("ExpressionParser.visitExpression - ternary op");
				while (true) {
					ch2 = childs.next();
					if (ch2 instanceof TermContext) {
						break;
					} else {
					}
				}
			}
		}

		return top;
	}
	public static Expr visitTerm(TermContext ctx) {
		// term :
		// unary_operator attribute_instance* primary
		// | primary
		// | String
		// ;
		Unary_operatorContext uOp = ctx.unary_operator();
		if (uOp != null) {
			NotImplementedLogger
					.print("ExpressionParser.visitTerm - unary_operator");
			return null;
		}
		PrimaryContext p = ctx.primary();
		if (p != null)
			return visitPrimary(p);
		return LiteralParser.visitString(ctx.String());
	}
	public static Expr visitPrimary(PrimaryContext ctx) {
		// primary :
		// number
		// | hierarchical_identifier
		// | hierarchical_identifier ( '[' expression ']' )+
		// | hierarchical_identifier ( '[' expression ']' )+ '['
		// range_expression
		// ']'
		// | hierarchical_identifier '[' range_expression ']'
		// | concatenation
		// | multiple_concatenation
		// | function_call
		// | system_function_call
		// | constant_function_call
		// | '(' mintypmax_expression ')'
		// ;
		NumberContext n = ctx.number();
		if (n != null)
			return LiteralParser.visitNumber(n);

		Hierarchical_identifierContext hi = ctx.hierarchical_identifier();
		if (hi != null) {
			Expr top = visitHierarchical_identifier(hi);
			for (ExpressionContext ex : ctx.expression()) {
				top = new Expr(top, OperatorType.INDEX, visitExpression(ex));
			}
			Range_expressionContext r = ctx.range_expression();
			if (r != null) {
				top = new Expr(top, OperatorType.INDEX,
						visitRange_expression(r));
			}
			return top;
		}

		ConcatenationContext c = ctx.concatenation();
		if (c != null) {
			return visitConcatenation(c);
		}
		Multiple_concatenationContext mc = ctx.multiple_concatenation();
		if (mc != null) {
			return visitMultiple_concatenation(mc);
		}

		Function_callContext fc = ctx.function_call();
		if (fc != null) {
			return visitFunction_call(fc);
		}
		System_function_callContext sfc = ctx.system_function_call();
		if (sfc != null) {
			return visitSystem_function_call(sfc);
		}
		Constant_function_callContext cfc = ctx.constant_function_call();
		if (cfc != null) {
			return visitConstant_function_call(cfc);
		}
		return visitMintypmax_expression(ctx.mintypmax_expression());
	}
	public static Expr visitConstant_function_call(
			Constant_function_callContext ctx) {
		// constant_function_call :
		// function_identifier attribute_instance* '('
		// (constant_expression ( ',' constant_expression )*)? ')'
		// ;
		NotImplementedLogger
				.print("ExpressionParser.visitConstant_function_call");
		return null;
	}
	public static Expr visitSystem_function_call(
			System_function_callContext ctx) {
		// system_function_call :
		// system_function_identifier (expression ( ',' expression )*)?
		// ;
		NotImplementedLogger
				.print("ExpressionParser.visitSystem_function_call");
		return null;
	}
	public static Expr visitFunction_call(Function_callContext ctx) {
		// function_call
		// : hierarchical_function_identifier attribute_instance*
		// '(' (expression ( ',' expression )*)? ')'
		// ;
		NotImplementedLogger.print("ExpressionParser.visitFunction_call");
		return null;
	}
	public static Expr visitMultiple_concatenation(
			Multiple_concatenationContext ctx) {
		// multiple_concatenation : '{' constant_expression concatenation '}' ;
		NotImplementedLogger
				.print("ExpressionParser.visitMultiple_concatenation");
		return null;
	}
	public static Expr visitConcatenation(ConcatenationContext ctx) {
		// concatenation : '{' expression ( ',' expression )* '}' ;
		NotImplementedLogger.print("ExpressionParser.visitConcatenation");
		return null;
	}
	public static Expr visitHierarchical_identifier(
			Hierarchical_identifierContext ctx) {
		// hierarchical_identifier :
		// simple_hierarchical_identifier
		// | escaped_hierarchical_identifier
		// ;
		Simple_hierarchical_identifierContext s = ctx
				.simple_hierarchical_identifier();
		if (s != null)
			return visitSimple_hierarchical_identifier(s);
		else
			return visitEscaped_hierarchical_identifier(
					ctx.escaped_hierarchical_identifier());
	}
	public static Expr visitEscaped_hierarchical_identifier(
			Escaped_hierarchical_identifierContext ctx) {
		// escaped_hierarchical_identifier :
		// escaped_hierarchical_branch ( '.' simple_hierarchical_branch | '.'
		// escaped_hierarchical_branch )*
		// ;
		Expr top = null;
		for (ParseTree ch : ctx.children) {
			if (top == null)
				top = visitEscaped_hierarchical_branch(
						ctx.escaped_hierarchical_branch(0));
			else {
				Expr second;
				if (ch instanceof Escaped_hierarchical_branchContext) {
					second = visitEscaped_hierarchical_branch(
							(Escaped_hierarchical_branchContext) ch);
				} else {
					second = visitSimple_hierarchical_branch(
							(Simple_hierarchical_branchContext) ch);
				}
				top = new Expr(top, OperatorType.DOT, second);
			}
		}
		return top;
	}
	public static Expr visitSimple_hierarchical_identifier(
			Simple_hierarchical_identifierContext ctx) {
		// simple_hierarchical_identifier : simple_hierarchical_branch ( '.'
		// Escaped_identifier )? ;
		Expr shb = visitSimple_hierarchical_branch(
				ctx.simple_hierarchical_branch());
		// [TODO] Escaped_identifier
		return shb;
	}
	public static Expr visitSimple_hierarchical_branch(
			Simple_hierarchical_branchContext ctx) {
		// simple_hierarchical_branch :
		// Simple_identifier ( '[' Decimal_number ']' )?
		// ( '.' Simple_identifier ( '[' Decimal_number ']' )? )*
		// ;
		Expr top = null;
		for (ParseTree ch : ctx.children) {
			if (top == null) {
				top = LiteralParser.parseSimple_identifier((TerminalNode) ch);
			} else {
				NotImplementedLogger.print(
						"ExpressionParser.visitSimple_hierarchical_branch");
			}

		}
		return top;
	}

	public static Expr visitEscaped_hierarchical_branch(
			Escaped_hierarchical_branchContext ctx) {
		// escaped_hierarchical_branch :
		// Escaped_identifier ( '[' Decimal_number ']' )?
		// ( '.' Escaped_identifier ( '[' Decimal_number ']' )? )*
		// ;
		NotImplementedLogger
				.print("ExpressionParser.visitEscaped_hierarchical_branch");
		return null;
	}
	public static Expr visitMintypmax_expression(
			Mintypmax_expressionContext ctx) {
		// mintypmax_expression
		// : expression (':' expression ':' expression)?
		// ;
		if (ctx.expression().size() > 1) {
			NotImplementedLogger.print(
					"ExpressionParser.visitMintypmax_expression - type and max specified");
		}
		return visitExpression(ctx.expression(0));
	}
}
