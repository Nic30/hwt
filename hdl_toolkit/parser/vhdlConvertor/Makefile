
all:
	rm -f hdlConvertor.jar
	java -Xmx500M -cp "./lib/antlr-4.5.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool -visitor vhdl.g4 -o vhdlParser -package vhdlParser
	java -Xmx500M -cp "./lib/antlr-4.5.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool -visitor Verilog2001.g4 -o verilogParser -package verilogParser
	javac -classpath lib/*:.                        hdlObjects/*.java vhdlParser/*.java  vhdlConvertor/*.java verilogConvertor/*.java verilogParser/*.java convertorApp/*.java
	jar mvcf META-INF/MANIFEST.MF hdlConvertor.jar  hdlObjects/*      vhdlParser/*       vhdlConvertor/*      verilogConvertor/*      verilogParser/*      convertorApp/*

