package vhdlConvertor;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.MalformedInputException;
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
		options.addOption("h", "hierarchy-only", false, "hierarchy-only");

		CommandLineParser cliParser = new DefaultParser();
		try {
			CommandLine line = cliParser.parse(options, args);
			String fileName = line.getArgList().get(0);
			Path file = Paths.get(fileName);
			boolean prettyPrint = line.hasOption("pretty");
			boolean hierarchyOnly = line.hasOption("h");
			NotImplementedLogger.doLog = line.hasOption("d");

			try (BufferedReader reader = Files.newBufferedReader(file,
					Charset.forName("UTF-8"))) {
				// create a CharStream that reads from standard input
				ANTLRInputStream input = new ANTLRInputStream(reader);
				input.name = fileName;
				// create a lexer that feeds off of input CharStream
				vhdlLexer lexer = new vhdlLexer(input);

				// create a buffer of tokens pulled from the lexer
				CommonTokenStream tokens = new CommonTokenStream(lexer);

				// create a parser that feeds off the tokens buffer
				vhdlParser parser = new vhdlParser(tokens);
				parser.removeErrorListeners();
				parser.addErrorListener(new SyntaxErrorLogger());
				// begin parsing at init rule
				Design_fileContext tree = parser.design_file();
				DesignFileParser p = new DesignFileParser(hierarchyOnly);
				p.visitDesign_file(tree);
				if (prettyPrint) {
					System.out.print(p.context.toJson().toString(4));
				} else {
					System.out.print(p.context.toJson());
				}
				System.out.print("done");
			} catch (Exception e) {
				if (e instanceof IOException) {
					System.err.format("IOException: %s\n", e);
					System.exit(1);
				} else if (e instanceof MalformedInputException) {
					System.err.format(
							"%s file %s is not parsable due encoding\n", e,
							file);
					System.exit(1);
				} else {
					throw e;
				}
			}
		} catch (ParseException exc) {
			System.err.println(
					"Parsing cli args failed.  Reason: " + exc.getMessage());
			HelpFormatter formatter = new HelpFormatter();
			formatter.printHelp("vhdlConvertorApp", options);

			System.exit(1);
		}

	}
}