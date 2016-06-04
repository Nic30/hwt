package convertorApp;
import org.antlr.v4.runtime.BaseErrorListener;

public class SyntaxErrorLogger extends BaseErrorListener {

	@Override
	public void syntaxError(org.antlr.v4.runtime.Recognizer<?, ?> recognizer,
			Object offendingSymbol, int line, int charPositionInLine,
			String msg, org.antlr.v4.runtime.RecognitionException e) {

		String sourceName = recognizer.getInputStream().getSourceName();
		if (!sourceName.isEmpty()) {
			sourceName = String.format("%s:%d:%d: ", sourceName, line,
					charPositionInLine);
		}

		System.err.println(sourceName + " " + msg);

	};

}
