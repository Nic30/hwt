// Generated from vhdl.g4 by ANTLR 4.5.1
package vhdlParser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link vhdlParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface vhdlVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link vhdlParser#abstract_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbstract_literal(vhdlParser.Abstract_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#access_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAccess_type_definition(vhdlParser.Access_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#across_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAcross_aspect(vhdlParser.Across_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#actual_designator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitActual_designator(vhdlParser.Actual_designatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#actual_parameter_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitActual_parameter_part(vhdlParser.Actual_parameter_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#actual_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitActual_part(vhdlParser.Actual_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#adding_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAdding_operator(vhdlParser.Adding_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#aggregate}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAggregate(vhdlParser.AggregateContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#alias_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAlias_declaration(vhdlParser.Alias_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#alias_designator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAlias_designator(vhdlParser.Alias_designatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#alias_indication}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAlias_indication(vhdlParser.Alias_indicationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#allocator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAllocator(vhdlParser.AllocatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#architecture_body}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArchitecture_body(vhdlParser.Architecture_bodyContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#architecture_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArchitecture_declarative_part(vhdlParser.Architecture_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#architecture_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArchitecture_statement(vhdlParser.Architecture_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#architecture_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArchitecture_statement_part(vhdlParser.Architecture_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#array_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray_nature_definition(vhdlParser.Array_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#array_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray_type_definition(vhdlParser.Array_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#assertion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssertion(vhdlParser.AssertionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#assertion_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssertion_statement(vhdlParser.Assertion_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#association_element}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssociation_element(vhdlParser.Association_elementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#association_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssociation_list(vhdlParser.Association_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#attribute_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttribute_declaration(vhdlParser.Attribute_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#attribute_designator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttribute_designator(vhdlParser.Attribute_designatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#attribute_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttribute_specification(vhdlParser.Attribute_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#base_unit_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBase_unit_declaration(vhdlParser.Base_unit_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#binding_indication}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBinding_indication(vhdlParser.Binding_indicationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_configuration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_configuration(vhdlParser.Block_configurationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_declarative_item(vhdlParser.Block_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_declarative_part(vhdlParser.Block_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_header}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_header(vhdlParser.Block_headerContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_specification(vhdlParser.Block_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_statement(vhdlParser.Block_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#block_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_statement_part(vhdlParser.Block_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#branch_quantity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBranch_quantity_declaration(vhdlParser.Branch_quantity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#break_element}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreak_element(vhdlParser.Break_elementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#break_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreak_list(vhdlParser.Break_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#break_selector_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreak_selector_clause(vhdlParser.Break_selector_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#break_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreak_statement(vhdlParser.Break_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#case_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCase_statement(vhdlParser.Case_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#case_statement_alternative}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCase_statement_alternative(vhdlParser.Case_statement_alternativeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#choice}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChoice(vhdlParser.ChoiceContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#choices}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChoices(vhdlParser.ChoicesContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#component_configuration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_configuration(vhdlParser.Component_configurationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#component_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_declaration(vhdlParser.Component_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#component_instantiation_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_instantiation_statement(vhdlParser.Component_instantiation_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#component_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_specification(vhdlParser.Component_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#composite_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComposite_nature_definition(vhdlParser.Composite_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#composite_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComposite_type_definition(vhdlParser.Composite_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#concurrent_assertion_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConcurrent_assertion_statement(vhdlParser.Concurrent_assertion_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#concurrent_break_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConcurrent_break_statement(vhdlParser.Concurrent_break_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#concurrent_procedure_call_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConcurrent_procedure_call_statement(vhdlParser.Concurrent_procedure_call_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#concurrent_signal_assignment_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConcurrent_signal_assignment_statement(vhdlParser.Concurrent_signal_assignment_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#condition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCondition(vhdlParser.ConditionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#condition_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCondition_clause(vhdlParser.Condition_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#conditional_signal_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConditional_signal_assignment(vhdlParser.Conditional_signal_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#conditional_waveforms}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConditional_waveforms(vhdlParser.Conditional_waveformsContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#configuration_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfiguration_declaration(vhdlParser.Configuration_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#configuration_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfiguration_declarative_item(vhdlParser.Configuration_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#configuration_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfiguration_declarative_part(vhdlParser.Configuration_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#configuration_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfiguration_item(vhdlParser.Configuration_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#configuration_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfiguration_specification(vhdlParser.Configuration_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#constant_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_declaration(vhdlParser.Constant_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#constrained_array_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstrained_array_definition(vhdlParser.Constrained_array_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#constrained_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstrained_nature_definition(vhdlParser.Constrained_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#constraint}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstraint(vhdlParser.ConstraintContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#context_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContext_clause(vhdlParser.Context_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#context_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContext_item(vhdlParser.Context_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#delay_mechanism}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay_mechanism(vhdlParser.Delay_mechanismContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#design_file}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDesign_file(vhdlParser.Design_fileContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#design_unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDesign_unit(vhdlParser.Design_unitContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#designator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDesignator(vhdlParser.DesignatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#direction}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDirection(vhdlParser.DirectionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#disconnection_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDisconnection_specification(vhdlParser.Disconnection_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#discrete_range}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDiscrete_range(vhdlParser.Discrete_rangeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#element_association}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElement_association(vhdlParser.Element_associationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#element_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElement_declaration(vhdlParser.Element_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#element_subnature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElement_subnature_definition(vhdlParser.Element_subnature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#element_subtype_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElement_subtype_definition(vhdlParser.Element_subtype_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_aspect(vhdlParser.Entity_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_class}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_class(vhdlParser.Entity_classContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_class_entry}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_class_entry(vhdlParser.Entity_class_entryContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_class_entry_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_class_entry_list(vhdlParser.Entity_class_entry_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_declaration(vhdlParser.Entity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_declarative_item(vhdlParser.Entity_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_declarative_part(vhdlParser.Entity_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_designator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_designator(vhdlParser.Entity_designatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_header}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_header(vhdlParser.Entity_headerContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_name_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_name_list(vhdlParser.Entity_name_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_specification(vhdlParser.Entity_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_statement(vhdlParser.Entity_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_statement_part(vhdlParser.Entity_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#entity_tag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEntity_tag(vhdlParser.Entity_tagContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#enumeration_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnumeration_literal(vhdlParser.Enumeration_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#enumeration_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnumeration_type_definition(vhdlParser.Enumeration_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#exit_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExit_statement(vhdlParser.Exit_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression(vhdlParser.ExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#factor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFactor(vhdlParser.FactorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#file_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFile_declaration(vhdlParser.File_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#file_logical_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFile_logical_name(vhdlParser.File_logical_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#file_open_information}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFile_open_information(vhdlParser.File_open_informationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#file_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFile_type_definition(vhdlParser.File_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#formal_parameter_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFormal_parameter_list(vhdlParser.Formal_parameter_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#formal_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFormal_part(vhdlParser.Formal_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#free_quantity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFree_quantity_declaration(vhdlParser.Free_quantity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#generate_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_statement(vhdlParser.Generate_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#generation_scheme}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGeneration_scheme(vhdlParser.Generation_schemeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#generic_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGeneric_clause(vhdlParser.Generic_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#generic_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGeneric_list(vhdlParser.Generic_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#generic_map_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGeneric_map_aspect(vhdlParser.Generic_map_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#group_constituent}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroup_constituent(vhdlParser.Group_constituentContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#group_constituent_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroup_constituent_list(vhdlParser.Group_constituent_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#group_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroup_declaration(vhdlParser.Group_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#group_template_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroup_template_declaration(vhdlParser.Group_template_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#guarded_signal_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGuarded_signal_specification(vhdlParser.Guarded_signal_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdentifier(vhdlParser.IdentifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#identifier_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdentifier_list(vhdlParser.Identifier_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#if_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIf_statement(vhdlParser.If_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#index_constraint}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_constraint(vhdlParser.Index_constraintContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#index_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_specification(vhdlParser.Index_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#index_subtype_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_subtype_definition(vhdlParser.Index_subtype_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#instantiated_unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstantiated_unit(vhdlParser.Instantiated_unitContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#instantiation_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstantiation_list(vhdlParser.Instantiation_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_constant_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_constant_declaration(vhdlParser.Interface_constant_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_declaration(vhdlParser.Interface_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_element}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_element(vhdlParser.Interface_elementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_file_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_file_declaration(vhdlParser.Interface_file_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_signal_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_signal_list(vhdlParser.Interface_signal_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_port_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_port_list(vhdlParser.Interface_port_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_list(vhdlParser.Interface_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_quantity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_quantity_declaration(vhdlParser.Interface_quantity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_port_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_port_declaration(vhdlParser.Interface_port_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_signal_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_signal_declaration(vhdlParser.Interface_signal_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_terminal_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_terminal_declaration(vhdlParser.Interface_terminal_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#interface_variable_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInterface_variable_declaration(vhdlParser.Interface_variable_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#iteration_scheme}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIteration_scheme(vhdlParser.Iteration_schemeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#label_colon}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLabel_colon(vhdlParser.Label_colonContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#library_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLibrary_clause(vhdlParser.Library_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#library_unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLibrary_unit(vhdlParser.Library_unitContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiteral(vhdlParser.LiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#logical_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogical_name(vhdlParser.Logical_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#logical_name_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogical_name_list(vhdlParser.Logical_name_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#logical_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogical_operator(vhdlParser.Logical_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#loop_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLoop_statement(vhdlParser.Loop_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signal_mode}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_mode(vhdlParser.Signal_modeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#multiplying_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplying_operator(vhdlParser.Multiplying_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName(vhdlParser.NameContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#name_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_part(vhdlParser.Name_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#name_attribute_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_attribute_part(vhdlParser.Name_attribute_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#name_function_call_or_indexed_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_function_call_or_indexed_part(vhdlParser.Name_function_call_or_indexed_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#name_slice_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_slice_part(vhdlParser.Name_slice_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#selected_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSelected_name(vhdlParser.Selected_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#nature_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNature_declaration(vhdlParser.Nature_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNature_definition(vhdlParser.Nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#nature_element_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNature_element_declaration(vhdlParser.Nature_element_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#next_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNext_statement(vhdlParser.Next_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#numeric_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumeric_literal(vhdlParser.Numeric_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#object_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitObject_declaration(vhdlParser.Object_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#opts}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOpts(vhdlParser.OptsContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_body}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_body(vhdlParser.Package_bodyContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_body_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_body_declarative_item(vhdlParser.Package_body_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_body_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_body_declarative_part(vhdlParser.Package_body_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_declaration(vhdlParser.Package_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_declarative_item(vhdlParser.Package_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#package_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPackage_declarative_part(vhdlParser.Package_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#parameter_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_specification(vhdlParser.Parameter_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#physical_literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPhysical_literal(vhdlParser.Physical_literalContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#physical_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPhysical_type_definition(vhdlParser.Physical_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#port_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_clause(vhdlParser.Port_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#port_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_list(vhdlParser.Port_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#port_map_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_map_aspect(vhdlParser.Port_map_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimary(vhdlParser.PrimaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#primary_unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimary_unit(vhdlParser.Primary_unitContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedural_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedural_declarative_item(vhdlParser.Procedural_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedural_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedural_declarative_part(vhdlParser.Procedural_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedural_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedural_statement_part(vhdlParser.Procedural_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedure_call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedure_call(vhdlParser.Procedure_callContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedure_call_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedure_call_statement(vhdlParser.Procedure_call_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#process_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess_declarative_item(vhdlParser.Process_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#process_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess_declarative_part(vhdlParser.Process_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#process_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess_statement(vhdlParser.Process_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#process_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcess_statement_part(vhdlParser.Process_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#qualified_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQualified_expression(vhdlParser.Qualified_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#quantity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuantity_declaration(vhdlParser.Quantity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#quantity_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuantity_list(vhdlParser.Quantity_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#quantity_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuantity_specification(vhdlParser.Quantity_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#range}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange(vhdlParser.RangeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#explicit_range}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExplicit_range(vhdlParser.Explicit_rangeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#range_constraint}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange_constraint(vhdlParser.Range_constraintContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#record_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRecord_nature_definition(vhdlParser.Record_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#record_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRecord_type_definition(vhdlParser.Record_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#relation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelation(vhdlParser.RelationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#relational_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelational_operator(vhdlParser.Relational_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#report_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReport_statement(vhdlParser.Report_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#return_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReturn_statement(vhdlParser.Return_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#scalar_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitScalar_nature_definition(vhdlParser.Scalar_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#scalar_type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitScalar_type_definition(vhdlParser.Scalar_type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#secondary_unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSecondary_unit(vhdlParser.Secondary_unitContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#secondary_unit_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSecondary_unit_declaration(vhdlParser.Secondary_unit_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#selected_signal_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSelected_signal_assignment(vhdlParser.Selected_signal_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#selected_waveforms}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSelected_waveforms(vhdlParser.Selected_waveformsContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#sensitivity_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSensitivity_clause(vhdlParser.Sensitivity_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#sensitivity_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSensitivity_list(vhdlParser.Sensitivity_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#sequence_of_statements}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSequence_of_statements(vhdlParser.Sequence_of_statementsContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#sequential_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSequential_statement(vhdlParser.Sequential_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#shift_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitShift_expression(vhdlParser.Shift_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#shift_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitShift_operator(vhdlParser.Shift_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signal_assignment_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_assignment_statement(vhdlParser.Signal_assignment_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signal_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_declaration(vhdlParser.Signal_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signal_kind}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_kind(vhdlParser.Signal_kindContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signal_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_list(vhdlParser.Signal_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#signature}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignature(vhdlParser.SignatureContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simple_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_expression(vhdlParser.Simple_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simple_simultaneous_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_simultaneous_statement(vhdlParser.Simple_simultaneous_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_alternative}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_alternative(vhdlParser.Simultaneous_alternativeContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_case_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_case_statement(vhdlParser.Simultaneous_case_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_if_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_if_statement(vhdlParser.Simultaneous_if_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_procedural_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_procedural_statement(vhdlParser.Simultaneous_procedural_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_statement(vhdlParser.Simultaneous_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#simultaneous_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimultaneous_statement_part(vhdlParser.Simultaneous_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#source_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSource_aspect(vhdlParser.Source_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#source_quantity_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSource_quantity_declaration(vhdlParser.Source_quantity_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#step_limit_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStep_limit_specification(vhdlParser.Step_limit_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subnature_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubnature_declaration(vhdlParser.Subnature_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subnature_indication}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubnature_indication(vhdlParser.Subnature_indicationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_body}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_body(vhdlParser.Subprogram_bodyContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_declaration(vhdlParser.Subprogram_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_declarative_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_declarative_item(vhdlParser.Subprogram_declarative_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_declarative_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_declarative_part(vhdlParser.Subprogram_declarative_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_kind}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_kind(vhdlParser.Subprogram_kindContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_specification(vhdlParser.Subprogram_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#procedure_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedure_specification(vhdlParser.Procedure_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#function_specification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_specification(vhdlParser.Function_specificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subprogram_statement_part}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubprogram_statement_part(vhdlParser.Subprogram_statement_partContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subtype_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubtype_declaration(vhdlParser.Subtype_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#subtype_indication}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubtype_indication(vhdlParser.Subtype_indicationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#suffix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSuffix(vhdlParser.SuffixContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#target}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTarget(vhdlParser.TargetContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(vhdlParser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#terminal_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerminal_aspect(vhdlParser.Terminal_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#terminal_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerminal_declaration(vhdlParser.Terminal_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#through_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitThrough_aspect(vhdlParser.Through_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#timeout_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTimeout_clause(vhdlParser.Timeout_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#tolerance_aspect}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTolerance_aspect(vhdlParser.Tolerance_aspectContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#type_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitType_declaration(vhdlParser.Type_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#type_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitType_definition(vhdlParser.Type_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#unconstrained_array_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnconstrained_array_definition(vhdlParser.Unconstrained_array_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#unconstrained_nature_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnconstrained_nature_definition(vhdlParser.Unconstrained_nature_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#use_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUse_clause(vhdlParser.Use_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#variable_assignment_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_assignment_statement(vhdlParser.Variable_assignment_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#variable_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_declaration(vhdlParser.Variable_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#wait_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWait_statement(vhdlParser.Wait_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#waveform}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWaveform(vhdlParser.WaveformContext ctx);
	/**
	 * Visit a parse tree produced by {@link vhdlParser#waveform_element}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWaveform_element(vhdlParser.Waveform_elementContext ctx);
}