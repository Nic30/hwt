package verilogConvertor;

import java.math.BigInteger;

import org.antlr.v4.runtime.tree.TerminalNode;

import convertorApp.NotImplementedLogger;
import hdlObjects.Expr;
import hdlObjects.SymbolType;
import verilogParser.Verilog2001Parser;

public class LiteralParser {
	public static Expr visitNumber(Verilog2001Parser.NumberContext ctx) {
		// number :
		// Decimal_number
		// | Octal_number
		// | Binary_number
		// | Hex_number
		// | Real_number
		// ;
		TerminalNode n = ctx.Decimal_number();
		if (n != null) {
			return parseIntNumber(n, 10);
		}
		n = ctx.Octal_number();
		if (n != null) {
			return parseIntNumber(n, 8);
		}
		n = ctx.Binary_number();
		if (n != null) {
			return parseIntNumber(n, 2);
		}
		n = ctx.Hex_number();
		if (n != null) {
			return parseIntNumber(n, 16);
		}
		NotImplementedLogger.print("ExpressionParser.visitNumber - Real_number");
		return null;

	}
	public static Expr parseSimple_identifier(TerminalNode n){
		return new Expr(SymbolType.ID, n.getText());
	}
	public static Expr parseIntNumber(TerminalNode n, int radix) {
		// Decimal_number :
		// Unsigned_number
		// | ( Size )? Decimal_base Unsigned_number
		// | ( Size )? Decimal_base X_digit ( '_' )*
		// | ( Size )? Decimal_base Z_digit ( '_' )*
		// ;

		// Unsigned_number : Decimal_digit ( '_' | Decimal_digit )* ;
		String s = n.getText().toLowerCase().replace("_", "");
		int size = -1;
		int valuePartStart = 0;

		int baseStart = s.indexOf('\'');
		if (baseStart >= 0) {
			if (baseStart > 0) {
				String sizeStr = s.substring(0, baseStart);
				size = Integer.parseInt(sizeStr);
			}
			valuePartStart = baseStart + 2;
			if (s.charAt(baseStart + 1) == 's')
				valuePartStart += 1;
		}

		String strVal = s.substring(valuePartStart, s.length());
		BigInteger val = new BigInteger(strVal.replaceAll("[xz]", "0"), radix);
		if (size == -1)
			return new Expr(SymbolType.INT, val);
		else
			return new Expr(val, size);
	}

	// Real_number :
	// Unsigned_number '.' Unsigned_number
	// | Unsigned_number ( '.' Unsigned_number )? [eE] ( [+-] )? Unsigned_number
	// ;
	//
	//
	// Binary_number : ( Size )? Binary_base Binary_value ;
	// Octal_number : ( Size )? Octal_base Octal_value ;
	// Hex_number : ( Size )? Hex_base Hex_value ;
	public static Expr visitString(TerminalNode n) {
		String s = n.getText();
		return new Expr(SymbolType.STRING, s.subSequence(1, s.length() - 1));
	}
}
