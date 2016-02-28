
all:
	rm -f vhdlConvertor.jar
	java -Xmx500M -cp "./lib/antlr-4.5.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool -visitor vhdl.g4 -o vhdlParser -package vhdlParser
	javac -classpath lib/*:.  vhdlParser/*.java vhdlObjects/*.java vhdlConvertor/*.java 
	jar mvcf META-INF/MANIFEST.MF vhdlConvertor.jar  vhdlConvertor/*   vhdlParser/* vhdlObjects/*

