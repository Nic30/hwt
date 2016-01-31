
# use vhdl file as argument of this script
export CLASSPATH=".:/usr/local/lib/antlr-4.5.1-complete.jar:$CLASSPATH"
java org.antlr.v4.gui.TestRig vhdlParser.vhdl design_file $1 -gui
