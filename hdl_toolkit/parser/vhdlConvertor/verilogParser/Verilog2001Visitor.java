// Generated from Verilog2001.g4 by ANTLR 4.5.1
package verilogParser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link Verilog2001Parser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface Verilog2001Visitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#config_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfig_declaration(Verilog2001Parser.Config_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#design_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDesign_statement(Verilog2001Parser.Design_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#config_rule_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfig_rule_statement(Verilog2001Parser.Config_rule_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#default_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDefault_clause(Verilog2001Parser.Default_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#inst_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInst_clause(Verilog2001Parser.Inst_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#inst_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInst_name(Verilog2001Parser.Inst_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#liblist_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiblist_clause(Verilog2001Parser.Liblist_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#cell_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCell_clause(Verilog2001Parser.Cell_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#use_clause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUse_clause(Verilog2001Parser.Use_clauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#source_text}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSource_text(Verilog2001Parser.Source_textContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#description}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDescription(Verilog2001Parser.DescriptionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_declaration(Verilog2001Parser.Module_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_keyword}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_keyword(Verilog2001Parser.Module_keywordContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_parameter_port_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_parameter_port_list(Verilog2001Parser.Module_parameter_port_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_ports}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_ports(Verilog2001Parser.List_of_portsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_port_declarations}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_port_declarations(Verilog2001Parser.List_of_port_declarationsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#port}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort(Verilog2001Parser.PortContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#port_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_expression(Verilog2001Parser.Port_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#port_reference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_reference(Verilog2001Parser.Port_referenceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#port_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_declaration(Verilog2001Parser.Port_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_item(Verilog2001Parser.Module_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_or_generate_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_or_generate_item(Verilog2001Parser.Module_or_generate_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#non_port_module_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNon_port_module_item(Verilog2001Parser.Non_port_module_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_or_generate_item_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_or_generate_item_declaration(Verilog2001Parser.Module_or_generate_item_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parameter_override}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_override(Verilog2001Parser.Parameter_overrideContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#local_parameter_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLocal_parameter_declaration(Verilog2001Parser.Local_parameter_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parameter_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_declaration(Verilog2001Parser.Parameter_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parameter_declaration_}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_declaration_(Verilog2001Parser.Parameter_declaration_Context ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specparam_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecparam_declaration(Verilog2001Parser.Specparam_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#inout_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInout_declaration(Verilog2001Parser.Inout_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#input_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInput_declaration(Verilog2001Parser.Input_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#output_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_declaration(Verilog2001Parser.Output_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_declaration(Verilog2001Parser.Event_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_declaration(Verilog2001Parser.Genvar_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#integer_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInteger_declaration(Verilog2001Parser.Integer_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#time_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTime_declaration(Verilog2001Parser.Time_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#real_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReal_declaration(Verilog2001Parser.Real_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#realtime_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRealtime_declaration(Verilog2001Parser.Realtime_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#reg_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReg_declaration(Verilog2001Parser.Reg_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_declaration(Verilog2001Parser.Net_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_type(Verilog2001Parser.Net_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#output_variable_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_variable_type(Verilog2001Parser.Output_variable_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#real_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReal_type(Verilog2001Parser.Real_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_type(Verilog2001Parser.Variable_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#drive_strength}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDrive_strength(Verilog2001Parser.Drive_strengthContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#strength0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStrength0(Verilog2001Parser.Strength0Context ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#strength1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStrength1(Verilog2001Parser.Strength1Context ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#charge_strength}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCharge_strength(Verilog2001Parser.Charge_strengthContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delay3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay3(Verilog2001Parser.Delay3Context ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delay2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay2(Verilog2001Parser.Delay2Context ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delay_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay_value(Verilog2001Parser.Delay_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_event_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_event_identifiers(Verilog2001Parser.List_of_event_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_net_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_net_identifiers(Verilog2001Parser.List_of_net_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_genvar_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_genvar_identifiers(Verilog2001Parser.List_of_genvar_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_port_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_port_identifiers(Verilog2001Parser.List_of_port_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_net_decl_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_net_decl_assignments(Verilog2001Parser.List_of_net_decl_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_param_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_param_assignments(Verilog2001Parser.List_of_param_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_specparam_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_specparam_assignments(Verilog2001Parser.List_of_specparam_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_real_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_real_identifiers(Verilog2001Parser.List_of_real_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_variable_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_variable_identifiers(Verilog2001Parser.List_of_variable_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_variable_port_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_variable_port_identifiers(Verilog2001Parser.List_of_variable_port_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_decl_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_decl_assignment(Verilog2001Parser.Net_decl_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#param_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParam_assignment(Verilog2001Parser.Param_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specparam_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecparam_assignment(Verilog2001Parser.Specparam_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pulse_control_specparam}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPulse_control_specparam(Verilog2001Parser.Pulse_control_specparamContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#error_limit_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitError_limit_value(Verilog2001Parser.Error_limit_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#reject_limit_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReject_limit_value(Verilog2001Parser.Reject_limit_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#limit_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLimit_value(Verilog2001Parser.Limit_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#dimension}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDimension(Verilog2001Parser.DimensionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#range}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange(Verilog2001Parser.RangeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_declaration(Verilog2001Parser.Function_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_item_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_item_declaration(Verilog2001Parser.Function_item_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_port_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_port_list(Verilog2001Parser.Function_port_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_port}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_port(Verilog2001Parser.Function_portContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#range_or_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange_or_type(Verilog2001Parser.Range_or_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_declaration(Verilog2001Parser.Task_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_item_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_item_declaration(Verilog2001Parser.Task_item_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_port_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_port_list(Verilog2001Parser.Task_port_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_port_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_port_item(Verilog2001Parser.Task_port_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tf_decl_header}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTf_decl_header(Verilog2001Parser.Tf_decl_headerContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tf_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTf_declaration(Verilog2001Parser.Tf_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_port_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_port_type(Verilog2001Parser.Task_port_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#block_item_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_item_declaration(Verilog2001Parser.Block_item_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#block_reg_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_reg_declaration(Verilog2001Parser.Block_reg_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_block_variable_identifiers}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_block_variable_identifiers(Verilog2001Parser.List_of_block_variable_identifiersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#block_variable_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_variable_type(Verilog2001Parser.Block_variable_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#gate_instantiation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGate_instantiation(Verilog2001Parser.Gate_instantiationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#cmos_switch_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCmos_switch_instance(Verilog2001Parser.Cmos_switch_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#enable_gate_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnable_gate_instance(Verilog2001Parser.Enable_gate_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#mos_switch_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMos_switch_instance(Verilog2001Parser.Mos_switch_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#n_input_gate_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitN_input_gate_instance(Verilog2001Parser.N_input_gate_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#n_output_gate_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitN_output_gate_instance(Verilog2001Parser.N_output_gate_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pass_switch_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPass_switch_instance(Verilog2001Parser.Pass_switch_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pass_enable_switch_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPass_enable_switch_instance(Verilog2001Parser.Pass_enable_switch_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pull_gate_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPull_gate_instance(Verilog2001Parser.Pull_gate_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#name_of_gate_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_of_gate_instance(Verilog2001Parser.Name_of_gate_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pulldown_strength}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPulldown_strength(Verilog2001Parser.Pulldown_strengthContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pullup_strength}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPullup_strength(Verilog2001Parser.Pullup_strengthContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#enable_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnable_terminal(Verilog2001Parser.Enable_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#ncontrol_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNcontrol_terminal(Verilog2001Parser.Ncontrol_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pcontrol_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPcontrol_terminal(Verilog2001Parser.Pcontrol_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#input_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInput_terminal(Verilog2001Parser.Input_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#inout_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInout_terminal(Verilog2001Parser.Inout_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#output_terminal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_terminal(Verilog2001Parser.Output_terminalContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#cmos_switchtype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCmos_switchtype(Verilog2001Parser.Cmos_switchtypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#enable_gatetype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnable_gatetype(Verilog2001Parser.Enable_gatetypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#mos_switchtype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMos_switchtype(Verilog2001Parser.Mos_switchtypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#n_input_gatetype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitN_input_gatetype(Verilog2001Parser.N_input_gatetypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#n_output_gatetype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitN_output_gatetype(Verilog2001Parser.N_output_gatetypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pass_en_switchtype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPass_en_switchtype(Verilog2001Parser.Pass_en_switchtypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pass_switchtype}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPass_switchtype(Verilog2001Parser.Pass_switchtypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_instantiation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_instantiation(Verilog2001Parser.Module_instantiationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parameter_value_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_value_assignment(Verilog2001Parser.Parameter_value_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_parameter_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_parameter_assignments(Verilog2001Parser.List_of_parameter_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#ordered_parameter_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOrdered_parameter_assignment(Verilog2001Parser.Ordered_parameter_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#named_parameter_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNamed_parameter_assignment(Verilog2001Parser.Named_parameter_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_instance(Verilog2001Parser.Module_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#name_of_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitName_of_instance(Verilog2001Parser.Name_of_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_port_connections}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_port_connections(Verilog2001Parser.List_of_port_connectionsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#ordered_port_connection}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOrdered_port_connection(Verilog2001Parser.Ordered_port_connectionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#named_port_connection}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNamed_port_connection(Verilog2001Parser.Named_port_connectionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generated_instantiation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerated_instantiation(Verilog2001Parser.Generated_instantiationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_item_or_null}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_item_or_null(Verilog2001Parser.Generate_item_or_nullContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_item(Verilog2001Parser.Generate_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_conditional_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_conditional_statement(Verilog2001Parser.Generate_conditional_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_case_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_case_statement(Verilog2001Parser.Generate_case_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_case_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_case_item(Verilog2001Parser.Genvar_case_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_loop_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_loop_statement(Verilog2001Parser.Generate_loop_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_assignment(Verilog2001Parser.Genvar_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_block(Verilog2001Parser.Generate_blockContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#continuous_assign}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContinuous_assign(Verilog2001Parser.Continuous_assignContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_net_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_net_assignments(Verilog2001Parser.List_of_net_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_assignment(Verilog2001Parser.Net_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#initial_construct}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInitial_construct(Verilog2001Parser.Initial_constructContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#always_construct}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAlways_construct(Verilog2001Parser.Always_constructContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#blocking_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlocking_assignment(Verilog2001Parser.Blocking_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#nonblocking_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNonblocking_assignment(Verilog2001Parser.Nonblocking_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#procedural_continuous_assignments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedural_continuous_assignments(Verilog2001Parser.Procedural_continuous_assignmentsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_blocking_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_blocking_assignment(Verilog2001Parser.Function_blocking_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_statement_or_null}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_statement_or_null(Verilog2001Parser.Function_statement_or_nullContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_seq_block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_seq_block(Verilog2001Parser.Function_seq_blockContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_assignment(Verilog2001Parser.Variable_assignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#par_block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPar_block(Verilog2001Parser.Par_blockContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#seq_block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_block(Verilog2001Parser.Seq_blockContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStatement(Verilog2001Parser.StatementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#statement_or_null}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStatement_or_null(Verilog2001Parser.Statement_or_nullContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_statement(Verilog2001Parser.Function_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delay_or_event_control}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay_or_event_control(Verilog2001Parser.Delay_or_event_controlContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delay_control}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelay_control(Verilog2001Parser.Delay_controlContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#disable_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDisable_statement(Verilog2001Parser.Disable_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_control}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_control(Verilog2001Parser.Event_controlContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_trigger}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_trigger(Verilog2001Parser.Event_triggerContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_expression(Verilog2001Parser.Event_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_primary(Verilog2001Parser.Event_primaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#procedural_timing_control_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedural_timing_control_statement(Verilog2001Parser.Procedural_timing_control_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#wait_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWait_statement(Verilog2001Parser.Wait_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#conditional_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConditional_statement(Verilog2001Parser.Conditional_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#if_else_if_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIf_else_if_statement(Verilog2001Parser.If_else_if_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_conditional_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_conditional_statement(Verilog2001Parser.Function_conditional_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_if_else_if_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_if_else_if_statement(Verilog2001Parser.Function_if_else_if_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#case_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCase_statement(Verilog2001Parser.Case_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#case_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCase_item(Verilog2001Parser.Case_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_case_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_case_statement(Verilog2001Parser.Function_case_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_case_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_case_item(Verilog2001Parser.Function_case_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_loop_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_loop_statement(Verilog2001Parser.Function_loop_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#loop_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLoop_statement(Verilog2001Parser.Loop_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#system_task_enable}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSystem_task_enable(Verilog2001Parser.System_task_enableContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_enable}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_enable(Verilog2001Parser.Task_enableContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specify_block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecify_block(Verilog2001Parser.Specify_blockContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specify_item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecify_item(Verilog2001Parser.Specify_itemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#pulsestyle_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPulsestyle_declaration(Verilog2001Parser.Pulsestyle_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#showcancelled_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitShowcancelled_declaration(Verilog2001Parser.Showcancelled_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#path_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPath_declaration(Verilog2001Parser.Path_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#simple_path_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_path_declaration(Verilog2001Parser.Simple_path_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parallel_path_description}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParallel_path_description(Verilog2001Parser.Parallel_path_descriptionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#full_path_description}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFull_path_description(Verilog2001Parser.Full_path_descriptionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_path_inputs}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_path_inputs(Verilog2001Parser.List_of_path_inputsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_path_outputs}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_path_outputs(Verilog2001Parser.List_of_path_outputsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specify_input_terminal_descriptor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecify_input_terminal_descriptor(Verilog2001Parser.Specify_input_terminal_descriptorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specify_output_terminal_descriptor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecify_output_terminal_descriptor(Verilog2001Parser.Specify_output_terminal_descriptorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#input_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInput_identifier(Verilog2001Parser.Input_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#output_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_identifier(Verilog2001Parser.Output_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#path_delay_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPath_delay_value(Verilog2001Parser.Path_delay_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#list_of_path_delay_expressions}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitList_of_path_delay_expressions(Verilog2001Parser.List_of_path_delay_expressionsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT_path_delay_expression(Verilog2001Parser.T_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#trise_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTrise_path_delay_expression(Verilog2001Parser.Trise_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tfall_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTfall_path_delay_expression(Verilog2001Parser.Tfall_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tz_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTz_path_delay_expression(Verilog2001Parser.Tz_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t01_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT01_path_delay_expression(Verilog2001Parser.T01_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t10_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT10_path_delay_expression(Verilog2001Parser.T10_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t0z_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT0z_path_delay_expression(Verilog2001Parser.T0z_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tz1_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTz1_path_delay_expression(Verilog2001Parser.Tz1_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t1z_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT1z_path_delay_expression(Verilog2001Parser.T1z_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tz0_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTz0_path_delay_expression(Verilog2001Parser.Tz0_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t0x_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT0x_path_delay_expression(Verilog2001Parser.T0x_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tx1_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTx1_path_delay_expression(Verilog2001Parser.Tx1_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#t1x_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitT1x_path_delay_expression(Verilog2001Parser.T1x_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tx0_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTx0_path_delay_expression(Verilog2001Parser.Tx0_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#txz_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTxz_path_delay_expression(Verilog2001Parser.Txz_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#tzx_path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTzx_path_delay_expression(Verilog2001Parser.Tzx_path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#path_delay_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPath_delay_expression(Verilog2001Parser.Path_delay_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#edge_sensitive_path_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEdge_sensitive_path_declaration(Verilog2001Parser.Edge_sensitive_path_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parallel_edge_sensitive_path_description}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParallel_edge_sensitive_path_description(Verilog2001Parser.Parallel_edge_sensitive_path_descriptionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#full_edge_sensitive_path_description}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFull_edge_sensitive_path_description(Verilog2001Parser.Full_edge_sensitive_path_descriptionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#data_source_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitData_source_expression(Verilog2001Parser.Data_source_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#edge_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEdge_identifier(Verilog2001Parser.Edge_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#state_dependent_path_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitState_dependent_path_declaration(Verilog2001Parser.State_dependent_path_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#polarity_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPolarity_operator(Verilog2001Parser.Polarity_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#checktime_condition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChecktime_condition(Verilog2001Parser.Checktime_conditionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delayed_data}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelayed_data(Verilog2001Parser.Delayed_dataContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#delayed_reference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelayed_reference(Verilog2001Parser.Delayed_referenceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#end_edge_offset}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnd_edge_offset(Verilog2001Parser.End_edge_offsetContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_based_flag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_based_flag(Verilog2001Parser.Event_based_flagContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#notify_reg}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNotify_reg(Verilog2001Parser.Notify_regContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#remain_active_flag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRemain_active_flag(Verilog2001Parser.Remain_active_flagContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#stamptime_condition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStamptime_condition(Verilog2001Parser.Stamptime_conditionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#start_edge_offset}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStart_edge_offset(Verilog2001Parser.Start_edge_offsetContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#threshold}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitThreshold(Verilog2001Parser.ThresholdContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#timing_check_limit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTiming_check_limit(Verilog2001Parser.Timing_check_limitContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConcatenation(Verilog2001Parser.ConcatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_concatenation(Verilog2001Parser.Constant_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_multiple_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_multiple_concatenation(Verilog2001Parser.Constant_multiple_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_concatenation(Verilog2001Parser.Module_path_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_multiple_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_multiple_concatenation(Verilog2001Parser.Module_path_multiple_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#multiple_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiple_concatenation(Verilog2001Parser.Multiple_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_concatenation(Verilog2001Parser.Net_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_concatenation_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_concatenation_value(Verilog2001Parser.Net_concatenation_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_concatenation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_concatenation(Verilog2001Parser.Variable_concatenationContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_concatenation_value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_concatenation_value(Verilog2001Parser.Variable_concatenation_valueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_function_call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_function_call(Verilog2001Parser.Constant_function_callContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_call(Verilog2001Parser.Function_callContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#system_function_call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSystem_function_call(Verilog2001Parser.System_function_callContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_function_call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_function_call(Verilog2001Parser.Genvar_function_callContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#base_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBase_expression(Verilog2001Parser.Base_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_base_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_base_expression(Verilog2001Parser.Constant_base_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_expression(Verilog2001Parser.Constant_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_mintypmax_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_mintypmax_expression(Verilog2001Parser.Constant_mintypmax_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_range_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_range_expression(Verilog2001Parser.Constant_range_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#dimension_constant_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDimension_constant_expression(Verilog2001Parser.Dimension_constant_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression(Verilog2001Parser.ExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(Verilog2001Parser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#lsb_constant_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLsb_constant_expression(Verilog2001Parser.Lsb_constant_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#mintypmax_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMintypmax_expression(Verilog2001Parser.Mintypmax_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_conditional_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_conditional_expression(Verilog2001Parser.Module_path_conditional_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_expression(Verilog2001Parser.Module_path_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_mintypmax_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_mintypmax_expression(Verilog2001Parser.Module_path_mintypmax_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#msb_constant_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMsb_constant_expression(Verilog2001Parser.Msb_constant_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#range_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange_expression(Verilog2001Parser.Range_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#width_constant_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWidth_constant_expression(Verilog2001Parser.Width_constant_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#constant_primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstant_primary(Verilog2001Parser.Constant_primaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_path_primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_path_primary(Verilog2001Parser.Module_path_primaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimary(Verilog2001Parser.PrimaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_lvalue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_lvalue(Verilog2001Parser.Net_lvalueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_lvalue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_lvalue(Verilog2001Parser.Variable_lvalueContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#unary_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnary_operator(Verilog2001Parser.Unary_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#binary_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBinary_operator(Verilog2001Parser.Binary_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#unary_module_path_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnary_module_path_operator(Verilog2001Parser.Unary_module_path_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#binary_module_path_operator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBinary_module_path_operator(Verilog2001Parser.Binary_module_path_operatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#number}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumber(Verilog2001Parser.NumberContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#default_nettype_spec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDefault_nettype_spec(Verilog2001Parser.Default_nettype_specContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#timing_spec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTiming_spec(Verilog2001Parser.Timing_specContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#attribute_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttribute_instance(Verilog2001Parser.Attribute_instanceContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#attr_spec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttr_spec(Verilog2001Parser.Attr_specContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#attr_name}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAttr_name(Verilog2001Parser.Attr_nameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#arrayed_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayed_identifier(Verilog2001Parser.Arrayed_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#block_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock_identifier(Verilog2001Parser.Block_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#cell_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCell_identifier(Verilog2001Parser.Cell_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#config_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfig_identifier(Verilog2001Parser.Config_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#escaped_arrayed_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEscaped_arrayed_identifier(Verilog2001Parser.Escaped_arrayed_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#escaped_hierarchical_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEscaped_hierarchical_identifier(Verilog2001Parser.Escaped_hierarchical_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#event_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvent_identifier(Verilog2001Parser.Event_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#function_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_identifier(Verilog2001Parser.Function_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#gate_instance_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGate_instance_identifier(Verilog2001Parser.Gate_instance_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#generate_block_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenerate_block_identifier(Verilog2001Parser.Generate_block_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_function_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_function_identifier(Verilog2001Parser.Genvar_function_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#genvar_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGenvar_identifier(Verilog2001Parser.Genvar_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_block_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_block_identifier(Verilog2001Parser.Hierarchical_block_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_event_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_event_identifier(Verilog2001Parser.Hierarchical_event_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_function_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_function_identifier(Verilog2001Parser.Hierarchical_function_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_identifier(Verilog2001Parser.Hierarchical_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_net_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_net_identifier(Verilog2001Parser.Hierarchical_net_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_variable_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_variable_identifier(Verilog2001Parser.Hierarchical_variable_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#hierarchical_task_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHierarchical_task_identifier(Verilog2001Parser.Hierarchical_task_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdentifier(Verilog2001Parser.IdentifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#inout_port_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInout_port_identifier(Verilog2001Parser.Inout_port_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#input_port_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInput_port_identifier(Verilog2001Parser.Input_port_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#instance_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstance_identifier(Verilog2001Parser.Instance_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#library_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLibrary_identifier(Verilog2001Parser.Library_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#memory_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMemory_identifier(Verilog2001Parser.Memory_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_identifier(Verilog2001Parser.Module_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#module_instance_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitModule_instance_identifier(Verilog2001Parser.Module_instance_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#net_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNet_identifier(Verilog2001Parser.Net_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#output_port_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_port_identifier(Verilog2001Parser.Output_port_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#parameter_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter_identifier(Verilog2001Parser.Parameter_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#port_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPort_identifier(Verilog2001Parser.Port_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#real_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReal_identifier(Verilog2001Parser.Real_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#simple_arrayed_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_arrayed_identifier(Verilog2001Parser.Simple_arrayed_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#simple_hierarchical_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_hierarchical_identifier(Verilog2001Parser.Simple_hierarchical_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#specparam_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecparam_identifier(Verilog2001Parser.Specparam_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#system_function_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSystem_function_identifier(Verilog2001Parser.System_function_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#system_task_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSystem_task_identifier(Verilog2001Parser.System_task_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#task_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTask_identifier(Verilog2001Parser.Task_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#terminal_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerminal_identifier(Verilog2001Parser.Terminal_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#text_macro_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitText_macro_identifier(Verilog2001Parser.Text_macro_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#topmodule_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTopmodule_identifier(Verilog2001Parser.Topmodule_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#udp_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUdp_identifier(Verilog2001Parser.Udp_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#udp_instance_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUdp_instance_identifier(Verilog2001Parser.Udp_instance_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#variable_identifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariable_identifier(Verilog2001Parser.Variable_identifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#simple_hierarchical_branch}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimple_hierarchical_branch(Verilog2001Parser.Simple_hierarchical_branchContext ctx);
	/**
	 * Visit a parse tree produced by {@link Verilog2001Parser#escaped_hierarchical_branch}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEscaped_hierarchical_branch(Verilog2001Parser.Escaped_hierarchical_branchContext ctx);
}