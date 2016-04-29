package vhdlConvertor;

import java.math.BigInteger;

import org.antlr.v4.runtime.tree.TerminalNode;

import convertorApp.NotImplementedLogger;
import hdlObjects.Expr;
import hdlObjects.SymbolType;
import vhdlParser.vhdlParser.Abstract_literalContext;
import vhdlParser.vhdlParser.DesignatorContext;
import vhdlParser.vhdlParser.Enumeration_literalContext;
import vhdlParser.vhdlParser.IdentifierContext;
import vhdlParser.vhdlParser.LiteralContext;
import vhdlParser.vhdlParser.Numeric_literalContext;
import vhdlParser.vhdlParser.Physical_literalContext;

public class LiteralParser {

	public static Expr visitLiteral(LiteralContext ctx) {
		// literal
		// : NULL
		// | BIT_STRING_LITERAL
		// | STRING_LITERAL
		// | enumeration_literal
		// | numeric_literal
		// ;
		if (ctx.NULL() != null)
			return new Expr(SymbolType.NULL, null);
		TerminalNode n;

		n = ctx.BIT_STRING_LITERAL();
		if (n != null) {
			String s = n.getText().toLowerCase();
			int radix = 0;
			int bitRatio = 0;
			switch (s.charAt(0)) {
				case 'b' :
					radix = 2;
					bitRatio = 1;
					break;
				case 'o' :
					radix = 8;
					bitRatio = 2;
					break;
				case 'x' :
					radix = 16;
					bitRatio = 4;
					break;
			}
			String strVal = s.substring(2, s.length() - 1);
			BigInteger val = new BigInteger(strVal, radix);
			return new Expr(val, strVal.length() * bitRatio);
		}

		n = ctx.STRING_LITERAL();
		if (n != null) {
			return visitSTRING_LITERAL(n);
		}

		Enumeration_literalContext el = ctx.enumeration_literal();
		if (el != null)
			return visitEnumeration_literal(el);
		Numeric_literalContext nl = ctx.numeric_literal();
		assert (nl != null);
		return visitNumeric_literal(nl);
	}
	public static Expr visitNumeric_literal(Numeric_literalContext ctx) {
		// numeric_literal
		// : abstract_literal
		// | physical_literal
		// ;
		Abstract_literalContext al = ctx.abstract_literal();
		if (al != null)
			return visitAbstract_literal(al);
		else
			return visitPhysical_literal(ctx.physical_literal());
	}
	public static Expr visitPhysical_literal(Physical_literalContext ctx) {
		// physical_literal
		// : abstract_literal (: identifier)
		// ;
		NotImplementedLogger.print("ExprParser.visitPhysical_literal");
		return null;
	}
	public static Expr visitAbstract_literal(Abstract_literalContext ctx) {
		// abstract_literal
		// : INTEGER
		// | REAL_LITERAL
		// | BASE_LITERAL
		// ;
		TerminalNode n = ctx.INTEGER();
		if (n != null)
			return new Expr(SymbolType.INT, new BigInteger(n.getText()));
		n = ctx.REAL_LITERAL();
		if (n != null)
			return new Expr(SymbolType.FLOAT, Float.parseFloat(n.getText()));

		// INTEGER must be checked to be between and including 2 and 16
		// (included) i.e. INTEGER >=2 and INTEGER <=16
		// A Based integer (a number without a . such as 3) should not have a
		// negative exponent A Based fractional number with a . i.e. 3.0 may
		// have a negative exponent These should be checked in the
		// Visitor/Listener whereby an appropriate error message
		// should be given

		// BASE_LITERAL
		// : INTEGER '#' BASED_INTEGER ('.'BASED_INTEGER)? '#' (EXPONENT)?
		// ;
		// [TODO] exponent
		n = ctx.BASE_LITERAL();
		Integer base = Integer.parseInt(n.getChild(0).getText());
		BigInteger val = new BigInteger(n.getChild(2).getText(), base);
		return new Expr(SymbolType.INT, val);
	}
	public static Expr visitEnumeration_literal(
			Enumeration_literalContext ctx) {
		// enumeration_literal
		// : identifier
		// | CHARACTER_LITERAL
		// ;
		// CHARACTER_LITERAL
		// : APOSTROPHE . APOSTROPHE
		// ;
		IdentifierContext id = ctx.identifier();
		if (id != null)
			return visitIdentifier(id);

		return visitCHARACTER_LITERAL(ctx.CHARACTER_LITERAL());
	}
	public static Expr visitSTRING_LITERAL(TerminalNode n) {
		String s = n.getText();
		return new Expr(SymbolType.STRING, s.subSequence(1, s.length() - 1));

	}
	public static Expr visitCHARACTER_LITERAL(TerminalNode ctx) {
		BigInteger ch = BigInteger
				.valueOf((int) (ctx.getText().charAt(1) - '0'));
		return new Expr(SymbolType.INT, ch);
	}
	public static Expr visitIdentifier(IdentifierContext ctx) {
		return new Expr(SymbolType.ID, ctx.getText());
	}
	static boolean isStrDesignator(DesignatorContext ctx) {
		// designator
		// : identifier
		// | STRING_LITERAL
		// ;
		return ctx.STRING_LITERAL() != null;
	}
	public static String visitDesignator(DesignatorContext ctx) {
		// designator
		// : identifier
		// | STRING_LITERAL
		// ;
		Expr e;
		if (isStrDesignator(ctx)) {
			e = visitSTRING_LITERAL(ctx.STRING_LITERAL());
		} else {
			e = visitIdentifier(ctx.identifier());
		}
		return (String) e.literal.value;
	}

}
