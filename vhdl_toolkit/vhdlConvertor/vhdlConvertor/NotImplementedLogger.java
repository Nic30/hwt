package vhdlConvertor;

public class NotImplementedLogger {
	public static boolean doLog = true;

	public static void print(Object msg) {
		if (doLog)
			System.err.println("NotImplemented " + String.valueOf(msg));
	}

}
