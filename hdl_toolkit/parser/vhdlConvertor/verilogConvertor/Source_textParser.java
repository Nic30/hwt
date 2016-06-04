package verilogConvertor;

import convertorApp.IHdlParser;
import convertorApp.NotImplementedLogger;
import hdlObjects.Context;
import verilogParser.Verilog2001Parser;
import verilogParser.Verilog2001Parser.DescriptionContext;
import verilogParser.Verilog2001Parser.Timing_specContext;

public class Source_textParser implements IHdlParser {
	boolean hierarchyOnly;
	Context context;
	public Source_textParser(boolean hierarchyOnly) {
		this.context = new Context();
		this.hierarchyOnly = hierarchyOnly;
	}
	public Context getContext() {
		return context;
	}
	public void visitSource_text(Verilog2001Parser.Source_textContext ctx) {
		//// START SYMBOL
		// source_text : timing_spec? description* EOF ;
		if (!hierarchyOnly) {
			Timing_specContext t = ctx.timing_spec();
			if (t != null)
				visitTiming_spec(t);
		}
		for (DescriptionContext d : ctx.description()) {
			visitDescription(d);
		}
	}
	void visitTiming_spec(Verilog2001Parser.Timing_specContext ctx) {
		// timing_spec : '`timescale' Time_Identifier '/' Time_Identifier;
		NotImplementedLogger.print("Source_textParser.visitTiming_spec");
	}
	void visitDescription(Verilog2001Parser.DescriptionContext ctx) {
		// description : module_declaration ;
		ModuleParser p = new ModuleParser(context, hierarchyOnly);
		p.visitModule_declaration(ctx.module_declaration());
	}
}
