package vhdlConvertor;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

//import ANTLR's runtime libraries
import org.antlr.v4.runtime.*;

import vhdlParser.vhdlLexer;
import vhdlParser.vhdlParser;
import vhdlParser.vhdlParser.Design_fileContext;

public class vhdlConvertorApp {
	public static void main(String[] args) throws Exception {
		boolean prettyPrint = true;

		if (args.length != 1) {
			System.err.print("Can be used only with one source file\n");
			System.exit(1);
		}
		String fileName = args[0];

		Path file = Paths.get(fileName);

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
			Design_fileContext tree = parser.design_file(); // begin parsing at
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
	}
}