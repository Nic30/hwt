package verilogConvertor;

import java.util.List;
import java.util.Vector;

import convertorApp.NotImplementedLogger;
import hdlObjects.Variable;
import verilogParser.Verilog2001Parser;

public class AttributeParser {
	public static List<Variable> visitAttribute_instance(
			Verilog2001Parser.Attribute_instanceContext ctx) {
		// attribute_instance : '(' '*' attr_spec ( ',' attr_spec )* '*' ')' ;
		NotImplementedLogger.print("AttributeParser.visitAttribute_instance");
		return new Vector<Variable>();
	}
}
