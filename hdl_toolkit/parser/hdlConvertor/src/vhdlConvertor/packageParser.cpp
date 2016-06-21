#include "packageParser.h"

PackageParser::PackageParser(bool _hierarchyOnly) {
	hierarchyOnly = _hierarchyOnly;
	p = new Package();
}
Package * PackageParser::visitPackage_body(
		Ref<vhdlParser::Package_bodyContext> ctx) {
	// package_body
	// : PACKAGE BODY identifier IS
	// package_body_declarative_part
	// END ( PACKAGE BODY )? ( identifier )? SEMI
	// ;
	p->name =
			(String) LiteralParser::visitIdentifier(ctx->identifier(0)).literal.value;
	if (!hierarchyOnly) {
		visitPackage_body_declarative_part(p,
				ctx->package_body_declarative_part());
	}
	return p;
}
void PackageParser::visitPackage_body_declarative_part(
		aPackage p,
		Ref<vhdlParser::Package_body_declarative_partContext> ctx) {
	// package_body_declarative_part
	// : ( package_body_declarative_item )*
	// ;
	for (auto i : ctx->package_body_declarative_item()) {
		visitPackage_body_declarative_item(i);
	}
}
void PackageParser::visitPackage_body_declarative_item(
		Ref<vhdlParser::Package_body_declarative_itemContext> ctx) {
	// package_body_declarative_item
	// : subprogram_declaration
	// | subprogram_body
	// | type_declaration
	// | subtype_declaration
	// | constant_declaration
	// | variable_declaration
	// | file_declaration
	// | alias_declaration
	// | use_clause
	// | group_template_declaration
	// | group_declaration
	// ;
	auto sd = ctx->subprogram_declaration();
	if (sd) {
		visitSubprogram_declaration(sd);
		return;
	}

	auto sb = ctx->subprogram_body();
	if (sb) {
		p.functions.add(visitSubprogram_body(sb));
		return;
	}

	NotImplementedLogger::print(
			"PackageParser.visitPackage_body_declarative_item");
}
static Function * PackageParser::visitSubprogram_body(
		Ref<vhdlParser.Subprogram_bodyContext> ctx) {
	// subprogram_body :
	// subprogram_specification IS
	// subprogram_declarative_part
	// BEGIN
	// subprogram_statement_part
	// END ( subprogram_kind )? ( designator )? SEMI
	// ;
	Function * f = PackageHeaderParser::visitSubprogram_specification(
			ctx->subprogram_specification());
	for (Variable * v : visitSubprogram_declarative_part(
			ctx->subprogram_declarative_part())) {
		f->locals->push_back(v);
	}
	for (Statement * s : visitSubprogram_statement_part(
			ctx->subprogram_statement_part())) {
		f->body->push_back(s);
	}
	return f;
}
static std::vector<Variable*>* PackageParser::PackageParser::visitSubprogram_declarative_part(
		Ref<vhdlParser::Subprogram_declarative_partContext> ctx) {
	// subprogram_declarative_part
	// : ( subprogram_declarative_item )*
	// ;
	std::vector<Variable*> * vars = new std::vector<Variable*>();
	for (auto sd : ctx->subprogram_declarative_item()) {
		vars.addAll(visitSubprogram_declarative_item(sd));
	}

	return vars;
}
static std::vector<Variable *> * PackageParser::visitSubprogram_declarative_item(
		Ref<vhdlParser::Subprogram_declarative_itemContext> ctx) {
	// subprogram_declarative_item
	// : subprogram_declaration
	// | subprogram_body
	// | type_declaration
	// | subtype_declaration
	// | constant_declaration
	// | variable_declaration
	// | file_declaration
	// | alias_declaration
	// | attribute_declaration
	// | attribute_specification
	// | use_clause
	// | group_template_declaration
	// | group_declaration
	// ;
	auto vd = ctx->variable_declaration();
	if (vd) {
		return visitVariable_declaration(vd);
	}

	NotImplementedLogger::print(
			"PackageParser.visitSubprogram_declarative_item");
	return new std::vector<Variable>();
}

static std::vector<Variable*> * PackageParser::visitVariable_declaration(
		Ref<vhdlParser::Variable_declarationContext> ctx) {
	// variable_declaration :
	// ( SHARED )? VARIABLE identifier_list COLON
	// subtype_indication ( VARASGN expression )? SEMI
	// ;
	if (ctx->SHARED())
		NotImplementedLogger::print(
				"PackageParser.visitVariable_declaration - SHARED");

	std::vector<Variable*> * vl = InterfaceParser::extractVariables(
			ctx->identifier_list(), ctx->subtype_indication(),
			ctx->expression());
	return vl;
}

void PackageParser::visitSubprogram_declaration(
		Ref<vhdlParser::Subprogram_declarationContext> ctx) {
	// subprogram_declaration
	// : subprogram_specification SEMI
	// ;
	NotImplementedLogger::print("PackageParser.visitSubprogram_declaration");
}

static std::vector<Statement *> * PackageParser::visitSubprogram_statement_part(
		Ref<vhdlParser::Subprogram_statement_partContext> ctx) {
	// subprogram_statement_part
	// : ( sequential_statement )*
	// ;
	std::vector<Statement *> * statements = new std::vector<Statement*>();
	for (auto s : ctx->sequential_statement()) {
		statements->push_back(StatementParser::visitSequential_statement(s));
	}
	return statements;
}
