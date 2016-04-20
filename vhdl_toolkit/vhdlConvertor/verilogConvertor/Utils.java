package verilogConvertor;

import java.util.List;
import java.util.Vector;

import hdlObjects.Expr;
import hdlObjects.SymbolType;
import verilogParser.Verilog2001Parser.RangeContext;

public class Utils {
	public static Expr mkStringT() {
		return mkId("__str__");
	}
	public static Expr mkWireT() {
		return mkId("wire");
	}
	public static Expr mkWireT(Expr range) {
		List<Expr> operands = new Vector<Expr>();
		operands.add(range);
		return Expr.call(mkWireT(), operands);
	}
	public static Expr mkWireT(RangeContext range) {
		if (range != null)
			return mkWireT(ExprParser.visitRange(range));
		else
			return mkWireT();
	}
	public static Expr mkId(String id) {
		return new Expr(SymbolType.ID, id);
	}

}
