package vhdlConvertor;

import java.util.List;
import java.util.Vector;

import convertorApp.IHdlParser;
import convertorApp.NotImplementedLogger;
import hdlObjects.Arch;
import hdlObjects.Context;
import hdlObjects.Entity;
import hdlObjects.Expr;
import hdlObjects.Package;
import hdlObjects.PackageHeader;
import vhdlParser.vhdlParser;

public class DesignFileParser implements IHdlParser {
	public Context context;
	boolean hierarchyOnly;
	public DesignFileParser(boolean _hierarchyOnly) {
		hierarchyOnly = _hierarchyOnly;
		context = new Context();
	}
	public Context getContext() {
		return context;
	}
	public void visitDesign_file(vhdlParser.Design_fileContext ctx) {
		if (ctx == null)
			return;
		// design_file
		// : ( design_unit )* EOF
		// ;
		for (vhdlParser.Design_unitContext u : ctx.design_unit()) {
			visitDesign_unit(u);
		}
	}

	void visitDesign_unit(vhdlParser.Design_unitContext ctx) {
		if (ctx == null)
			return;
		// design_unit
		// : context_clause library_unit
		// ;
		visitContext_clause(ctx.context_clause());
		visitLibrary_unit(ctx.library_unit());
	}
	void visitLibrary_unit(vhdlParser.Library_unitContext ctx) {
		if (ctx == null)
			return;
		// library_unit
		// : secondary_unit | primary_unit
		// ;

		visitSecondary_unit(ctx.secondary_unit());
		visitPrimary_unit(ctx.primary_unit());
	}
	void visitSecondary_unit(vhdlParser.Secondary_unitContext ctx) {
		if (ctx == null)
			return;
		// secondary_unit
		// : architecture_body
		// | package_body
		// ;
		vhdlParser.Architecture_bodyContext arch = ctx.architecture_body();
		if (arch != null) {
			Arch a = (new ArchParser(hierarchyOnly))
					.visitArchitecture_body(arch);
			context.architectures.add(a);
		}
		vhdlParser.Package_bodyContext pack = ctx.package_body();
		if (pack != null) {
			Package p = (new PackageParser(hierarchyOnly))
					.visitPackage_body(pack);
			context.packages.add(p);
		}
	}
	void visitContext_clause(vhdlParser.Context_clauseContext ctx) {
		if (ctx == null)
			return;
		// context_clause
		// : ( context_item )*
		// ;
		for (vhdlParser.Context_itemContext item : ctx.context_item()) {
			visitContext_item(item);
		}
	}
	void visitPrimary_unit(vhdlParser.Primary_unitContext ctx) {
		if (ctx == null)
			return;
		// primary_unit
		// : entity_declaration
		// | configuration_declaration
		// | package_declaration
		// ;
		vhdlParser.Entity_declarationContext ed = ctx.entity_declaration();
		if (ed != null) {
			Entity e = (new EntityParser(hierarchyOnly))
					.visitEntity_declaration(ed);
			context.entities.add(e);
			return;
		}
		vhdlParser.Configuration_declarationContext cd = ctx
				.configuration_declaration();
		if (cd != null) {
			NotImplementedLogger
					.print("DesignFileParser.visitConfiguration_declaration");
			return;
		}
		vhdlParser.Package_declarationContext pd = ctx.package_declaration();
		if (pd != null) {
			PackageHeader ph = (new PackageHeaderParser(hierarchyOnly))
					.visitPackage_declaration(pd);
			context.packageHeaders.add(ph);
		}

	}
	void visitContext_item(vhdlParser.Context_itemContext ctx) {
		// context_item
		// : library_clause
		// | use_clause
		// ;
		vhdlParser.Library_clauseContext l = ctx.library_clause();
		if (l != null) {
			return; //libraries are ignored
		}
		vhdlParser.Use_clauseContext u = ctx.use_clause();
		if (u != null) {
			for (Expr r : visitUse_clause(u)) {
				context.imports.add(r);
			}
		}

	}

	List<Expr> visitUse_clause(vhdlParser.Use_clauseContext ctx) {
		// use_clause
		// : USE selected_name ( COMMA selected_name )* SEMI
		// ;
		List<Expr> refL = new Vector<Expr>();
		for (vhdlParser.Selected_nameContext sn : ctx.selected_name()) {
			Expr r = ReferenceParser.visitSelected_name(sn);
			refL.add(r);
		}
		return refL;
	}
}
