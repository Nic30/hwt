package vhdlConvertor;

import java.util.Iterator;
import java.util.List;
import java.util.Vector;

import convertorApp.NotImplementedLogger;
import hdlObjects.Expr;
import hdlObjects.Statement;
import hdlObjects.SymbolType;
import vhdlParser.vhdlParser.Assertion_statementContext;
import vhdlParser.vhdlParser.Case_statementContext;
import vhdlParser.vhdlParser.ConditionContext;
import vhdlParser.vhdlParser.ExpressionContext;
import vhdlParser.vhdlParser.If_statementContext;
import vhdlParser.vhdlParser.Iteration_schemeContext;
import vhdlParser.vhdlParser.Loop_statementContext;
import vhdlParser.vhdlParser.Report_statementContext;
import vhdlParser.vhdlParser.Return_statementContext;
import vhdlParser.vhdlParser.Sequence_of_statementsContext;
import vhdlParser.vhdlParser.Sequential_statementContext;
import vhdlParser.vhdlParser.Signal_assignment_statementContext;
import vhdlParser.vhdlParser.Variable_assignment_statementContext;

public class StatementParser {
	public static Statement visitSequential_statement(
			Sequential_statementContext ctx) {
		// sequential_statement :
		// wait_statement
		// | assertion_statement
		// | report_statement
		// | signal_assignment_statement
		// | variable_assignment_statement
		// | if_statement
		// | case_statement
		// | loop_statement
		// | next_statement
		// | exit_statement
		// | return_statement
		// | ( label_colon )? NULL SEMI
		// | break_statement
		// | procedure_call_statement
		// ;
		Assertion_statementContext as = ctx.assertion_statement();
		if (as != null) {
			NotImplementedLogger.print(
					"StatementParser.visitSequential_statement - assertion_statement");
			return null;
		}

		Report_statementContext r = ctx.report_statement();
		if (r != null) {
			NotImplementedLogger.print(
					"StatementParser.visitSequential_statement - report_statement");
			return null;
		}

		Signal_assignment_statementContext sas = ctx
				.signal_assignment_statement();
		if (sas != null)
			return visitSignal_assignment_statement(sas);

		Variable_assignment_statementContext vas = ctx
				.variable_assignment_statement();
		if (vas != null)
			return visitVariable_assignment_statement(vas);

		If_statementContext ifStm = ctx.if_statement();
		if (ifStm != null)
			return visitIf_statement(ifStm);

		Return_statementContext rt = ctx.return_statement();
		if (rt != null)
			return visitReturn_statement(rt);

		Case_statementContext c = ctx.case_statement();
		if (c != null) {
			NotImplementedLogger.print(
					"StatementParser.visitSequential_statement - case_statement");
			return null;
		}

		Loop_statementContext l = ctx.loop_statement();
		if (l != null)
			return visitLoop_statement(l);

		NotImplementedLogger.print("StatementParser.visitSequential_statement");
		return null;

	}
	public static Statement visitSignal_assignment_statement(
			Signal_assignment_statementContext ctx) {
		// signal_assignment_statement :
		// ( label_colon )?
		// target LE ( delay_mechanism )? waveform SEMI
		// ;
		if (ctx.label_colon() != null)
			NotImplementedLogger.print(
					"StatementParser.visitSignal_assignment_statement - label_colon");
		if (ctx.delay_mechanism() != null)
			NotImplementedLogger.print(
					"StatementParser.visitSignal_assignment_statement - delay_mechanism");

		return Statement.ASSIG(ExprParser.visitTarget(ctx.target()),
				ExprParser.visitWaveform(ctx.waveform()));

	}
	public static Statement visitVariable_assignment_statement(
			Variable_assignment_statementContext ctx) {
		// variable_assignment_statement :
		// ( label_colon )? target VARASGN expression SEMI
		// ;
		if (ctx.label_colon() != null)
			NotImplementedLogger.print(
					"StatementParser.visitSignal_assignment_statement - label_colon");

		return Statement.ASSIG(ExprParser.visitTarget(ctx.target()),
				ExprParser.visitExpression(ctx.expression()));
	}
	public static Statement visitIf_statement(If_statementContext ctx) {
		// if_statement :
		// ( label_colon )? IF condition THEN
		// sequence_of_statements
		// ( ELSIF condition THEN sequence_of_statements )*
		// ( ELSE sequence_of_statements )?
		// END IF ( identifier )? SEMI
		// ;
		if (ctx.label_colon() != null)
			NotImplementedLogger
					.print("StatementParser.visitIf_statement - label_colon");

		Iterator<ConditionContext> c = ctx.condition().iterator();
		Iterator<Sequence_of_statementsContext> s = ctx.sequence_of_statements()
				.iterator();

		Expr cond = visitCondition(c.next());
		if (c.hasNext()) {
			NotImplementedLogger
					.print("StatementParser.visitIf_statement - ELSIF");
		}
		List<Statement> ifTrue = visitSequence_of_statements(s.next());
		if (s.hasNext()) {
			return Statement.IF(cond, ifTrue,
					visitSequence_of_statements(s.next()));
		} else {
			return Statement.IF(cond, ifTrue);
		}
	}
	public static Statement visitReturn_statement(Return_statementContext ctx) {
		// return_statement
		// : ( label_colon )? RETURN ( expression )? SEMI
		// ;
		if (ctx.label_colon() != null) {
			NotImplementedLogger.print(
					"StatementParser.visitReturn_statement - label_colon");
		}
		ExpressionContext e = ctx.expression();
		if (e != null) {
			return Statement.RETURN(ExprParser.visitExpression(e));
		} else {
			return Statement.RETURN();
		}

	}
	public static Statement visitLoop_statement(Loop_statementContext ctx) {
		// loop_statement :
		// ( label_colon )? ( iteration_scheme )?
		// LOOP
		// sequence_of_statements
		// END LOOP ( identifier )? SEMI
		// ;
		if (ctx.label_colon() != null) {
			NotImplementedLogger
					.print("StatementParser.visitLoop_statement - label_colon");
		}
		Iteration_schemeContext is = ctx.iteration_scheme();
		Statement loop;

		if (is != null)
			loop = visitIteration_scheme(is);
		else {
			loop = Statement.WHILE(new Expr(SymbolType.ID, "True"),
					new Vector<Statement>());
		}
		loop.ops.set(0,
				visitSequence_of_statements(ctx.sequence_of_statements()));
		return loop;
	}
	public static Expr visitCondition(ConditionContext ctx) {
		// condition
		// : expression
		// ;
		return ExprParser.visitExpression(ctx.expression());
	}
	public static Statement visitIteration_scheme(Iteration_schemeContext ctx) {
		// iteration_scheme
		// : WHILE condition
		// | FOR parameter_specification
		// ;
		if (ctx.WHILE() != null)
			return Statement.WHILE(visitCondition(ctx.condition()),
					new Vector<Statement>());
		else {
			NotImplementedLogger
					.print("StatementParser.visitIteration_scheme - FOR");
			return null;
		}

	}
	public static List<Statement> visitSequence_of_statements(
			Sequence_of_statementsContext ctx) {
		// sequence_of_statements
		// : ( sequential_statement )*
		// ;
		List<Statement> s = new Vector<Statement>();
		for (Sequential_statementContext ss : ctx.sequential_statement()) {
			s.add(visitSequential_statement(ss));
		}
		return s;
	}
}
