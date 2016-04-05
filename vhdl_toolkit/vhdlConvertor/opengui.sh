
# use vhdl file as argument of this script
export CLASSPATH=".:lib/antlr-4.5.1-complete.jar:$CLASSPATH"
designFile=$1

errMsg () { 
   echo "Can not resolve hdl langue from file extension use .vhd or .v"
}

if [[ $designFile == *.vhd ]]; then
    java org.antlr.v4.gui.TestRig vhdlParser.vhdl design_file $1 -gui
else
    if [[ $designFile == *.v ]]; then
        java org.antlr.v4.gui.TestRig verilogParser.Verilog2001 source_text $1 -gui
    else
        errMsg
    fi
fi 
