package vhdlConvertor;

import java.util.Iterator;
import java.util.List;
import java.util.Vector;

import convertorApp.NotImplementedLogger;
import hdlObjects.Expr;
import hdlObjects.OperatorType;
import hdlObjects.SymbolType;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.ConstraintContext;
import vhdlParser.vhdlParser.ExpressionContext;
import vhdlParser.vhdlParser.NameContext;
import vhdlParser.vhdlParser.Selected_nameContext;
import vhdlParser.vhdlParser.Subtype_indicationContext;
import vhdlParser.vhdlParser.TargetContext;
import vhdlParser.vhdlParser.WaveformContext;
import vhdlParser.vhdlParser.Waveform_elementContext;

public class ExprParser {

	public static List<Expr> visitActual_parameter_part(
			vhdlParser.Actual_parameter_partContext ctx) {
		List<Expr> l = new Vector<Expr>();
		if (ctx == null)
			return l;
		// actual_parameter_part
		// : association_list
		// ;
		// association_list
		// : association_element ( COMMA association_element )*
		// ;
		for (vhdlParser.Association_elementContext e : ctx.association_list()
				.association_element()) {
			l.add(visitAssociation_element(e));
		}
		return l;
	}
	public static Expr visitAssociation_element(
			vhdlParser.Association_elementContext ctx) {
		// association_element
		// : ( formal_part ARROW )? actual_part
		// ;
		Expr ap = visitActual_part(ctx.actual_part());
		vhdlParser.Formal_partContext fp = ctx.formal_part();
		if (fp != null) {
			return new Expr(visitFormal_part(fp), OperatorType.ARROW, ap);
		}
		return ap;
	}
	public static Expr visitFormal_part(vhdlParser.Formal_partContext ctx) {
		// formal_part
		// : identifier
		// | identifier LPAREN explicit_range RPAREN
		// ;
		Expr id = LiteralParser.visitIdentifier(ctx.identifier());
		vhdlParser.Explicit_rangeContext er = ctx.explicit_range();
		if (er != null) {
			return new Expr(id, OperatorType.RANGE, visitExplicit_range(er));
		}
		return id;
	}

	public static Expr visitExplicit_range(
			vhdlParser.Explicit_rangeContext ctx) {
		// explicit_range
		// : simple_expression direction simple_expression
		// ;
		OperatorType op;
		if (ctx.direction().DOWNTO() != null) {
			op = OperatorType.DOWNTO;
		} else {
			op = OperatorType.TO;
		}
		return new Expr(visitSimple_expression(ctx.simple_expression(0)), op,
				visitSimple_expression(ctx.simple_expression(1)));
	}
	public static Expr visitRange(vhdlParser.RangeContext ctx) {
		// range
		// : explicit_range
		// | name
		// ;

		vhdlParser.Explicit_rangeContext er = ctx.explicit_range();
		if (er != null)
			return visitExplicit_range(er);

		return ReferenceParser.visitName(ctx.name());
	}
	public static Expr visitActual_part(vhdlParser.Actual_partContext ctx) {
		// actual_part
		// : name LPAREN actual_designator RPAREN
		// | actual_designator
		// ;
		vhdlParser.NameContext name = ctx.name();
		Expr ad = visitActual_designator(ctx.actual_designator());
		if (name != null) {
			return new Expr(ReferenceParser.visitName(name), OperatorType.CALL,
					ad);
		}
		return ad;
	}
	public static Expr visitActual_designator(
			vhdlParser.Actual_designatorContext ctx) {
		// actual_designator
		// : expression
		// | OPEN
		// ;
		if (ctx.OPEN() != null)
			return new Expr(SymbolType.OPEN, null);

		return visitExpression(ctx.expression());
	}
	public static Expr visitSubtype_indication(Subtype_indicationContext ctx) {
		// subtype_indication
		// : selected_name ( selected_name )? ( constraint )? ( tolerance_aspect
		// )?
		// ;
		vhdlParser.ConstraintContext c = ctx.constraint();
		assert (ctx.tolerance_aspect() == null);
		List<Selected_nameContext> snames = ctx.selected_name();
		Selected_nameContext mainSelName = snames.get(0);
		
		if (snames.size() > 1)
			NotImplementedLogger.print(
					"ExprParser.visitSubtype_indication - selected_name2");
		if (ctx.tolerance_aspect() != null)
			NotImplementedLogger.print(
					"ExprParser.visitSubtype_indication - tolerance_aspect");

		if (c != null) {
			return visitConstraint(mainSelName, c);
		} else {
			return ReferenceParser.visitSelected_name(mainSelName);
		}
	}

	public static Expr visitConstraint(Selected_nameContext selectedName,
			ConstraintContext ctx) {
		// constraint
		// : range_constraint
		// | index_constraint
		// ;
		vhdlParser.Range_constraintContext r = ctx.range_constraint();
		OperatorType op;
		Expr op1 = null;
		if (r != null) {
			// range_constraint
			// : RANGE range
			// ;
			op = OperatorType.RANGE;
			op1 = visitRange(r.range());
		} else {
			vhdlParser.Index_constraintContext i = ctx.index_constraint();
			op = OperatorType.INDEX;
			op1 = visitIndex_constraint(i);
		}

		return new Expr(ReferenceParser.visitSelected_name(selectedName), op,
				op1);

	}
	public static Expr visitIndex_constraint(
			vhdlParser.Index_constraintContext ctx) {
		// index_constraint
		// : LPAREN discrete_range ( COMMA discrete_range )* RPAREN
		// ;
		if (ctx.discrete_range().size() > 1) {
			NotImplementedLogger.print(
					"ExprParser.visitIndex_constraint multiple discrete_range");
		}
		return visitDiscrete_range(ctx.discrete_range(0));
	}
	public static Expr visitDiscrete_range(
			vhdlParser.Discrete_rangeContext ctx) {
		// discrete_range
		// : range
		// | subtype_indication
		// ;
		vhdlParser.RangeContext r = ctx.range();
		if (r != null)
			return visitRange(r);
		return visitSubtype_indication(ctx.subtype_indication());
	}
	public static Expr visitSimple_expression(
			vhdlParser.Simple_expressionContext ctx) {
		// simple_expression
		// : ( PLUS | MINUS )? term ( : adding_operator term )*
		// ;
		// adding_operator
		// : PLUS
		// | MINUS
		// | AMPERSAND
		// ;

		Iterator<vhdlParser.TermContext> t = ctx.term().iterator();
		Iterator<vhdlParser.Adding_operatorContext> opList = ctx
				.adding_operator().iterator();
		Expr op0 = visitTerm(t.next());
		if (ctx.MINUS() != null) {
			op0 = new Expr(op0, OperatorType.UN_MINUS, (Expr) null);
		}
		while (opList.hasNext()) {
			vhdlParser.Adding_operatorContext op = opList.next();
			Expr op1 = visitTerm(t.next());
			OperatorType opType;
			if (op.PLUS() != null)
				opType = OperatorType.PLUS;
			else if (op.MINUS() != null) {
				opType = OperatorType.MINUS;
			} else {
				assert (op.AMPERSAND() != null);
				opType = OperatorType.CONCAT;
			}
			op0 = new Expr(op0, opType, op1);
		}
		return op0;
	}
	public static Expr visitExpression(vhdlParser.ExpressionContext ctx) {
		// expression
		// : relation ( : logical_operator relation )*
		// ;
		Iterator<vhdlParser.RelationContext> relIt = ctx.relation().iterator();
		Iterator<vhdlParser.Logical_operatorContext> opIt = ctx
				.logical_operator().iterator();
		Expr op0 = visitRelation(relIt.next());
		while (opIt.hasNext()) {
			Expr op1 = visitRelation(relIt.next());
			op0 = new Expr(op0, OperatorType.from(opIt.next()), op1);
		}
		return op0;
	}
	public static Expr visitRelation(vhdlParser.RelationContext ctx) {
		// relation
		// : shift_expression
		// ( : relational_operator shift_expression )?
		// ;

		vhdlParser.Shift_expressionContext ex = ctx.shift_expression(0);
		Expr op0 = visitShift_expression(ex);

		vhdlParser.Relational_operatorContext op = ctx.relational_operator();
		if (op != null) {
			Expr op1 = visitShift_expression(ctx.shift_expression(1));
			op0 = new Expr(op0, OperatorType.from(op), op1);
		}

		return op0;

	}
	public static Expr visitShift_expression(
			vhdlParser.Shift_expressionContext ctx) {
		// shift_expression
		// : simple_expression
		// ( : shift_operator simple_expression )?
		// ;
		Expr op0 = visitSimple_expression(ctx.simple_expression(0));
		vhdlParser.Shift_operatorContext op = ctx.shift_operator();
		if (op != null) {
			Expr op1 = visitSimple_expression(ctx.simple_expression(1));
			op0 = new Expr(op0, OperatorType.from(op), op1);
		}
		return op0;
	}
	public static Expr visitTerm(vhdlParser.TermContext ctx) {
		// term
		// : factor ( : multiplying_operator factor )*
		// ;

		// multiplying_operator
		// : MUL
		// | DIV
		// | MOD
		// | REM
		// ;
		Iterator<vhdlParser.FactorContext> t = ctx.factor().iterator();
		Iterator<vhdlParser.Multiplying_operatorContext> opList = ctx
				.multiplying_operator().iterator();
		Expr op0 = visitFactor(t.next());

		while (opList.hasNext()) {
			vhdlParser.Multiplying_operatorContext op = opList.next();
			Expr op1 = visitFactor(t.next());
			OperatorType opType;
			if (op.MUL() != null)
				opType = OperatorType.MUL;
			else if (op.DIV() != null)
				opType = OperatorType.DIV;
			else if (op.MOD() != null)
				opType = OperatorType.MOD;
			else {
				assert (op.REM() != null);
				opType = OperatorType.REM;
			}
			op0 = new Expr(op0, opType, op1);
		}
		return op0;
	}
	public static Expr visitFactor(vhdlParser.FactorContext ctx) {
		// factor
		// : primary ( : DOUBLESTAR primary )?
		// | ABS primary
		// | NOT primary
		// ;
		Expr op0 = visitPrimary(ctx.primary(0));
		vhdlParser.PrimaryContext p1 = ctx.primary(1);
		if (p1 != null)
			return new Expr(op0, OperatorType.POW, visitPrimary(p1));
		if (ctx.ABS() != null)
			return new Expr(op0, OperatorType.ABS, (Expr) null);
		if (ctx.NOT() != null)
			return new Expr(op0, OperatorType.NOT, (Expr) null);
		return op0;
	}
	public static Expr visitPrimary(vhdlParser.PrimaryContext ctx) {
		// primary
		// : literal
		// | qualified_expression
		// | LPAREN expression RPAREN
		// | allocator
		// | aggregate
		// | name
		// ;
		vhdlParser.LiteralContext l = ctx.literal();
		if (l != null)
			return LiteralParser.visitLiteral(l);
		vhdlParser.Qualified_expressionContext qe = ctx.qualified_expression();
		if (qe != null)
			return visitQualified_expression(qe);
		vhdlParser.ExpressionContext e = ctx.expression();
		if (e != null)
			return visitExpression(e);
		vhdlParser.AllocatorContext al = ctx.allocator();
		if (al != null)
			return visitAllocator(al);
		vhdlParser.AggregateContext ag = ctx.aggregate();
		if (ag != null)
			return visitAggregate(ag);
		vhdlParser.NameContext n = ctx.name();
		assert (n != null);
		return ReferenceParser.visitName(n);
	}
	public static Expr visitQualified_expression(
			vhdlParser.Qualified_expressionContext ctx) {
		// qualified_expression
		// : subtype_indication APOSTROPHE ( aggregate | LPAREN expression
		// RPAREN )
		// ;
		NotImplementedLogger.print("ExprParser visitQualified_expression");
		return null;
	}
	public static Expr visitAllocator(vhdlParser.AllocatorContext ctx) {
		// allocator
		// : NEW ( qualified_expression | subtype_indication )
		// ;
		NotImplementedLogger.print("ExprParser visitAllocator");
		return null;

	}
	public static Expr visitAggregate(vhdlParser.AggregateContext ctx) {
		// aggregate
		// : LPAREN element_association ( COMMA element_association )* RPAREN
		// ;
		NotImplementedLogger.print("ExprParser visitAggregate");
		return null;
	}

	public static Expr visitTarget(TargetContext ctx) {
		// target
		// : name
		// | aggregate
		// ;
		NameContext n = ctx.name();
		if (n != null) {
			return ReferenceParser.visitName(n);
		} else {
			return visitAggregate(ctx.aggregate());
		}

	}
	public static Expr visitWaveform(WaveformContext ctx) {
		// waveform :
		// waveform_element ( COMMA waveform_element )*
		// | UNAFFECTED
		// ;
		if (ctx.UNAFFECTED() != null) {
			NotImplementedLogger.print("ExprParser.visitWaveform - UNAFFECTED");
			return null;
		}
		Iterator<Waveform_elementContext> we = ctx.waveform_element()
				.iterator();

		Expr top = visitWaveform_element(we.next());
		while (we.hasNext()) {
			top = new Expr(top, OperatorType.DOT,
					visitWaveform_element(we.next()));
		}
		return top;
	}

	public static Expr visitWaveform_element(Waveform_elementContext ctx) {
		// waveform_element :
		// expression ( AFTER expression )?
		// ;
		Iterator<ExpressionContext> e = ctx.expression().iterator();
		Expr top = visitExpression(e.next());
		if (e.hasNext()) {
			NotImplementedLogger.print(
					"ExprParser.visitWaveform_element - AFTER expression");
		}
		return top;

	}
}
