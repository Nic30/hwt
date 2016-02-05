package vhdlConvertor;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

//import ANTLR's runtime libraries
import org.antlr.v4.runtime.*;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import vhdlParser.vhdlLexer;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.Design_fileContext;

public class vhdlConvertorApp {
	public static void main(String[] args) throws Exception {
		Options options = new Options();
		options.addOption("p", "pretty", false, "pretty print for output json");
		options.addOption("d", "debug", false, "debug");

		CommandLineParser cliParser = new DefaultParser();
		try {
			CommandLine line = cliParser.parse(options, args);
			
			Path file = Paths.get(line.getArgList().get(0));
			boolean prettyPrint = line.hasOption("pretty");
			NotImplementedLogger.doLog = line.hasOption("d");

			try (BufferedReader reader = Files.newBufferedReader(file,
					Charset.forName("UTF-8"))) {

				// create a CharStream that reads from standard input
				ANTLRInputStream input = new ANTLRInputStream(reader);

				// create a lexer that feeds off of input CharStream
				vhdlLexer lexer = new vhdlLexer(input);

				// create a buffer of tokens pulled from the lexer
				CommonTokenStream tokens = new CommonTokenStream(lexer);

				// create a parser that feeds off the tokens buffer
				vhdlParser parser = new vhdlParser(tokens);
				Design_fileContext tree = parser.design_file(); // begin parsing
																// at
																// init rule
				DesignFileParser p = new DesignFileParser();
				p.visitDesign_file(tree);
				if (prettyPrint) {
					System.out.print(p.context.toJson().toString(4));
				} else {
					System.out.print(p.context.toJson());
				}
			} catch (IOException x) {
				System.err.format("IOException: %s\n", x);
			}
		} catch (ParseException exp) {
			System.err.println(
					"Parsing cli args failed.  Reason: " + exp.getMessage());
			HelpFormatter formatter = new HelpFormatter();
			formatter.printHelp("vhdlConvertorApp", options);

			System.exit(1);
		}

	}
}