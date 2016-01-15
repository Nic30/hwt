# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from antlr4 import *
import numpy as np
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package) > 0 if package is not None else False
if ischild:
    from .vhdlListener import vhdlListener
else:
    from vhdlListener import vhdlListener
def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\u00a4")
        buf.write("\u0a24\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.\t.\4")
        buf.write("/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t\64")
        buf.write("\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t")
        buf.write(";\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\t")
        buf.write("D\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\tL\4M\t")
        buf.write("M\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\tU\4V\t")
        buf.write("V\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4^\t^\4")
        buf.write("_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4g\tg\4")
        buf.write("h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4p\tp\4")
        buf.write("q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4y\ty\4")
        buf.write("z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\4\u0080\t\u0080")
        buf.write("\4\u0081\t\u0081\4\u0082\t\u0082\4\u0083\t\u0083\4\u0084")
        buf.write("\t\u0084\4\u0085\t\u0085\4\u0086\t\u0086\4\u0087\t\u0087")
        buf.write("\4\u0088\t\u0088\4\u0089\t\u0089\4\u008a\t\u008a\4\u008b")
        buf.write("\t\u008b\4\u008c\t\u008c\4\u008d\t\u008d\4\u008e\t\u008e")
        buf.write("\4\u008f\t\u008f\4\u0090\t\u0090\4\u0091\t\u0091\4\u0092")
        buf.write("\t\u0092\4\u0093\t\u0093\4\u0094\t\u0094\4\u0095\t\u0095")
        buf.write("\4\u0096\t\u0096\4\u0097\t\u0097\4\u0098\t\u0098\4\u0099")
        buf.write("\t\u0099\4\u009a\t\u009a\4\u009b\t\u009b\4\u009c\t\u009c")
        buf.write("\4\u009d\t\u009d\4\u009e\t\u009e\4\u009f\t\u009f\4\u00a0")
        buf.write("\t\u00a0\4\u00a1\t\u00a1\4\u00a2\t\u00a2\4\u00a3\t\u00a3")
        buf.write("\4\u00a4\t\u00a4\4\u00a5\t\u00a5\4\u00a6\t\u00a6\4\u00a7")
        buf.write("\t\u00a7\4\u00a8\t\u00a8\4\u00a9\t\u00a9\4\u00aa\t\u00aa")
        buf.write("\4\u00ab\t\u00ab\4\u00ac\t\u00ac\4\u00ad\t\u00ad\4\u00ae")
        buf.write("\t\u00ae\4\u00af\t\u00af\4\u00b0\t\u00b0\4\u00b1\t\u00b1")
        buf.write("\4\u00b2\t\u00b2\4\u00b3\t\u00b3\4\u00b4\t\u00b4\4\u00b5")
        buf.write("\t\u00b5\4\u00b6\t\u00b6\4\u00b7\t\u00b7\4\u00b8\t\u00b8")
        buf.write("\4\u00b9\t\u00b9\4\u00ba\t\u00ba\4\u00bb\t\u00bb\4\u00bc")
        buf.write("\t\u00bc\4\u00bd\t\u00bd\4\u00be\t\u00be\4\u00bf\t\u00bf")
        buf.write("\4\u00c0\t\u00c0\4\u00c1\t\u00c1\4\u00c2\t\u00c2\4\u00c3")
        buf.write("\t\u00c3\4\u00c4\t\u00c4\4\u00c5\t\u00c5\4\u00c6\t\u00c6")
        buf.write("\4\u00c7\t\u00c7\4\u00c8\t\u00c8\4\u00c9\t\u00c9\4\u00ca")
        buf.write("\t\u00ca\4\u00cb\t\u00cb\4\u00cc\t\u00cc\4\u00cd\t\u00cd")
        buf.write("\4\u00ce\t\u00ce\4\u00cf\t\u00cf\4\u00d0\t\u00d0\4\u00d1")
        buf.write("\t\u00d1\4\u00d2\t\u00d2\4\u00d3\t\u00d3\4\u00d4\t\u00d4")
        buf.write("\4\u00d5\t\u00d5\4\u00d6\t\u00d6\4\u00d7\t\u00d7\4\u00d8")
        buf.write("\t\u00d8\4\u00d9\t\u00d9\4\u00da\t\u00da\4\u00db\t\u00db")
        buf.write("\4\u00dc\t\u00dc\4\u00dd\t\u00dd\4\u00de\t\u00de\4\u00df")
        buf.write("\t\u00df\4\u00e0\t\u00e0\4\u00e1\t\u00e1\4\u00e2\t\u00e2")
        buf.write("\4\u00e3\t\u00e3\4\u00e4\t\u00e4\4\u00e5\t\u00e5\4\u00e6")
        buf.write("\t\u00e6\4\u00e7\t\u00e7\4\u00e8\t\u00e8\4\u00e9\t\u00e9")
        buf.write("\4\u00ea\t\u00ea\4\u00eb\t\u00eb\4\u00ec\t\u00ec\4\u00ed")
        buf.write("\t\u00ed\4\u00ee\t\u00ee\4\u00ef\t\u00ef\4\u00f0\t\u00f0")
        buf.write("\4\u00f1\t\u00f1\4\u00f2\t\u00f2\4\u00f3\t\u00f3\4\u00f4")
        buf.write("\t\u00f4\4\u00f5\t\u00f5\4\u00f6\t\u00f6\4\u00f7\t\u00f7")
        buf.write("\4\u00f8\t\u00f8\4\u00f9\t\u00f9\4\u00fa\t\u00fa\4\u00fb")
        buf.write("\t\u00fb\4\u00fc\t\u00fc\4\u00fd\t\u00fd\4\u00fe\t\u00fe")
        buf.write("\4\u00ff\t\u00ff\3\2\3\2\3\3\3\3\3\3\3\4\3\4\5\4\u0206")
        buf.write("\n\4\3\4\3\4\5\4\u020a\n\4\3\4\3\4\3\5\3\5\5\5\u0210\n")
        buf.write("\5\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u021a\n\7\3\b\3")
        buf.write("\b\3\t\3\t\3\t\3\t\7\t\u0222\n\t\f\t\16\t\u0225\13\t\3")
        buf.write("\t\3\t\3\n\3\n\3\n\3\n\5\n\u022d\n\n\3\n\3\n\3\n\5\n\u0232")
        buf.write("\n\n\3\n\3\n\3\13\3\13\3\13\5\13\u0239\n\13\3\f\3\f\5")
        buf.write("\f\u023d\n\f\3\r\3\r\3\r\5\r\u0242\n\r\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u024e\n\16\3")
        buf.write("\16\5\16\u0251\n\16\3\16\3\16\3\17\7\17\u0256\n\17\f\17")
        buf.write("\16\17\u0259\13\17\3\20\3\20\3\20\5\20\u025e\n\20\3\20")
        buf.write("\3\20\5\20\u0262\n\20\3\20\3\20\5\20\u0266\n\20\3\20\5")
        buf.write("\20\u0269\n\20\3\20\3\20\3\20\3\20\3\20\5\20\u0270\n\20")
        buf.write("\3\21\7\21\u0273\n\21\f\21\16\21\u0276\13\21\3\22\3\22")
        buf.write("\5\22\u027a\n\22\3\23\3\23\5\23\u027e\n\23\3\24\3\24\3")
        buf.write("\24\3\24\5\24\u0284\n\24\3\24\3\24\5\24\u0288\n\24\3\25")
        buf.write("\5\25\u028b\n\25\3\25\3\25\3\25\3\26\3\26\3\26\5\26\u0293")
        buf.write("\n\26\3\26\3\26\3\27\3\27\3\27\7\27\u029a\n\27\f\27\16")
        buf.write("\27\u029d\13\27\3\30\3\30\3\30\3\30\3\30\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\5\31\u02ab\n\31\3\32\3\32\3\32\3")
        buf.write("\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\34\3\34\5\34")
        buf.write("\u02ba\n\34\3\34\5\34\u02bd\n\34\3\34\5\34\u02c0\n\34")
        buf.write("\3\35\3\35\3\35\7\35\u02c5\n\35\f\35\16\35\u02c8\13\35")
        buf.write("\3\35\7\35\u02cb\n\35\f\35\16\35\u02ce\13\35\3\35\3\35")
        buf.write("\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\5\36\u02ea\n\36\3\37\7\37\u02ed\n\37\f\37\16")
        buf.write("\37\u02f0\13\37\3 \3 \3 \3 \5 \u02f6\n \5 \u02f8\n \3")
        buf.write(" \3 \3 \3 \5 \u02fe\n \5 \u0300\n \3!\3!\3!\3!\3!\5!\u0307")
        buf.write("\n!\3!\5!\u030a\n!\3\"\3\"\3\"\3\"\3\"\3\"\5\"\u0312\n")
        buf.write("\"\3\"\5\"\u0315\n\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\5\"\u031e")
        buf.write("\n\"\3\"\3\"\3#\7#\u0323\n#\f#\16#\u0326\13#\3$\3$\5$")
        buf.write("\u032a\n$\3$\5$\u032d\n$\3$\3$\3$\3%\5%\u0333\n%\3%\3")
        buf.write("%\3%\3%\3&\3&\3&\7&\u033c\n&\f&\16&\u033f\13&\3\'\3\'")
        buf.write("\3\'\3\'\3(\5(\u0346\n(\3(\3(\5(\u034a\n(\3(\3(\5(\u034e")
        buf.write("\n(\3(\3(\3)\5)\u0353\n)\3)\3)\3)\3)\6)\u0359\n)\r)\16")
        buf.write(")\u035a\3)\3)\3)\5)\u0360\n)\3)\3)\3*\3*\3*\3*\3*\3+\3")
        buf.write("+\3+\3+\5+\u036d\n+\3,\3,\3,\7,\u0372\n,\f,\16,\u0375")
        buf.write("\13,\3-\3-\3-\3-\3-\5-\u037c\n-\3-\5-\u037f\n-\3-\3-\3")
        buf.write("-\3-\3.\3.\3.\5.\u0388\n.\3.\5.\u038b\n.\3.\5.\u038e\n")
        buf.write(".\3.\3.\3.\5.\u0393\n.\3.\3.\3/\3/\3/\5/\u039a\n/\3/\5")
        buf.write("/\u039d\n/\3/\3/\3\60\3\60\3\60\3\60\3\61\3\61\5\61\u03a7")
        buf.write("\n\61\3\62\3\62\5\62\u03ab\n\62\3\63\5\63\u03ae\n\63\3")
        buf.write("\63\5\63\u03b1\n\63\3\63\3\63\3\63\3\64\5\64\u03b7\n\64")
        buf.write("\3\64\3\64\5\64\u03bb\n\64\3\64\5\64\u03be\n\64\3\64\3")
        buf.write("\64\5\64\u03c2\n\64\3\64\3\64\3\65\5\65\u03c7\n\65\3\65")
        buf.write("\5\65\u03ca\n\65\3\65\3\65\3\65\3\66\5\66\u03d0\n\66\3")
        buf.write("\66\5\66\u03d3\n\66\3\66\3\66\5\66\u03d7\n\66\3\67\3\67")
        buf.write("\38\38\38\39\39\39\39\39\39\3:\3:\3:\3:\3:\5:\u03e9\n")
        buf.write(":\5:\u03eb\n:\3;\3;\3;\3;\3;\3;\3;\3;\3;\5;\u03f6\n;\3")
        buf.write(";\5;\u03f9\n;\3;\3;\3<\3<\3<\5<\u0400\n<\3=\7=\u0403\n")
        buf.write("=\f=\16=\u0406\13=\3>\3>\5>\u040a\n>\3?\3?\3?\3?\3?\3")
        buf.write("@\3@\3@\3@\3@\3@\5@\u0417\n@\3@\3@\3A\3A\3A\3A\3A\3B\3")
        buf.write("B\3B\3B\3B\3C\3C\5C\u0427\nC\3D\7D\u042a\nD\fD\16D\u042d")
        buf.write("\13D\3E\3E\5E\u0431\nE\3F\3F\3F\5F\u0436\nF\3F\5F\u0439")
        buf.write("\nF\3G\7G\u043c\nG\fG\16G\u043f\13G\3G\3G\3H\3H\3H\3I")
        buf.write("\3I\5I\u0448\nI\3J\3J\3K\3K\3K\3K\3K\3K\3L\3L\5L\u0454")
        buf.write("\nL\3M\3M\3M\5M\u0459\nM\3M\3M\3N\3N\3N\3N\3N\3O\3O\3")
        buf.write("P\3P\3Q\3Q\3Q\3Q\3Q\3Q\5Q\u046c\nQ\3Q\3Q\3Q\5Q\u0471\n")
        buf.write("Q\3R\3R\3S\3S\5S\u0477\nS\3T\3T\3T\7T\u047c\nT\fT\16T")
        buf.write("\u047f\13T\3U\3U\3U\3U\3U\3U\3U\5U\u0488\nU\3U\3U\5U\u048c")
        buf.write("\nU\3U\5U\u048f\nU\3U\3U\3V\3V\3V\3V\3V\3V\3V\3V\3V\3")
        buf.write("V\3V\3V\3V\3V\3V\3V\3V\3V\3V\3V\5V\u04a7\nV\3W\7W\u04aa")
        buf.write("\nW\fW\16W\u04ad\13W\3X\3X\5X\u04b1\nX\3Y\5Y\u04b4\nY")
        buf.write("\3Y\5Y\u04b7\nY\3Z\3Z\3Z\7Z\u04bc\nZ\fZ\16Z\u04bf\13Z")
        buf.write("\3Z\3Z\5Z\u04c3\nZ\3[\3[\3[\3[\3\\\3\\\3\\\5\\\u04cc\n")
        buf.write("\\\3]\7]\u04cf\n]\f]\16]\u04d2\13]\3^\3^\3^\5^\u04d7\n")
        buf.write("^\3_\3_\5_\u04db\n_\3`\3`\3`\3`\7`\u04e1\n`\f`\16`\u04e4")
        buf.write("\13`\3`\3`\3a\5a\u04e9\na\3a\3a\5a\u04ed\na\3a\3a\5a\u04f1")
        buf.write("\na\3a\3a\3b\3b\3b\3b\7b\u04f9\nb\fb\16b\u04fc\13b\3c")
        buf.write("\3c\3c\5c\u0501\nc\3c\3c\3c\3c\5c\u0507\nc\3d\3d\3d\3")
        buf.write("d\3d\5d\u050e\nd\3d\3d\3e\3e\3f\3f\5f\u0516\nf\3f\3f\3")
        buf.write("f\3g\3g\3g\3g\3h\3h\3i\3i\3i\3i\3i\3i\5i\u0527\ni\3j\3")
        buf.write("j\3j\3j\3j\3j\5j\u052f\nj\3j\3j\3k\3k\3k\3k\7k\u0537\n")
        buf.write("k\fk\16k\u053a\13k\3k\5k\u053d\nk\3k\7k\u0540\nk\fk\16")
        buf.write("k\u0543\13k\3k\3k\3k\5k\u0548\nk\3k\3k\3l\3l\3l\3l\5l")
        buf.write("\u0550\nl\3m\3m\3m\3m\3m\3m\3n\3n\3n\7n\u055b\nn\fn\16")
        buf.write("n\u055e\13n\3o\3o\3o\3o\3o\3o\3p\3p\5p\u0568\np\3q\3q")
        buf.write("\3q\7q\u056d\nq\fq\16q\u0570\13q\3r\3r\3r\3r\3r\3r\3r")
        buf.write("\3r\3s\3s\3s\3s\3s\3s\3s\3s\3t\3t\3t\3t\3u\3u\3v\3v\3")
        buf.write("v\7v\u058b\nv\fv\16v\u058e\13v\3w\5w\u0591\nw\3w\3w\3")
        buf.write("w\3w\3w\3w\3w\3w\3w\7w\u059c\nw\fw\16w\u059f\13w\3w\3")
        buf.write("w\5w\u05a3\nw\3w\3w\3w\5w\u05a8\nw\3w\3w\3x\3x\3x\3x\7")
        buf.write("x\u05b0\nx\fx\16x\u05b3\13x\3x\3x\3y\3y\5y\u05b9\ny\3")
        buf.write("z\3z\3z\3z\3{\5{\u05c0\n{\3{\3{\3{\3{\3{\3{\3{\5{\u05c9")
        buf.write("\n{\3{\3{\5{\u05cd\n{\3|\3|\3|\7|\u05d2\n|\f|\16|\u05d5")
        buf.write("\13|\3|\3|\5|\u05d9\n|\3}\5}\u05dc\n}\3}\3}\3}\5}\u05e1")
        buf.write("\n}\3}\3}\3}\5}\u05e6\n}\3~\3~\3~\3~\3~\3~\5~\u05ee\n")
        buf.write("~\3\177\3\177\3\u0080\3\u0080\3\u0080\3\u0080\3\u0080")
        buf.write("\3\u0081\3\u0081\3\u0081\7\u0081\u05fa\n\u0081\f\u0081")
        buf.write("\16\u0081\u05fd\13\u0081\3\u0082\3\u0082\3\u0082\7\u0082")
        buf.write("\u0602\n\u0082\f\u0082\16\u0082\u0605\13\u0082\3\u0083")
        buf.write("\3\u0083\3\u0083\7\u0083\u060a\n\u0083\f\u0083\16\u0083")
        buf.write("\u060d\13\u0083\3\u0084\3\u0084\3\u0084\3\u0084\5\u0084")
        buf.write("\u0613\n\u0084\3\u0084\3\u0084\3\u0084\5\u0084\u0618\n")
        buf.write("\u0084\3\u0085\3\u0085\3\u0085\3\u0085\3\u0085\5\u0085")
        buf.write("\u061f\n\u0085\3\u0085\3\u0085\5\u0085\u0623\n\u0085\3")
        buf.write("\u0086\3\u0086\3\u0086\3\u0086\3\u0086\5\u0086\u062a\n")
        buf.write("\u0086\3\u0086\3\u0086\5\u0086\u062e\n\u0086\3\u0087\3")
        buf.write("\u0087\3\u0087\3\u0087\3\u0087\3\u0088\5\u0088\u0636\n")
        buf.write("\u0088\3\u0088\3\u0088\3\u0088\5\u0088\u063b\n\u0088\3")
        buf.write("\u0088\3\u0088\3\u0088\5\u0088\u0640\n\u0088\3\u0089\3")
        buf.write("\u0089\3\u0089\3\u0089\5\u0089\u0646\n\u0089\3\u008a\3")
        buf.write("\u008a\3\u008a\3\u008b\3\u008b\3\u008b\3\u008b\3\u008c")
        buf.write("\3\u008c\5\u008c\u0651\n\u008c\3\u008d\3\u008d\3\u008d")
        buf.write("\3\u008d\3\u008d\5\u008d\u0658\n\u008d\3\u008e\3\u008e")
        buf.write("\3\u008f\3\u008f\3\u008f\7\u008f\u065f\n\u008f\f\u008f")
        buf.write("\16\u008f\u0662\13\u008f\3\u0090\3\u0090\3\u0091\5\u0091")
        buf.write("\u0667\n\u0091\3\u0091\5\u0091\u066a\n\u0091\3\u0091\3")
        buf.write("\u0091\3\u0091\3\u0091\3\u0091\5\u0091\u0671\n\u0091\3")
        buf.write("\u0091\3\u0091\3\u0092\3\u0092\3\u0093\3\u0093\3\u0094")
        buf.write("\3\u0094\3\u0094\3\u0094\7\u0094\u067d\n\u0094\f\u0094")
        buf.write("\16\u0094\u0680\13\u0094\5\u0094\u0682\n\u0094\3\u0095")
        buf.write("\3\u0095\3\u0095\3\u0095\5\u0095\u0688\n\u0095\3\u0096")
        buf.write("\3\u0096\3\u0096\3\u0096\3\u0096\7\u0096\u068f\n\u0096")
        buf.write("\f\u0096\16\u0096\u0692\13\u0096\5\u0096\u0694\n\u0096")
        buf.write("\3\u0097\3\u0097\5\u0097\u0698\n\u0097\3\u0097\3\u0097")
        buf.write("\3\u0098\3\u0098\3\u0098\3\u0098\7\u0098\u06a0\n\u0098")
        buf.write("\f\u0098\16\u0098\u06a3\13\u0098\3\u0098\3\u0098\3\u0099")
        buf.write("\3\u0099\3\u0099\7\u0099\u06aa\n\u0099\f\u0099\16\u0099")
        buf.write("\u06ad\13\u0099\3\u009a\3\u009a\3\u009a\3\u009a\3\u009a")
        buf.write("\3\u009a\3\u009b\3\u009b\5\u009b\u06b7\n\u009b\3\u009c")
        buf.write("\3\u009c\3\u009c\3\u009c\3\u009d\5\u009d\u06be\n\u009d")
        buf.write("\3\u009d\3\u009d\5\u009d\u06c2\n\u009d\3\u009d\3\u009d")
        buf.write("\5\u009d\u06c6\n\u009d\3\u009d\3\u009d\3\u009e\3\u009e")
        buf.write("\5\u009e\u06cc\n\u009e\3\u009f\3\u009f\3\u009f\3\u009f")
        buf.write("\3\u009f\3\u009f\5\u009f\u06d4\n\u009f\3\u00a0\5\u00a0")
        buf.write("\u06d7\n\u00a0\3\u00a0\5\u00a0\u06da\n\u00a0\3\u00a1\3")
        buf.write("\u00a1\3\u00a1\3\u00a1\3\u00a1\3\u00a1\3\u00a1\3\u00a1")
        buf.write("\5\u00a1\u06e4\n\u00a1\3\u00a1\5\u00a1\u06e7\n\u00a1\3")
        buf.write("\u00a1\3\u00a1\3\u00a2\3\u00a2\3\u00a2\3\u00a2\3\u00a2")
        buf.write("\3\u00a2\3\u00a2\3\u00a2\3\u00a2\3\u00a2\3\u00a2\5\u00a2")
        buf.write("\u06f6\n\u00a2\3\u00a3\7\u00a3\u06f9\n\u00a3\f\u00a3\16")
        buf.write("\u00a3\u06fc\13\u00a3\3\u00a4\3\u00a4\3\u00a4\3\u00a4")
        buf.write("\3\u00a4\3\u00a4\5\u00a4\u0704\n\u00a4\3\u00a4\5\u00a4")
        buf.write("\u0707\n\u00a4\3\u00a4\3\u00a4\3\u00a5\3\u00a5\3\u00a5")
        buf.write("\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5")
        buf.write("\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5\3\u00a5")
        buf.write("\3\u00a5\5\u00a5\u071d\n\u00a5\3\u00a6\7\u00a6\u0720\n")
        buf.write("\u00a6\f\u00a6\16\u00a6\u0723\13\u00a6\3\u00a7\3\u00a7")
        buf.write("\3\u00a7\3\u00a7\3\u00a8\3\u00a8\3\u00a8\3\u00a9\3\u00a9")
        buf.write("\3\u00a9\3\u00a9\7\u00a9\u0730\n\u00a9\f\u00a9\16\u00a9")
        buf.write("\u0733\13\u00a9\3\u00a9\3\u00a9\3\u00a9\5\u00a9\u0738")
        buf.write("\n\u00a9\3\u00aa\3\u00aa\3\u00aa\3\u00aa\3\u00aa\3\u00aa")
        buf.write("\3\u00ab\3\u00ab\3\u00ac\3\u00ac\3\u00ac\3\u00ac\3\u00ac")
        buf.write("\3\u00ac\3\u00ad\3\u00ad\3\u00ad\3\u00ad\3\u00ad\3\u00ad")
        buf.write("\3\u00ad\3\u00ad\3\u00ad\5\u00ad\u0751\n\u00ad\3\u00ae")
        buf.write("\3\u00ae\3\u00ae\5\u00ae\u0756\n\u00ae\3\u00af\3\u00af")
        buf.write("\3\u00af\3\u00af\3\u00af\3\u00af\3\u00af\3\u00af\3\u00af")
        buf.write("\3\u00af\3\u00af\3\u00af\5\u00af\u0764\n\u00af\3\u00b0")
        buf.write("\7\u00b0\u0767\n\u00b0\f\u00b0\16\u00b0\u076a\13\u00b0")
        buf.write("\3\u00b1\7\u00b1\u076d\n\u00b1\f\u00b1\16\u00b1\u0770")
        buf.write("\13\u00b1\3\u00b2\3\u00b2\3\u00b2\3\u00b2\3\u00b2\5\u00b2")
        buf.write("\u0777\n\u00b2\3\u00b3\5\u00b3\u077a\n\u00b3\3\u00b3\3")
        buf.write("\u00b3\3\u00b3\3\u00b4\3\u00b4\3\u00b4\3\u00b4\3\u00b4")
        buf.write("\3\u00b4\3\u00b4\3\u00b4\3\u00b4\3\u00b4\3\u00b4\3\u00b4")
        buf.write("\3\u00b4\5\u00b4\u078c\n\u00b4\3\u00b5\7\u00b5\u078f\n")
        buf.write("\u00b5\f\u00b5\16\u00b5\u0792\13\u00b5\3\u00b6\5\u00b6")
        buf.write("\u0795\n\u00b6\3\u00b6\5\u00b6\u0798\n\u00b6\3\u00b6\3")
        buf.write("\u00b6\3\u00b6\3\u00b6\3\u00b6\5\u00b6\u079f\n\u00b6\3")
        buf.write("\u00b6\5\u00b6\u07a2\n\u00b6\3\u00b6\3\u00b6\3\u00b6\3")
        buf.write("\u00b6\3\u00b6\5\u00b6\u07a9\n\u00b6\3\u00b6\3\u00b6\5")
        buf.write("\u00b6\u07ad\n\u00b6\3\u00b6\3\u00b6\3\u00b7\7\u00b7\u07b2")
        buf.write("\n\u00b7\f\u00b7\16\u00b7\u07b5\13\u00b7\3\u00b8\3\u00b8")
        buf.write("\3\u00b8\3\u00b8\3\u00b8\3\u00b8\3\u00b8\5\u00b8\u07be")
        buf.write("\n\u00b8\3\u00b9\3\u00b9\3\u00b9\5\u00b9\u07c3\n\u00b9")
        buf.write("\3\u00ba\3\u00ba\3\u00ba\7\u00ba\u07c8\n\u00ba\f\u00ba")
        buf.write("\16\u00ba\u07cb\13\u00ba\3\u00ba\3\u00ba\5\u00ba\u07cf")
        buf.write("\n\u00ba\3\u00bb\3\u00bb\3\u00bb\3\u00bb\3\u00bc\3\u00bc")
        buf.write("\5\u00bc\u07d7\n\u00bc\3\u00bd\3\u00bd\3\u00bd\3\u00bd")
        buf.write("\3\u00be\3\u00be\3\u00be\3\u00bf\3\u00bf\6\u00bf\u07e2")
        buf.write("\n\u00bf\r\u00bf\16\u00bf\u07e3\3\u00bf\3\u00bf\3\u00bf")
        buf.write("\5\u00bf\u07e9\n\u00bf\3\u00c0\3\u00c0\6\u00c0\u07ed\n")
        buf.write("\u00c0\r\u00c0\16\u00c0\u07ee\3\u00c0\3\u00c0\3\u00c0")
        buf.write("\5\u00c0\u07f4\n\u00c0\3\u00c1\3\u00c1\3\u00c1\3\u00c1")
        buf.write("\5\u00c1\u07fa\n\u00c1\3\u00c2\3\u00c2\3\u00c3\5\u00c3")
        buf.write("\u07ff\n\u00c3\3\u00c3\3\u00c3\3\u00c3\3\u00c3\5\u00c3")
        buf.write("\u0805\n\u00c3\3\u00c3\3\u00c3\3\u00c4\5\u00c4\u080a\n")
        buf.write("\u00c4\3\u00c4\3\u00c4\5\u00c4\u080e\n\u00c4\3\u00c4\3")
        buf.write("\u00c4\3\u00c5\3\u00c5\3\u00c5\3\u00c5\3\u00c5\3\u00c5")
        buf.write("\3\u00c5\3\u00c6\3\u00c6\3\u00c6\5\u00c6\u081c\n\u00c6")
        buf.write("\3\u00c7\3\u00c7\5\u00c7\u0820\n\u00c7\3\u00c8\3\u00c8")
        buf.write("\3\u00c8\3\u00c8\3\u00c8\3\u00c9\3\u00c9\3\u00c9\3\u00c9")
        buf.write("\3\u00c9\3\u00c9\3\u00c9\3\u00c9\3\u00c9\3\u00ca\3\u00ca")
        buf.write("\3\u00ca\3\u00ca\3\u00ca\3\u00ca\3\u00ca\3\u00ca\7\u00ca")
        buf.write("\u0838\n\u00ca\f\u00ca\16\u00ca\u083b\13\u00ca\3\u00cb")
        buf.write("\3\u00cb\3\u00cb\3\u00cc\3\u00cc\3\u00cc\7\u00cc\u0843")
        buf.write("\n\u00cc\f\u00cc\16\u00cc\u0846\13\u00cc\3\u00cd\7\u00cd")
        buf.write("\u0849\n\u00cd\f\u00cd\16\u00cd\u084c\13\u00cd\3\u00ce")
        buf.write("\3\u00ce\3\u00ce\3\u00ce\3\u00ce\3\u00ce\3\u00ce\3\u00ce")
        buf.write("\3\u00ce\3\u00ce\3\u00ce\3\u00ce\5\u00ce\u085a\n\u00ce")
        buf.write("\3\u00ce\3\u00ce\3\u00ce\3\u00ce\5\u00ce\u0860\n\u00ce")
        buf.write("\3\u00cf\3\u00cf\3\u00cf\3\u00cf\5\u00cf\u0866\n\u00cf")
        buf.write("\3\u00d0\3\u00d0\3\u00d1\5\u00d1\u086b\n\u00d1\3\u00d1")
        buf.write("\3\u00d1\3\u00d1\5\u00d1\u0870\n\u00d1\3\u00d1\3\u00d1")
        buf.write("\3\u00d1\3\u00d2\3\u00d2\3\u00d2\3\u00d2\3\u00d2\5\u00d2")
        buf.write("\u087a\n\u00d2\3\u00d2\3\u00d2\5\u00d2\u087e\n\u00d2\3")
        buf.write("\u00d2\3\u00d2\3\u00d3\3\u00d3\3\u00d4\3\u00d4\3\u00d4")
        buf.write("\7\u00d4\u0887\n\u00d4\f\u00d4\16\u00d4\u088a\13\u00d4")
        buf.write("\3\u00d4\3\u00d4\5\u00d4\u088e\n\u00d4\3\u00d5\3\u00d5")
        buf.write("\3\u00d5\3\u00d5\7\u00d5\u0894\n\u00d5\f\u00d5\16\u00d5")
        buf.write("\u0897\13\u00d5\5\u00d5\u0899\n\u00d5\3\u00d5\3\u00d5")
        buf.write("\5\u00d5\u089d\n\u00d5\3\u00d5\3\u00d5\3\u00d6\5\u00d6")
        buf.write("\u08a2\n\u00d6\3\u00d6\3\u00d6\3\u00d6\3\u00d6\7\u00d6")
        buf.write("\u08a8\n\u00d6\f\u00d6\16\u00d6\u08ab\13\u00d6\3\u00d7")
        buf.write("\5\u00d7\u08ae\n\u00d7\3\u00d7\3\u00d7\3\u00d7\3\u00d7")
        buf.write("\5\u00d7\u08b4\n\u00d7\3\u00d7\3\u00d7\3\u00d8\3\u00d8")
        buf.write("\3\u00d8\3\u00d8\3\u00d8\3\u00d9\5\u00d9\u08be\n\u00d9")
        buf.write("\3\u00d9\3\u00d9\3\u00d9\3\u00d9\6\u00d9\u08c4\n\u00d9")
        buf.write("\r\u00d9\16\u00d9\u08c5\3\u00d9\3\u00d9\3\u00d9\5\u00d9")
        buf.write("\u08cb\n\u00d9\3\u00d9\3\u00d9\3\u00da\5\u00da\u08d0\n")
        buf.write("\u00da\3\u00da\3\u00da\3\u00da\3\u00da\3\u00da\3\u00da")
        buf.write("\3\u00da\3\u00da\3\u00da\7\u00da\u08db\n\u00da\f\u00da")
        buf.write("\16\u00da\u08de\13\u00da\3\u00da\3\u00da\5\u00da\u08e2")
        buf.write("\n\u00da\3\u00da\3\u00da\3\u00da\5\u00da\u08e7\n\u00da")
        buf.write("\3\u00da\3\u00da\3\u00db\5\u00db\u08ec\n\u00db\3\u00db")
        buf.write("\3\u00db\5\u00db\u08f0\n\u00db\3\u00db\3\u00db\3\u00db")
        buf.write("\3\u00db\3\u00db\3\u00db\5\u00db\u08f8\n\u00db\3\u00db")
        buf.write("\3\u00db\3\u00dc\3\u00dc\3\u00dc\3\u00dc\3\u00dc\5\u00dc")
        buf.write("\u0901\n\u00dc\3\u00dc\3\u00dc\5\u00dc\u0905\n\u00dc\3")
        buf.write("\u00dd\7\u00dd\u0908\n\u00dd\f\u00dd\16\u00dd\u090b\13")
        buf.write("\u00dd\3\u00de\3\u00de\3\u00de\3\u00de\3\u00de\3\u00de")
        buf.write("\3\u00de\5\u00de\u0914\n\u00de\3\u00df\3\u00df\3\u00df")
        buf.write("\3\u00df\3\u00df\3\u00df\3\u00df\3\u00e0\3\u00e0\3\u00e0")
        buf.write("\3\u00e0\3\u00e0\3\u00e0\3\u00e1\3\u00e1\3\u00e1\3\u00e1")
        buf.write("\3\u00e1\3\u00e1\3\u00e2\3\u00e2\5\u00e2\u092b\n\u00e2")
        buf.write("\3\u00e2\3\u00e2\3\u00e2\3\u00e2\3\u00e2\3\u00e2\5\u00e2")
        buf.write("\u0933\n\u00e2\3\u00e3\3\u00e3\3\u00e3\3\u00e3\3\u00e3")
        buf.write("\3\u00e3\3\u00e3\5\u00e3\u093c\n\u00e3\3\u00e3\5\u00e3")
        buf.write("\u093f\n\u00e3\3\u00e3\3\u00e3\3\u00e4\3\u00e4\3\u00e4")
        buf.write("\3\u00e5\3\u00e5\3\u00e5\3\u00e5\3\u00e5\3\u00e5\3\u00e5")
        buf.write("\3\u00e5\3\u00e5\3\u00e5\3\u00e5\3\u00e5\3\u00e5\5\u00e5")
        buf.write("\u0953\n\u00e5\3\u00e6\7\u00e6\u0956\n\u00e6\f\u00e6\16")
        buf.write("\u00e6\u0959\13\u00e6\3\u00e7\3\u00e7\3\u00e8\3\u00e8")
        buf.write("\5\u00e8\u095f\n\u00e8\3\u00e9\3\u00e9\3\u00e9\3\u00e9")
        buf.write("\3\u00e9\3\u00e9\5\u00e9\u0967\n\u00e9\3\u00ea\5\u00ea")
        buf.write("\u096a\n\u00ea\3\u00ea\3\u00ea\3\u00ea\3\u00ea\3\u00ea")
        buf.write("\3\u00ea\5\u00ea\u0972\n\u00ea\3\u00ea\3\u00ea\3\u00ea")
        buf.write("\3\u00eb\7\u00eb\u0978\n\u00eb\f\u00eb\16\u00eb\u097b")
        buf.write("\13\u00eb\3\u00ec\3\u00ec\3\u00ec\3\u00ec\3\u00ec\3\u00ec")
        buf.write("\3\u00ed\3\u00ed\5\u00ed\u0985\n\u00ed\3\u00ed\5\u00ed")
        buf.write("\u0988\n\u00ed\3\u00ed\5\u00ed\u098b\n\u00ed\3\u00ee\3")
        buf.write("\u00ee\3\u00ee\3\u00ee\5\u00ee\u0991\n\u00ee\3\u00ef\3")
        buf.write("\u00ef\5\u00ef\u0995\n\u00ef\3\u00f0\3\u00f0\3\u00f0\3")
        buf.write("\u00f0\7\u00f0\u099b\n\u00f0\f\u00f0\16\u00f0\u099e\13")
        buf.write("\u00f0\3\u00f1\3\u00f1\3\u00f1\5\u00f1\u09a3\n\u00f1\3")
        buf.write("\u00f2\3\u00f2\3\u00f2\3\u00f2\3\u00f2\3\u00f2\3\u00f3")
        buf.write("\3\u00f3\5\u00f3\u09ad\n\u00f3\3\u00f3\3\u00f3\5\u00f3")
        buf.write("\u09b1\n\u00f3\3\u00f3\3\u00f3\3\u00f4\3\u00f4\3\u00f4")
        buf.write("\3\u00f5\3\u00f5\3\u00f5\3\u00f6\3\u00f6\3\u00f6\3\u00f6")
        buf.write("\5\u00f6\u09bf\n\u00f6\3\u00f6\3\u00f6\3\u00f7\3\u00f7")
        buf.write("\3\u00f7\3\u00f7\5\u00f7\u09c7\n\u00f7\3\u00f8\3\u00f8")
        buf.write("\3\u00f8\3\u00f8\3\u00f8\7\u00f8\u09ce\n\u00f8\f\u00f8")
        buf.write("\16\u00f8\u09d1\13\u00f8\3\u00f8\3\u00f8\3\u00f8\3\u00f8")
        buf.write("\3\u00f9\3\u00f9\3\u00f9\3\u00f9\3\u00f9\7\u00f9\u09dc")
        buf.write("\n\u00f9\f\u00f9\16\u00f9\u09df\13\u00f9\3\u00f9\3\u00f9")
        buf.write("\3\u00f9\3\u00f9\3\u00fa\3\u00fa\3\u00fa\3\u00fa\7\u00fa")
        buf.write("\u09e9\n\u00fa\f\u00fa\16\u00fa\u09ec\13\u00fa\3\u00fa")
        buf.write("\3\u00fa\3\u00fb\5\u00fb\u09f1\n\u00fb\3\u00fb\3\u00fb")
        buf.write("\3\u00fb\3\u00fb\3\u00fb\3\u00fc\5\u00fc\u09f9\n\u00fc")
        buf.write("\3\u00fc\3\u00fc\3\u00fc\3\u00fc\3\u00fc\3\u00fc\5\u00fc")
        buf.write("\u0a01\n\u00fc\3\u00fc\3\u00fc\3\u00fd\5\u00fd\u0a06\n")
        buf.write("\u00fd\3\u00fd\3\u00fd\5\u00fd\u0a0a\n\u00fd\3\u00fd\5")
        buf.write("\u00fd\u0a0d\n\u00fd\3\u00fd\5\u00fd\u0a10\n\u00fd\3\u00fd")
        buf.write("\3\u00fd\3\u00fe\3\u00fe\3\u00fe\7\u00fe\u0a17\n\u00fe")
        buf.write("\f\u00fe\16\u00fe\u0a1a\13\u00fe\3\u00fe\5\u00fe\u0a1d")
        buf.write("\n\u00fe\3\u00ff\3\u00ff\3\u00ff\5\u00ff\u0a22\n\u00ff")
        buf.write("\3\u00ff\2\2\u0100\2\4\6\b\n\f\16\20\22\24\26\30\32\34")
        buf.write("\36 \"$&(*,.\60\62\64\668:<>@BDFHJLNPRTVXZ\\^`bdfhjln")
        buf.write("prtvxz|~\u0080\u0082\u0084\u0086\u0088\u008a\u008c\u008e")
        buf.write("\u0090\u0092\u0094\u0096\u0098\u009a\u009c\u009e\u00a0")
        buf.write("\u00a2\u00a4\u00a6\u00a8\u00aa\u00ac\u00ae\u00b0\u00b2")
        buf.write("\u00b4\u00b6\u00b8\u00ba\u00bc\u00be\u00c0\u00c2\u00c4")
        buf.write("\u00c6\u00c8\u00ca\u00cc\u00ce\u00d0\u00d2\u00d4\u00d6")
        buf.write("\u00d8\u00da\u00dc\u00de\u00e0\u00e2\u00e4\u00e6\u00e8")
        buf.write("\u00ea\u00ec\u00ee\u00f0\u00f2\u00f4\u00f6\u00f8\u00fa")
        buf.write("\u00fc\u00fe\u0100\u0102\u0104\u0106\u0108\u010a\u010c")
        buf.write("\u010e\u0110\u0112\u0114\u0116\u0118\u011a\u011c\u011e")
        buf.write("\u0120\u0122\u0124\u0126\u0128\u012a\u012c\u012e\u0130")
        buf.write("\u0132\u0134\u0136\u0138\u013a\u013c\u013e\u0140\u0142")
        buf.write("\u0144\u0146\u0148\u014a\u014c\u014e\u0150\u0152\u0154")
        buf.write("\u0156\u0158\u015a\u015c\u015e\u0160\u0162\u0164\u0166")
        buf.write("\u0168\u016a\u016c\u016e\u0170\u0172\u0174\u0176\u0178")
        buf.write("\u017a\u017c\u017e\u0180\u0182\u0184\u0186\u0188\u018a")
        buf.write("\u018c\u018e\u0190\u0192\u0194\u0196\u0198\u019a\u019c")
        buf.write("\u019e\u01a0\u01a2\u01a4\u01a6\u01a8\u01aa\u01ac\u01ae")
        buf.write("\u01b0\u01b2\u01b4\u01b6\u01b8\u01ba\u01bc\u01be\u01c0")
        buf.write("\u01c2\u01c4\u01c6\u01c8\u01ca\u01cc\u01ce\u01d0\u01d2")
        buf.write("\u01d4\u01d6\u01d8\u01da\u01dc\u01de\u01e0\u01e2\u01e4")
        buf.write("\u01e6\u01e8\u01ea\u01ec\u01ee\u01f0\u01f2\u01f4\u01f6")
        buf.write("\u01f8\u01fa\u01fc\2\21\5\2rrww\u00a0\u00a0\4\2\u008e")
        buf.write("\u008e\u0096\u0097\4\2\31\31cc\23\2\n\n\25\27\33\33\37")
        buf.write("\37!!$$,,\60\60\65\65BBFFIIXX^`ffhhkk\3\2xy\4\2((AA\7")
        buf.write("\2\t\t\64\6499??pq\7\2\22\22((**//AA\5\2\63\63MM\u0094")
        buf.write("\u0095\5\2\u0085\u0086\u0088\u0088\u0098\u009a\5\2STY")
        buf.write("Z\\]\4\2\23\23PP\3\2\u0096\u0097\4\2!!FF\4\2\'\'HH\u0ae8")
        buf.write("\2\u01fe\3\2\2\2\4\u0200\3\2\2\2\6\u0203\3\2\2\2\b\u020f")
        buf.write("\3\2\2\2\n\u0211\3\2\2\2\f\u0219\3\2\2\2\16\u021b\3\2")
        buf.write("\2\2\20\u021d\3\2\2\2\22\u0228\3\2\2\2\24\u0238\3\2\2")
        buf.write("\2\26\u023c\3\2\2\2\30\u023e\3\2\2\2\32\u0243\3\2\2\2")
        buf.write("\34\u0257\3\2\2\2\36\u026f\3\2\2\2 \u0274\3\2\2\2\"\u0279")
        buf.write("\3\2\2\2$\u027d\3\2\2\2&\u027f\3\2\2\2(\u028a\3\2\2\2")
        buf.write("*\u0292\3\2\2\2,\u0296\3\2\2\2.\u029e\3\2\2\2\60\u02aa")
        buf.write("\3\2\2\2\62\u02ac\3\2\2\2\64\u02b4\3\2\2\2\66\u02b9\3")
        buf.write("\2\2\28\u02c1\3\2\2\2:\u02e9\3\2\2\2<\u02ee\3\2\2\2>\u02f7")
        buf.write("\3\2\2\2@\u0309\3\2\2\2B\u030b\3\2\2\2D\u0324\3\2\2\2")
        buf.write("F\u0327\3\2\2\2H\u0332\3\2\2\2J\u0338\3\2\2\2L\u0340\3")
        buf.write("\2\2\2N\u0345\3\2\2\2P\u0352\3\2\2\2R\u0363\3\2\2\2T\u036c")
        buf.write("\3\2\2\2V\u036e\3\2\2\2X\u0376\3\2\2\2Z\u0384\3\2\2\2")
        buf.write("\\\u0396\3\2\2\2^\u03a0\3\2\2\2`\u03a6\3\2\2\2b\u03aa")
        buf.write("\3\2\2\2d\u03ad\3\2\2\2f\u03b6\3\2\2\2h\u03c6\3\2\2\2")
        buf.write("j\u03cf\3\2\2\2l\u03d8\3\2\2\2n\u03da\3\2\2\2p\u03dd\3")
        buf.write("\2\2\2r\u03e3\3\2\2\2t\u03ec\3\2\2\2v\u03ff\3\2\2\2x\u0404")
        buf.write("\3\2\2\2z\u0409\3\2\2\2|\u040b\3\2\2\2~\u0410\3\2\2\2")
        buf.write("\u0080\u041a\3\2\2\2\u0082\u041f\3\2\2\2\u0084\u0426\3")
        buf.write("\2\2\2\u0086\u042b\3\2\2\2\u0088\u0430\3\2\2\2\u008a\u0438")
        buf.write("\3\2\2\2\u008c\u043d\3\2\2\2\u008e\u0442\3\2\2\2\u0090")
        buf.write("\u0447\3\2\2\2\u0092\u0449\3\2\2\2\u0094\u044b\3\2\2\2")
        buf.write("\u0096\u0453\3\2\2\2\u0098\u0458\3\2\2\2\u009a\u045c\3")
        buf.write("\2\2\2\u009c\u0461\3\2\2\2\u009e\u0463\3\2\2\2\u00a0\u0470")
        buf.write("\3\2\2\2\u00a2\u0472\3\2\2\2\u00a4\u0474\3\2\2\2\u00a6")
        buf.write("\u0478\3\2\2\2\u00a8\u0480\3\2\2\2\u00aa\u04a6\3\2\2\2")
        buf.write("\u00ac\u04ab\3\2\2\2\u00ae\u04ae\3\2\2\2\u00b0\u04b3\3")
        buf.write("\2\2\2\u00b2\u04c2\3\2\2\2\u00b4\u04c4\3\2\2\2\u00b6\u04cb")
        buf.write("\3\2\2\2\u00b8\u04d0\3\2\2\2\u00ba\u04d6\3\2\2\2\u00bc")
        buf.write("\u04da\3\2\2\2\u00be\u04dc\3\2\2\2\u00c0\u04e8\3\2\2\2")
        buf.write("\u00c2\u04f4\3\2\2\2\u00c4\u0506\3\2\2\2\u00c6\u0508\3")
        buf.write("\2\2\2\u00c8\u0511\3\2\2\2\u00ca\u0515\3\2\2\2\u00cc\u051a")
        buf.write("\3\2\2\2\u00ce\u051e\3\2\2\2\u00d0\u0526\3\2\2\2\u00d2")
        buf.write("\u0528\3\2\2\2\u00d4\u0532\3\2\2\2\u00d6\u054f\3\2\2\2")
        buf.write("\u00d8\u0551\3\2\2\2\u00da\u0557\3\2\2\2\u00dc\u055f\3")
        buf.write("\2\2\2\u00de\u0567\3\2\2\2\u00e0\u0569\3\2\2\2\u00e2\u0571")
        buf.write("\3\2\2\2\u00e4\u0579\3\2\2\2\u00e6\u0581\3\2\2\2\u00e8")
        buf.write("\u0585\3\2\2\2\u00ea\u0587\3\2\2\2\u00ec\u0590\3\2\2\2")
        buf.write("\u00ee\u05ab\3\2\2\2\u00f0\u05b8\3\2\2\2\u00f2\u05ba\3")
        buf.write("\2\2\2\u00f4\u05cc\3\2\2\2\u00f6\u05d8\3\2\2\2\u00f8\u05db")
        buf.write("\3\2\2\2\u00fa\u05ed\3\2\2\2\u00fc\u05ef\3\2\2\2\u00fe")
        buf.write("\u05f1\3\2\2\2\u0100\u05f6\3\2\2\2\u0102\u05fe\3\2\2\2")
        buf.write("\u0104\u0606\3\2\2\2\u0106\u060e\3\2\2\2\u0108\u0619\3")
        buf.write("\2\2\2\u010a\u0624\3\2\2\2\u010c\u062f\3\2\2\2\u010e\u0635")
        buf.write("\3\2\2\2\u0110\u0645\3\2\2\2\u0112\u0647\3\2\2\2\u0114")
        buf.write("\u064a\3\2\2\2\u0116\u0650\3\2\2\2\u0118\u0657\3\2\2\2")
        buf.write("\u011a\u0659\3\2\2\2\u011c\u065b\3\2\2\2\u011e\u0663\3")
        buf.write("\2\2\2\u0120\u0666\3\2\2\2\u0122\u0674\3\2\2\2\u0124\u0676")
        buf.write("\3\2\2\2\u0126\u0681\3\2\2\2\u0128\u0683\3\2\2\2\u012a")
        buf.write("\u0689\3\2\2\2\u012c\u0695\3\2\2\2\u012e\u069b\3\2\2\2")
        buf.write("\u0130\u06a6\3\2\2\2\u0132\u06ae\3\2\2\2\u0134\u06b6\3")
        buf.write("\2\2\2\u0136\u06b8\3\2\2\2\u0138\u06bd\3\2\2\2\u013a\u06cb")
        buf.write("\3\2\2\2\u013c\u06d3\3\2\2\2\u013e\u06d6\3\2\2\2\u0140")
        buf.write("\u06db\3\2\2\2\u0142\u06f5\3\2\2\2\u0144\u06fa\3\2\2\2")
        buf.write("\u0146\u06fd\3\2\2\2\u0148\u071c\3\2\2\2\u014a\u0721\3")
        buf.write("\2\2\2\u014c\u0724\3\2\2\2\u014e\u0728\3\2\2\2\u0150\u072b")
        buf.write("\3\2\2\2\u0152\u0739\3\2\2\2\u0154\u073f\3\2\2\2\u0156")
        buf.write("\u0741\3\2\2\2\u0158\u0750\3\2\2\2\u015a\u0755\3\2\2\2")
        buf.write("\u015c\u0763\3\2\2\2\u015e\u0768\3\2\2\2\u0160\u076e\3")
        buf.write("\2\2\2\u0162\u0771\3\2\2\2\u0164\u0779\3\2\2\2\u0166\u078b")
        buf.write("\3\2\2\2\u0168\u0790\3\2\2\2\u016a\u0794\3\2\2\2\u016c")
        buf.write("\u07b3\3\2\2\2\u016e\u07b6\3\2\2\2\u0170\u07c2\3\2\2\2")
        buf.write("\u0172\u07ce\3\2\2\2\u0174\u07d0\3\2\2\2\u0176\u07d6\3")
        buf.write("\2\2\2\u0178\u07d8\3\2\2\2\u017a\u07dc\3\2\2\2\u017c\u07df")
        buf.write("\3\2\2\2\u017e\u07ea\3\2\2\2\u0180\u07f5\3\2\2\2\u0182")
        buf.write("\u07fb\3\2\2\2\u0184\u07fe\3\2\2\2\u0186\u0809\3\2\2\2")
        buf.write("\u0188\u0811\3\2\2\2\u018a\u081b\3\2\2\2\u018c\u081f\3")
        buf.write("\2\2\2\u018e\u0821\3\2\2\2\u0190\u0826\3\2\2\2\u0192\u082f")
        buf.write("\3\2\2\2\u0194\u083c\3\2\2\2\u0196\u083f\3\2\2\2\u0198")
        buf.write("\u084a\3\2\2\2\u019a\u085f\3\2\2\2\u019c\u0861\3\2\2\2")
        buf.write("\u019e\u0867\3\2\2\2\u01a0\u086a\3\2\2\2\u01a2\u0874\3")
        buf.write("\2\2\2\u01a4\u0881\3\2\2\2\u01a6\u088d\3\2\2\2\u01a8\u088f")
        buf.write("\3\2\2\2\u01aa\u08a1\3\2\2\2\u01ac\u08ad\3\2\2\2\u01ae")
        buf.write("\u08b7\3\2\2\2\u01b0\u08bd\3\2\2\2\u01b2\u08cf\3\2\2\2")
        buf.write("\u01b4\u08eb\3\2\2\2\u01b6\u0904\3\2\2\2\u01b8\u0909\3")
        buf.write("\2\2\2\u01ba\u0913\3\2\2\2\u01bc\u0915\3\2\2\2\u01be\u091c")
        buf.write("\3\2\2\2\u01c0\u0922\3\2\2\2\u01c2\u0928\3\2\2\2\u01c4")
        buf.write("\u0934\3\2\2\2\u01c6\u0942\3\2\2\2\u01c8\u0952\3\2\2\2")
        buf.write("\u01ca\u0957\3\2\2\2\u01cc\u095a\3\2\2\2\u01ce\u095e\3")
        buf.write("\2\2\2\u01d0\u0960\3\2\2\2\u01d2\u0969\3\2\2\2\u01d4\u0979")
        buf.write("\3\2\2\2\u01d6\u097c\3\2\2\2\u01d8\u0982\3\2\2\2\u01da")
        buf.write("\u0990\3\2\2\2\u01dc\u0994\3\2\2\2\u01de\u0996\3\2\2\2")
        buf.write("\u01e0\u099f\3\2\2\2\u01e2\u09a4\3\2\2\2\u01e4\u09aa\3")
        buf.write("\2\2\2\u01e6\u09b4\3\2\2\2\u01e8\u09b7\3\2\2\2\u01ea\u09ba")
        buf.write("\3\2\2\2\u01ec\u09c6\3\2\2\2\u01ee\u09c8\3\2\2\2\u01f0")
        buf.write("\u09d6\3\2\2\2\u01f2\u09e4\3\2\2\2\u01f4\u09f0\3\2\2\2")
        buf.write("\u01f6\u09f8\3\2\2\2\u01f8\u0a05\3\2\2\2\u01fa\u0a1c\3")
        buf.write("\2\2\2\u01fc\u0a1e\3\2\2\2\u01fe\u01ff\t\2\2\2\u01ff\3")
        buf.write("\3\2\2\2\u0200\u0201\7\4\2\2\u0201\u0202\5\u01d8\u00ed")
        buf.write("\2\u0202\5\3\2\2\2\u0203\u0205\5\u00eav\2\u0204\u0206")
        buf.write("\5\u01e8\u00f5\2\u0205\u0204\3\2\2\2\u0205\u0206\3\2\2")
        buf.write("\2\u0206\u0209\3\2\2\2\u0207\u0208\7\u0089\2\2\u0208\u020a")
        buf.write("\5\u00c2b\2\u0209\u0207\3\2\2\2\u0209\u020a\3\2\2\2\u020a")
        buf.write("\u020b\3\2\2\2\u020b\u020c\7\5\2\2\u020c\7\3\2\2\2\u020d")
        buf.write("\u0210\5\u00c2b\2\u020e\u0210\7>\2\2\u020f\u020d\3\2\2")
        buf.write("\2\u020f\u020e\3\2\2\2\u0210\t\3\2\2\2\u0211\u0212\5,")
        buf.write("\27\2\u0212\13\3\2\2\2\u0213\u0214\5\u0126\u0094\2\u0214")
        buf.write("\u0215\7\u008f\2\2\u0215\u0216\5\b\5\2\u0216\u0217\7\u0090")
        buf.write("\2\2\u0217\u021a\3\2\2\2\u0218\u021a\5\b\5\2\u0219\u0213")
        buf.write("\3\2\2\2\u0219\u0218\3\2\2\2\u021a\r\3\2\2\2\u021b\u021c")
        buf.write("\t\3\2\2\u021c\17\3\2\2\2\u021d\u021e\7\u008f\2\2\u021e")
        buf.write("\u0223\5\u0098M\2\u021f\u0220\7\u008d\2\2\u0220\u0222")
        buf.write("\5\u0098M\2\u0221\u021f\3\2\2\2\u0222\u0225\3\2\2\2\u0223")
        buf.write("\u0221\3\2\2\2\u0223\u0224\3\2\2\2\u0224\u0226\3\2\2\2")
        buf.write("\u0225\u0223\3\2\2\2\u0226\u0227\7\u0090\2\2\u0227\21")
        buf.write("\3\2\2\2\u0228\u0229\7\7\2\2\u0229\u022c\5\24\13\2\u022a")
        buf.write("\u022b\7\u0093\2\2\u022b\u022d\5\26\f\2\u022c\u022a\3")
        buf.write("\2\2\2\u022c\u022d\3\2\2\2\u022d\u022e\3\2\2\2\u022e\u022f")
        buf.write("\7+\2\2\u022f\u0231\5\u0126\u0094\2\u0230\u0232\5\u01a8")
        buf.write("\u00d5\2\u0231\u0230\3\2\2\2\u0231\u0232\3\2\2\2\u0232")
        buf.write("\u0233\3\2\2\2\u0233\u0234\7\u008c\2\2\u0234\23\3\2\2")
        buf.write("\2\u0235\u0239\5\u00e8u\2\u0236\u0239\7\u0080\2\2\u0237")
        buf.write("\u0239\7\u0081\2\2\u0238\u0235\3\2\2\2\u0238\u0236\3\2")
        buf.write("\2\2\u0238\u0237\3\2\2\2\u0239\25\3\2\2\2\u023a\u023d")
        buf.write("\5\u01c2\u00e2\2\u023b\u023d\5\u01d8\u00ed\2\u023c\u023a")
        buf.write("\3\2\2\2\u023c\u023b\3\2\2\2\u023d\27\3\2\2\2\u023e\u0241")
        buf.write("\7\66\2\2\u023f\u0242\5\u016e\u00b8\2\u0240\u0242\5\u01d8")
        buf.write("\u00ed\2\u0241\u023f\3\2\2\2\u0241\u0240\3\2\2\2\u0242")
        buf.write("\31\3\2\2\2\u0243\u0244\7\n\2\2\u0244\u0245\5\u00e8u\2")
        buf.write("\u0245\u0246\7<\2\2\u0246\u0247\5\u00e8u\2\u0247\u0248")
        buf.write("\7+\2\2\u0248\u0249\5\34\17\2\u0249\u024a\7\16\2\2\u024a")
        buf.write("\u024b\5 \21\2\u024b\u024d\7\32\2\2\u024c\u024e\7\n\2")
        buf.write("\2\u024d\u024c\3\2\2\2\u024d\u024e\3\2\2\2\u024e\u0250")
        buf.write("\3\2\2\2\u024f\u0251\5\u00e8u\2\u0250\u024f\3\2\2\2\u0250")
        buf.write("\u0251\3\2\2\2\u0251\u0252\3\2\2\2\u0252\u0253\7\u008c")
        buf.write("\2\2\u0253\33\3\2\2\2\u0254\u0256\5:\36\2\u0255\u0254")
        buf.write("\3\2\2\2\u0256\u0259\3\2\2\2\u0257\u0255\3\2\2\2\u0257")
        buf.write("\u0258\3\2\2\2\u0258\35\3\2\2\2\u0259\u0257\3\2\2\2\u025a")
        buf.write("\u0270\5B\"\2\u025b\u0270\5\u016a\u00b6\2\u025c\u025e")
        buf.write("\5\u0112\u008a\2\u025d\u025c\3\2\2\2\u025d\u025e\3\2\2")
        buf.write("\2\u025e\u025f\3\2\2\2\u025f\u0270\5h\65\2\u0260\u0262")
        buf.write("\5\u0112\u008a\2\u0261\u0260\3\2\2\2\u0261\u0262\3\2\2")
        buf.write("\2\u0262\u0263\3\2\2\2\u0263\u0270\5d\63\2\u0264\u0266")
        buf.write("\5\u0112\u008a\2\u0265\u0264\3\2\2\2\u0265\u0266\3\2\2")
        buf.write("\2\u0266\u0268\3\2\2\2\u0267\u0269\7D\2\2\u0268\u0267")
        buf.write("\3\2\2\2\u0268\u0269\3\2\2\2\u0269\u026a\3\2\2\2\u026a")
        buf.write("\u0270\5j\66\2\u026b\u0270\5\\/\2\u026c\u0270\5\u00d4")
        buf.write("k\2\u026d\u0270\5f\64\2\u026e\u0270\5\u01b6\u00dc\2\u026f")
        buf.write("\u025a\3\2\2\2\u026f\u025b\3\2\2\2\u026f\u025d\3\2\2\2")
        buf.write("\u026f\u0261\3\2\2\2\u026f\u0265\3\2\2\2\u026f\u026b\3")
        buf.write("\2\2\2\u026f\u026c\3\2\2\2\u026f\u026d\3\2\2\2\u026f\u026e")
        buf.write("\3\2\2\2\u0270\37\3\2\2\2\u0271\u0273\5\36\20\2\u0272")
        buf.write("\u0271\3\2\2\2\u0273\u0276\3\2\2\2\u0274\u0272\3\2\2\2")
        buf.write("\u0274\u0275\3\2\2\2\u0275!\3\2\2\2\u0276\u0274\3\2\2")
        buf.write("\2\u0277\u027a\5\u01f0\u00f9\2\u0278\u027a\5\u0082B\2")
        buf.write("\u0279\u0277\3\2\2\2\u0279\u0278\3\2\2\2\u027a#\3\2\2")
        buf.write("\2\u027b\u027e\5\u01ee\u00f8\2\u027c\u027e\5\u0080A\2")
        buf.write("\u027d\u027b\3\2\2\2\u027d\u027c\3\2\2\2\u027e%\3\2\2")
        buf.write("\2\u027f\u0280\7\f\2\2\u0280\u0283\5l\67\2\u0281\u0282")
        buf.write("\7Q\2\2\u0282\u0284\5\u00c2b\2\u0283\u0281\3\2\2\2\u0283")
        buf.write("\u0284\3\2\2\2\u0284\u0287\3\2\2\2\u0285\u0286\7V\2\2")
        buf.write("\u0286\u0288\5\u00c2b\2\u0287\u0285\3\2\2\2\u0287\u0288")
        buf.write("\3\2\2\2\u0288\'\3\2\2\2\u0289\u028b\5\u0112\u008a\2\u028a")
        buf.write("\u0289\3\2\2\2\u028a\u028b\3\2\2\2\u028b\u028c\3\2\2\2")
        buf.write("\u028c\u028d\5&\24\2\u028d\u028e\7\u008c\2\2\u028e)\3")
        buf.write("\2\2\2\u028f\u0290\5\u00d0i\2\u0290\u0291\7\u0087\2\2")
        buf.write("\u0291\u0293\3\2\2\2\u0292\u028f\3\2\2\2\u0292\u0293\3")
        buf.write("\2\2\2\u0293\u0294\3\2\2\2\u0294\u0295\5\f\7\2\u0295+")
        buf.write("\3\2\2\2\u0296\u029b\5*\26\2\u0297\u0298\7\u008d\2\2\u0298")
        buf.write("\u029a\5*\26\2\u0299\u0297\3\2\2\2\u029a\u029d\3\2\2\2")
        buf.write("\u029b\u0299\3\2\2\2\u029b\u029c\3\2\2\2\u029c-\3\2\2")
        buf.write("\2\u029d\u029b\3\2\2\2\u029e\u029f\7\r\2\2\u029f\u02a0")
        buf.write("\5\u0112\u008a\2\u02a0\u02a1\5\u0126\u0094\2\u02a1\u02a2")
        buf.write("\7\u008c\2\2\u02a2/\3\2\2\2\u02a3\u02ab\5\u00e8u\2\u02a4")
        buf.write("\u02ab\7J\2\2\u02a5\u02ab\7K\2\2\u02a6\u02ab\7\5\2\2\u02a7")
        buf.write("\u02ab\7b\2\2\u02a8\u02ab\7O\2\2\u02a9\u02ab\7d\2\2\u02aa")
        buf.write("\u02a3\3\2\2\2\u02aa\u02a4\3\2\2\2\u02aa\u02a5\3\2\2\2")
        buf.write("\u02aa\u02a6\3\2\2\2\u02aa\u02a7\3\2\2\2\u02aa\u02a8\3")
        buf.write("\2\2\2\u02aa\u02a9\3\2\2\2\u02ab\61\3\2\2\2\u02ac\u02ad")
        buf.write("\7\r\2\2\u02ad\u02ae\5\60\31\2\u02ae\u02af\7<\2\2\u02af")
        buf.write("\u02b0\5\u00b4[\2\u02b0\u02b1\7+\2\2\u02b1\u02b2\5\u00c2")
        buf.write("b\2\u02b2\u02b3\7\u008c\2\2\u02b3\63\3\2\2\2\u02b4\u02b5")
        buf.write("\5\u00e8u\2\u02b5\u02b6\7\u008c\2\2\u02b6\65\3\2\2\2\u02b7")
        buf.write("\u02b8\7j\2\2\u02b8\u02ba\5\u00a0Q\2\u02b9\u02b7\3\2\2")
        buf.write("\2\u02b9\u02ba\3\2\2\2\u02ba\u02bc\3\2\2\2\u02bb\u02bd")
        buf.write("\5\u00dco\2\u02bc\u02bb\3\2\2\2\u02bc\u02bd\3\2\2\2\u02bd")
        buf.write("\u02bf\3\2\2\2\u02be\u02c0\5\u0156\u00ac\2\u02bf\u02be")
        buf.write("\3\2\2\2\u02bf\u02c0\3\2\2\2\u02c0\67\3\2\2\2\u02c1\u02c2")
        buf.write("\7 \2\2\u02c2\u02c6\5@!\2\u02c3\u02c5\5\u01f2\u00fa\2")
        buf.write("\u02c4\u02c3\3\2\2\2\u02c5\u02c8\3\2\2\2\u02c6\u02c4\3")
        buf.write("\2\2\2\u02c6\u02c7\3\2\2\2\u02c7\u02cc\3\2\2\2\u02c8\u02c6")
        buf.write("\3\2\2\2\u02c9\u02cb\5z>\2\u02ca\u02c9\3\2\2\2\u02cb\u02ce")
        buf.write("\3\2\2\2\u02cc\u02ca\3\2\2\2\u02cc\u02cd\3\2\2\2\u02cd")
        buf.write("\u02cf\3\2\2\2\u02ce\u02cc\3\2\2\2\u02cf\u02d0\7\32\2")
        buf.write("\2\u02d0\u02d1\7 \2\2\u02d1\u02d2\7\u008c\2\2\u02d29\3")
        buf.write("\2\2\2\u02d3\u02ea\5\u01c6\u00e4\2\u02d4\u02ea\5\u01c4")
        buf.write("\u00e3\2\u02d5\u02ea\5\u01ea\u00f6\2\u02d6\u02ea\5\u01d6")
        buf.write("\u00ec\2\u02d7\u02ea\5~@\2\u02d8\u02ea\5\u01a2\u00d2\2")
        buf.write("\u02d9\u02ea\5\u01f6\u00fc\2\u02da\u02ea\5\u00c6d\2\u02db")
        buf.write("\u02ea\5\22\n\2\u02dc\u02ea\5Z.\2\u02dd\u02ea\5.\30\2")
        buf.write("\u02de\u02ea\5\62\32\2\u02df\u02ea\5|?\2\u02e0\u02ea\5")
        buf.write("\u0094K\2\u02e1\u02ea\5\u01be\u00e0\2\u02e2\u02ea\5\u01f2")
        buf.write("\u00fa\2\u02e3\u02ea\5\u00e4s\2\u02e4\u02ea\5\u00e2r\2")
        buf.write("\u02e5\u02ea\5\u0132\u009a\2\u02e6\u02ea\5\u01c0\u00e1")
        buf.write("\2\u02e7\u02ea\5\u0170\u00b9\2\u02e8\u02ea\5\u01e2\u00f2")
        buf.write("\2\u02e9\u02d3\3\2\2\2\u02e9\u02d4\3\2\2\2\u02e9\u02d5")
        buf.write("\3\2\2\2\u02e9\u02d6\3\2\2\2\u02e9\u02d7\3\2\2\2\u02e9")
        buf.write("\u02d8\3\2\2\2\u02e9\u02d9\3\2\2\2\u02e9\u02da\3\2\2\2")
        buf.write("\u02e9\u02db\3\2\2\2\u02e9\u02dc\3\2\2\2\u02e9\u02dd\3")
        buf.write("\2\2\2\u02e9\u02de\3\2\2\2\u02e9\u02df\3\2\2\2\u02e9\u02e0")
        buf.write("\3\2\2\2\u02e9\u02e1\3\2\2\2\u02e9\u02e2\3\2\2\2\u02e9")
        buf.write("\u02e3\3\2\2\2\u02e9\u02e4\3\2\2\2\u02e9\u02e5\3\2\2\2")
        buf.write("\u02e9\u02e6\3\2\2\2\u02e9\u02e7\3\2\2\2\u02e9\u02e8\3")
        buf.write("\2\2\2\u02ea;\3\2\2\2\u02eb\u02ed\5:\36\2\u02ec\u02eb")
        buf.write("\3\2\2\2\u02ed\u02f0\3\2\2\2\u02ee\u02ec\3\2\2\2\u02ee")
        buf.write("\u02ef\3\2\2\2\u02ef=\3\2\2\2\u02f0\u02ee\3\2\2\2\u02f1")
        buf.write("\u02f5\5\u00d8m\2\u02f2\u02f3\5\u00dco\2\u02f3\u02f4\7")
        buf.write("\u008c\2\2\u02f4\u02f6\3\2\2\2\u02f5\u02f2\3\2\2\2\u02f5")
        buf.write("\u02f6\3\2\2\2\u02f6\u02f8\3\2\2\2\u02f7\u02f1\3\2\2\2")
        buf.write("\u02f7\u02f8\3\2\2\2\u02f8\u02ff\3\2\2\2\u02f9\u02fd\5")
        buf.write("\u0152\u00aa\2\u02fa\u02fb\5\u0156\u00ac\2\u02fb\u02fc")
        buf.write("\7\u008c\2\2\u02fc\u02fe\3\2\2\2\u02fd\u02fa\3\2\2\2\u02fd")
        buf.write("\u02fe\3\2\2\2\u02fe\u0300\3\2\2\2\u02ff\u02f9\3\2\2\2")
        buf.write("\u02ff\u0300\3\2\2\2\u0300?\3\2\2\2\u0301\u0306\5\u00e8")
        buf.write("u\2\u0302\u0303\7\u008f\2\2\u0303\u0304\5\u00f0y\2\u0304")
        buf.write("\u0305\7\u0090\2\2\u0305\u0307\3\2\2\2\u0306\u0302\3\2")
        buf.write("\2\2\u0306\u0307\3\2\2\2\u0307\u030a\3\2\2\2\u0308\u030a")
        buf.write("\5\u0126\u0094\2\u0309\u0301\3\2\2\2\u0309\u0308\3\2\2")
        buf.write("\2\u030aA\3\2\2\2\u030b\u030c\5\u0112\u008a\2\u030c\u0311")
        buf.write("\7\17\2\2\u030d\u030e\7\u008f\2\2\u030e\u030f\5\u00c2")
        buf.write("b\2\u030f\u0310\7\u0090\2\2\u0310\u0312\3\2\2\2\u0311")
        buf.write("\u030d\3\2\2\2\u0311\u0312\3\2\2\2\u0312\u0314\3\2\2\2")
        buf.write("\u0313\u0315\7+\2\2\u0314\u0313\3\2\2\2\u0314\u0315\3")
        buf.write("\2\2\2\u0315\u0316\3\2\2\2\u0316\u0317\5> \2\u0317\u0318")
        buf.write("\5<\37\2\u0318\u0319\7\16\2\2\u0319\u031a\5D#\2\u031a")
        buf.write("\u031b\7\32\2\2\u031b\u031d\7\17\2\2\u031c\u031e\5\u00e8")
        buf.write("u\2\u031d\u031c\3\2\2\2\u031d\u031e\3\2\2\2\u031e\u031f")
        buf.write("\3\2\2\2\u031f\u0320\7\u008c\2\2\u0320C\3\2\2\2\u0321")
        buf.write("\u0323\5\36\20\2\u0322\u0321\3\2\2\2\u0323\u0326\3\2\2")
        buf.write("\2\u0324\u0322\3\2\2\2\u0324\u0325\3\2\2\2\u0325E\3\2")
        buf.write("\2\2\u0326\u0324\3\2\2\2\u0327\u0329\7I\2\2\u0328\u032a")
        buf.write("\5\6\4\2\u0329\u0328\3\2\2\2\u0329\u032a\3\2\2\2\u032a")
        buf.write("\u032c\3\2\2\2\u032b\u032d\5\u01e4\u00f3\2\u032c\u032b")
        buf.write("\3\2\2\2\u032c\u032d\3\2\2\2\u032d\u032e\3\2\2\2\u032e")
        buf.write("\u032f\5\u01e0\u00f1\2\u032f\u0330\7\u008c\2\2\u0330G")
        buf.write("\3\2\2\2\u0331\u0333\5L\'\2\u0332\u0331\3\2\2\2\u0332")
        buf.write("\u0333\3\2\2\2\u0333\u0334\3\2\2\2\u0334\u0335\5\u0126")
        buf.write("\u0094\2\u0335\u0336\7\u0087\2\2\u0336\u0337\5\u00c2b")
        buf.write("\2\u0337I\3\2\2\2\u0338\u033d\5H%\2\u0339\u033a\7\u008d")
        buf.write("\2\2\u033a\u033c\5H%\2\u033b\u0339\3\2\2\2\u033c\u033f")
        buf.write("\3\2\2\2\u033d\u033b\3\2\2\2\u033d\u033e\3\2\2\2\u033e")
        buf.write("K\3\2\2\2\u033f\u033d\3\2\2\2\u0340\u0341\7 \2\2\u0341")
        buf.write("\u0342\5\u0126\u0094\2\u0342\u0343\7j\2\2\u0343M\3\2\2")
        buf.write("\2\u0344\u0346\5\u0112\u008a\2\u0345\u0344\3\2\2\2\u0345")
        buf.write("\u0346\3\2\2\2\u0346\u0347\3\2\2\2\u0347\u0349\7\21\2")
        buf.write("\2\u0348\u034a\5J&\2\u0349\u0348\3\2\2\2\u0349\u034a\3")
        buf.write("\2\2\2\u034a\u034d\3\2\2\2\u034b\u034c\7n\2\2\u034c\u034e")
        buf.write("\5l\67\2\u034d\u034b\3\2\2\2\u034d\u034e\3\2\2\2\u034e")
        buf.write("\u034f\3\2\2\2\u034f\u0350\7\u008c\2\2\u0350O\3\2\2\2")
        buf.write("\u0351\u0353\5\u0112\u008a\2\u0352\u0351\3\2\2\2\u0352")
        buf.write("\u0353\3\2\2\2\u0353\u0354\3\2\2\2\u0354\u0355\7\24\2")
        buf.write("\2\u0355\u0356\5\u00c2b\2\u0356\u0358\7+\2\2\u0357\u0359")
        buf.write("\5R*\2\u0358\u0357\3\2\2\2\u0359\u035a\3\2\2\2\u035a\u0358")
        buf.write("\3\2\2\2\u035a\u035b\3\2\2\2\u035b\u035c\3\2\2\2\u035c")
        buf.write("\u035d\7\32\2\2\u035d\u035f\7\24\2\2\u035e\u0360\5\u00e8")
        buf.write("u\2\u035f\u035e\3\2\2\2\u035f\u0360\3\2\2\2\u0360\u0361")
        buf.write("\3\2\2\2\u0361\u0362\7\u008c\2\2\u0362Q\3\2\2\2\u0363")
        buf.write("\u0364\7n\2\2\u0364\u0365\5V,\2\u0365\u0366\7\u0087\2")
        buf.write("\2\u0366\u0367\5\u0198\u00cd\2\u0367S\3\2\2\2\u0368\u036d")
        buf.write("\5\u00e8u\2\u0369\u036d\5\u0096L\2\u036a\u036d\5\u01aa")
        buf.write("\u00d6\2\u036b\u036d\7@\2\2\u036c\u0368\3\2\2\2\u036c")
        buf.write("\u0369\3\2\2\2\u036c\u036a\3\2\2\2\u036c\u036b\3\2\2\2")
        buf.write("\u036dU\3\2\2\2\u036e\u0373\5T+\2\u036f\u0370\7\u009b")
        buf.write("\2\2\u0370\u0372\5T+\2\u0371\u036f\3\2\2\2\u0372\u0375")
        buf.write("\3\2\2\2\u0373\u0371\3\2\2\2\u0373\u0374\3\2\2\2\u0374")
        buf.write("W\3\2\2\2\u0375\u0373\3\2\2\2\u0376\u0377\7 \2\2\u0377")
        buf.write("\u037b\5^\60\2\u0378\u0379\5\66\34\2\u0379\u037a\7\u008c")
        buf.write("\2\2\u037a\u037c\3\2\2\2\u037b\u0378\3\2\2\2\u037b\u037c")
        buf.write("\3\2\2\2\u037c\u037e\3\2\2\2\u037d\u037f\58\35\2\u037e")
        buf.write("\u037d\3\2\2\2\u037e\u037f\3\2\2\2\u037f\u0380\3\2\2\2")
        buf.write("\u0380\u0381\7\32\2\2\u0381\u0382\7 \2\2\u0382\u0383\7")
        buf.write("\u008c\2\2\u0383Y\3\2\2\2\u0384\u0385\7\25\2\2\u0385\u0387")
        buf.write("\5\u00e8u\2\u0386\u0388\7+\2\2\u0387\u0386\3\2\2\2\u0387")
        buf.write("\u0388\3\2\2\2\u0388\u038a\3\2\2\2\u0389\u038b\5\u00d8")
        buf.write("m\2\u038a\u0389\3\2\2\2\u038a\u038b\3\2\2\2\u038b\u038d")
        buf.write("\3\2\2\2\u038c\u038e\5\u0152\u00aa\2\u038d\u038c\3\2\2")
        buf.write("\2\u038d\u038e\3\2\2\2\u038e\u038f\3\2\2\2\u038f\u0390")
        buf.write("\7\32\2\2\u0390\u0392\7\25\2\2\u0391\u0393\5\u00e8u\2")
        buf.write("\u0392\u0391\3\2\2\2\u0392\u0393\3\2\2\2\u0393\u0394\3")
        buf.write("\2\2\2\u0394\u0395\7\u008c\2\2\u0395[\3\2\2\2\u0396\u0397")
        buf.write("\5\u0112\u008a\2\u0397\u0399\5\u00f4{\2\u0398\u039a\5")
        buf.write("\u00dco\2\u0399\u0398\3\2\2\2\u0399\u039a\3\2\2\2\u039a")
        buf.write("\u039c\3\2\2\2\u039b\u039d\5\u0156\u00ac\2\u039c\u039b")
        buf.write("\3\2\2\2\u039c\u039d\3\2\2\2\u039d\u039e\3\2\2\2\u039e")
        buf.write("\u039f\7\u008c\2\2\u039f]\3\2\2\2\u03a0\u03a1\5\u00f6")
        buf.write("|\2\u03a1\u03a2\7\u0093\2\2\u03a2\u03a3\5\u0126\u0094")
        buf.write("\2\u03a3_\3\2\2\2\u03a4\u03a7\5\"\22\2\u03a5\u03a7\5\u017c")
        buf.write("\u00bf\2\u03a6\u03a4\3\2\2\2\u03a6\u03a5\3\2\2\2\u03a7")
        buf.write("a\3\2\2\2\u03a8\u03ab\5$\23\2\u03a9\u03ab\5\u017e\u00c0")
        buf.write("\2\u03aa\u03a8\3\2\2\2\u03aa\u03a9\3\2\2\2\u03abc\3\2")
        buf.write("\2\2\u03ac\u03ae\5\u0112\u008a\2\u03ad\u03ac\3\2\2\2\u03ad")
        buf.write("\u03ae\3\2\2\2\u03ae\u03b0\3\2\2\2\u03af\u03b1\7D\2\2")
        buf.write("\u03b0\u03af\3\2\2\2\u03b0\u03b1\3\2\2\2\u03b1\u03b2\3")
        buf.write("\2\2\2\u03b2\u03b3\5&\24\2\u03b3\u03b4\7\u008c\2\2\u03b4")
        buf.write("e\3\2\2\2\u03b5\u03b7\5\u0112\u008a\2\u03b6\u03b5\3\2")
        buf.write("\2\2\u03b6\u03b7\3\2\2\2\u03b7\u03b8\3\2\2\2\u03b8\u03ba")
        buf.write("\7\21\2\2\u03b9\u03bb\5J&\2\u03ba\u03b9\3\2\2\2\u03ba")
        buf.write("\u03bb\3\2\2\2\u03bb\u03bd\3\2\2\2\u03bc\u03be\5\u0194")
        buf.write("\u00cb\2\u03bd\u03bc\3\2\2\2\u03bd\u03be\3\2\2\2\u03be")
        buf.write("\u03c1\3\2\2\2\u03bf\u03c0\7n\2\2\u03c0\u03c2\5l\67\2")
        buf.write("\u03c1\u03bf\3\2\2\2\u03c1\u03c2\3\2\2\2\u03c2\u03c3\3")
        buf.write("\2\2\2\u03c3\u03c4\7\u008c\2\2\u03c4g\3\2\2\2\u03c5\u03c7")
        buf.write("\5\u0112\u008a\2\u03c6\u03c5\3\2\2\2\u03c6\u03c7\3\2\2")
        buf.write("\2\u03c7\u03c9\3\2\2\2\u03c8\u03ca\7D\2\2\u03c9\u03c8")
        buf.write("\3\2\2\2\u03c9\u03ca\3\2\2\2\u03ca\u03cb\3\2\2\2\u03cb")
        buf.write("\u03cc\5\u0162\u00b2\2\u03cc\u03cd\7\u008c\2\2\u03cdi")
        buf.write("\3\2\2\2\u03ce\u03d0\5\u0112\u008a\2\u03cf\u03ce\3\2\2")
        buf.write("\2\u03cf\u03d0\3\2\2\2\u03d0\u03d2\3\2\2\2\u03d1\u03d3")
        buf.write("\7D\2\2\u03d2\u03d1\3\2\2\2\u03d2\u03d3\3\2\2\2\u03d3")
        buf.write("\u03d6\3\2\2\2\u03d4\u03d7\5p9\2\u03d5\u03d7\5\u0190\u00c9")
        buf.write("\2\u03d6\u03d4\3\2\2\2\u03d6\u03d5\3\2\2\2\u03d7k\3\2")
        buf.write("\2\2\u03d8\u03d9\5\u00c2b\2\u03d9m\3\2\2\2\u03da\u03db")
        buf.write("\7i\2\2\u03db\u03dc\5l\67\2\u03dco\3\2\2\2\u03dd\u03de")
        buf.write("\5\u01dc\u00ef\2\u03de\u03df\7\u0085\2\2\u03df\u03e0\5")
        buf.write("\u013e\u00a0\2\u03e0\u03e1\5r:\2\u03e1\u03e2\7\u008c\2")
        buf.write("\2\u03e2q\3\2\2\2\u03e3\u03ea\5\u01fa\u00fe\2\u03e4\u03e5")
        buf.write("\7n\2\2\u03e5\u03e8\5l\67\2\u03e6\u03e7\7\34\2\2\u03e7")
        buf.write("\u03e9\5r:\2\u03e8\u03e6\3\2\2\2\u03e8\u03e9\3\2\2\2\u03e9")
        buf.write("\u03eb\3\2\2\2\u03ea\u03e4\3\2\2\2\u03ea\u03eb\3\2\2\2")
        buf.write("\u03ebs\3\2\2\2\u03ec\u03ed\7\26\2\2\u03ed\u03ee\5\u00e8")
        buf.write("u\2\u03ee\u03ef\7<\2\2\u03ef\u03f0\5\u0126\u0094\2\u03f0")
        buf.write("\u03f1\7+\2\2\u03f1\u03f2\5x=\2\u03f2\u03f3\58\35\2\u03f3")
        buf.write("\u03f5\7\32\2\2\u03f4\u03f6\7\26\2\2\u03f5\u03f4\3\2\2")
        buf.write("\2\u03f5\u03f6\3\2\2\2\u03f6\u03f8\3\2\2\2\u03f7\u03f9")
        buf.write("\5\u00e8u\2\u03f8\u03f7\3\2\2\2\u03f8\u03f9\3\2\2\2\u03f9")
        buf.write("\u03fa\3\2\2\2\u03fa\u03fb\7\u008c\2\2\u03fbu\3\2\2\2")
        buf.write("\u03fc\u0400\5\u01f2\u00fa\2\u03fd\u0400\5\62\32\2\u03fe")
        buf.write("\u0400\5\u00e2r\2\u03ff\u03fc\3\2\2\2\u03ff\u03fd\3\2")
        buf.write("\2\2\u03ff\u03fe\3\2\2\2\u0400w\3\2\2\2\u0401\u0403\5")
        buf.write("v<\2\u0402\u0401\3\2\2\2\u0403\u0406\3\2\2\2\u0404\u0402")
        buf.write("\3\2\2\2\u0404\u0405\3\2\2\2\u0405y\3\2\2\2\u0406\u0404")
        buf.write("\3\2\2\2\u0407\u040a\58\35\2\u0408\u040a\5X-\2\u0409\u0407")
        buf.write("\3\2\2\2\u0409\u0408\3\2\2\2\u040a{\3\2\2\2\u040b\u040c")
        buf.write("\7 \2\2\u040c\u040d\5^\60\2\u040d\u040e\5\66\34\2\u040e")
        buf.write("\u040f\7\u008c\2\2\u040f}\3\2\2\2\u0410\u0411\7\27\2\2")
        buf.write("\u0411\u0412\5\u00eav\2\u0412\u0413\7\u0093\2\2\u0413")
        buf.write("\u0416\5\u01d8\u00ed\2\u0414\u0415\7\u0089\2\2\u0415\u0417")
        buf.write("\5\u00c2b\2\u0416\u0414\3\2\2\2\u0416\u0417\3\2\2\2\u0417")
        buf.write("\u0418\3\2\2\2\u0418\u0419\7\u008c\2\2\u0419\177\3\2\2")
        buf.write("\2\u041a\u041b\7\13\2\2\u041b\u041c\5\u00eex\2\u041c\u041d")
        buf.write("\7<\2\2\u041d\u041e\5\u01d8\u00ed\2\u041e\u0081\3\2\2")
        buf.write("\2\u041f\u0420\7\13\2\2\u0420\u0421\5\u00eex\2\u0421\u0422")
        buf.write("\7<\2\2\u0422\u0423\5\u01c2\u00e2\2\u0423\u0083\3\2\2")
        buf.write("\2\u0424\u0427\5\u017a\u00be\2\u0425\u0427\5\u00eex\2")
        buf.write("\u0426\u0424\3\2\2\2\u0426\u0425\3\2\2\2\u0427\u0085\3")
        buf.write("\2\2\2\u0428\u042a\5\u0088E\2\u0429\u0428\3\2\2\2\u042a")
        buf.write("\u042d\3\2\2\2\u042b\u0429\3\2\2\2\u042b\u042c\3\2\2\2")
        buf.write("\u042c\u0087\3\2\2\2\u042d\u042b\3\2\2\2\u042e\u0431\5")
        buf.write("\u0114\u008b\2\u042f\u0431\5\u01f2\u00fa\2\u0430\u042e")
        buf.write("\3\2\2\2\u0430\u042f\3\2\2\2\u0431\u0089\3\2\2\2\u0432")
        buf.write("\u0439\7e\2\2\u0433\u0434\7L\2\2\u0434\u0436\5\u00c2b")
        buf.write("\2\u0435\u0433\3\2\2\2\u0435\u0436\3\2\2\2\u0436\u0437")
        buf.write("\3\2\2\2\u0437\u0439\7)\2\2\u0438\u0432\3\2\2\2\u0438")
        buf.write("\u0435\3\2\2\2\u0439\u008b\3\2\2\2\u043a\u043c\5\u008e")
        buf.write("H\2\u043b\u043a\3\2\2\2\u043c\u043f\3\2\2\2\u043d\u043b")
        buf.write("\3\2\2\2\u043d\u043e\3\2\2\2\u043e\u0440\3\2\2\2\u043f")
        buf.write("\u043d\3\2\2\2\u0440\u0441\7\2\2\3\u0441\u008d\3\2\2\2")
        buf.write("\u0442\u0443\5\u0086D\2\u0443\u0444\5\u0116\u008c\2\u0444")
        buf.write("\u008f\3\2\2\2\u0445\u0448\5\u00e8u\2\u0446\u0448\7\u0081")
        buf.write("\2\2\u0447\u0445\3\2\2\2\u0447\u0446\3\2\2\2\u0448\u0091")
        buf.write("\3\2\2\2\u0449\u044a\t\4\2\2\u044a\u0093\3\2\2\2\u044b")
        buf.write("\u044c\7\30\2\2\u044c\u044d\5\u00e6t\2\u044d\u044e\7\6")
        buf.write("\2\2\u044e\u044f\5\u00c2b\2\u044f\u0450\7\u008c\2\2\u0450")
        buf.write("\u0095\3\2\2\2\u0451\u0454\5\u0176\u00bc\2\u0452\u0454")
        buf.write("\5\u01d8\u00ed\2\u0453\u0451\3\2\2\2\u0453\u0452\3\2\2")
        buf.write("\2\u0454\u0097\3\2\2\2\u0455\u0456\5V,\2\u0456\u0457\7")
        buf.write("\u0087\2\2\u0457\u0459\3\2\2\2\u0458\u0455\3\2\2\2\u0458")
        buf.write("\u0459\3\2\2\2\u0459\u045a\3\2\2\2\u045a\u045b\5\u00c2")
        buf.write("b\2\u045b\u0099\3\2\2\2\u045c\u045d\5\u00eav\2\u045d\u045e")
        buf.write("\7\u0093\2\2\u045e\u045f\5\u009eP\2\u045f\u0460\7\u008c")
        buf.write("\2\2\u0460\u009b\3\2\2\2\u0461\u0462\5\u01c2\u00e2\2\u0462")
        buf.write("\u009d\3\2\2\2\u0463\u0464\5\u01d8\u00ed\2\u0464\u009f")
        buf.write("\3\2\2\2\u0465\u0466\7\33\2\2\u0466\u046b\5\u0126\u0094")
        buf.write("\2\u0467\u0468\7\u008f\2\2\u0468\u0469\5\u00e8u\2\u0469")
        buf.write("\u046a\7\u0090\2\2\u046a\u046c\3\2\2\2\u046b\u0467\3\2")
        buf.write("\2\2\u046b\u046c\3\2\2\2\u046c\u0471\3\2\2\2\u046d\u046e")
        buf.write("\7\26\2\2\u046e\u0471\5\u0126\u0094\2\u046f\u0471\7>\2")
        buf.write("\2\u0470\u0465\3\2\2\2\u0470\u046d\3\2\2\2\u0470\u046f")
        buf.write("\3\2\2\2\u0471\u00a1\3\2\2\2\u0472\u0473\t\5\2\2\u0473")
        buf.write("\u00a3\3\2\2\2\u0474\u0476\5\u00a2R\2\u0475\u0477\7\u008a")
        buf.write("\2\2\u0476\u0475\3\2\2\2\u0476\u0477\3\2\2\2\u0477\u00a5")
        buf.write("\3\2\2\2\u0478\u047d\5\u00a4S\2\u0479\u047a\7\u008d\2")
        buf.write("\2\u047a\u047c\5\u00a4S\2\u047b\u0479\3\2\2\2\u047c\u047f")
        buf.write("\3\2\2\2\u047d\u047b\3\2\2\2\u047d\u047e\3\2\2\2\u047e")
        buf.write("\u00a7\3\2\2\2\u047f\u047d\3\2\2\2\u0480\u0481\7\33\2")
        buf.write("\2\u0481\u0482\5\u00e8u\2\u0482\u0483\7+\2\2\u0483\u0484")
        buf.write("\5\u00b0Y\2\u0484\u0487\5\u00acW\2\u0485\u0486\7\16\2")
        buf.write("\2\u0486\u0488\5\u00b8]\2\u0487\u0485\3\2\2\2\u0487\u0488")
        buf.write("\3\2\2\2\u0488\u0489\3\2\2\2\u0489\u048b\7\32\2\2\u048a")
        buf.write("\u048c\7\33\2\2\u048b\u048a\3\2\2\2\u048b\u048c\3\2\2")
        buf.write("\2\u048c\u048e\3\2\2\2\u048d\u048f\5\u00e8u\2\u048e\u048d")
        buf.write("\3\2\2\2\u048e\u048f\3\2\2\2\u048f\u0490\3\2\2\2\u0490")
        buf.write("\u0491\7\u008c\2\2\u0491\u00a9\3\2\2\2\u0492\u04a7\5\u01c6")
        buf.write("\u00e4\2\u0493\u04a7\5\u01c4\u00e3\2\u0494\u04a7\5\u01ea")
        buf.write("\u00f6\2\u0495\u04a7\5\u01d6\u00ec\2\u0496\u04a7\5~@\2")
        buf.write("\u0497\u04a7\5\u01a2\u00d2\2\u0498\u04a7\5\u01f6\u00fc")
        buf.write("\2\u0499\u04a7\5\u00c6d\2\u049a\u04a7\5\22\n\2\u049b\u04a7")
        buf.write("\5.\30\2\u049c\u04a7\5\62\32\2\u049d\u04a7\5\u0094K\2")
        buf.write("\u049e\u04a7\5\u01be\u00e0\2\u049f\u04a7\5\u01f2\u00fa")
        buf.write("\2\u04a0\u04a7\5\u00e4s\2\u04a1\u04a7\5\u00e2r\2\u04a2")
        buf.write("\u04a7\5\u0132\u009a\2\u04a3\u04a7\5\u01c0\u00e1\2\u04a4")
        buf.write("\u04a7\5\u0170\u00b9\2\u04a5\u04a7\5\u01e2\u00f2\2\u04a6")
        buf.write("\u0492\3\2\2\2\u04a6\u0493\3\2\2\2\u04a6\u0494\3\2\2\2")
        buf.write("\u04a6\u0495\3\2\2\2\u04a6\u0496\3\2\2\2\u04a6\u0497\3")
        buf.write("\2\2\2\u04a6\u0498\3\2\2\2\u04a6\u0499\3\2\2\2\u04a6\u049a")
        buf.write("\3\2\2\2\u04a6\u049b\3\2\2\2\u04a6\u049c\3\2\2\2\u04a6")
        buf.write("\u049d\3\2\2\2\u04a6\u049e\3\2\2\2\u04a6\u049f\3\2\2\2")
        buf.write("\u04a6\u04a0\3\2\2\2\u04a6\u04a1\3\2\2\2\u04a6\u04a2\3")
        buf.write("\2\2\2\u04a6\u04a3\3\2\2\2\u04a6\u04a4\3\2\2\2\u04a6\u04a5")
        buf.write("\3\2\2\2\u04a7\u00ab\3\2\2\2\u04a8\u04aa\5\u00aaV\2\u04a9")
        buf.write("\u04a8\3\2\2\2\u04aa\u04ad\3\2\2\2\u04ab\u04a9\3\2\2\2")
        buf.write("\u04ab\u04ac\3\2\2\2\u04ac\u00ad\3\2\2\2\u04ad\u04ab\3")
        buf.write("\2\2\2\u04ae\u04b0\5\u00ba^\2\u04af\u04b1\5\u01a8\u00d5")
        buf.write("\2\u04b0\u04af\3\2\2\2\u04b0\u04b1\3\2\2\2\u04b1\u00af")
        buf.write("\3\2\2\2\u04b2\u04b4\5\u00d8m\2\u04b3\u04b2\3\2\2\2\u04b3")
        buf.write("\u04b4\3\2\2\2\u04b4\u04b6\3\2\2\2\u04b5\u04b7\5\u0152")
        buf.write("\u00aa\2\u04b6\u04b5\3\2\2\2\u04b6\u04b7\3\2\2\2\u04b7")
        buf.write("\u00b1\3\2\2\2\u04b8\u04bd\5\u00aeX\2\u04b9\u04ba\7\u008d")
        buf.write("\2\2\u04ba\u04bc\5\u00aeX\2\u04bb\u04b9\3\2\2\2\u04bc")
        buf.write("\u04bf\3\2\2\2\u04bd\u04bb\3\2\2\2\u04bd\u04be\3\2\2\2")
        buf.write("\u04be\u04c3\3\2\2\2\u04bf\u04bd\3\2\2\2\u04c0\u04c3\7")
        buf.write("@\2\2\u04c1\u04c3\7\b\2\2\u04c2\u04b8\3\2\2\2\u04c2\u04c0")
        buf.write("\3\2\2\2\u04c2\u04c1\3\2\2\2\u04c3\u00b3\3\2\2\2\u04c4")
        buf.write("\u04c5\5\u00b2Z\2\u04c5\u04c6\7\u0093\2\2\u04c6\u04c7")
        buf.write("\5\u00a2R\2\u04c7\u00b5\3\2\2\2\u04c8\u04cc\5d\63\2\u04c9")
        buf.write("\u04cc\5\u016a\u00b6\2\u04ca\u04cc\5h\65\2\u04cb\u04c8")
        buf.write("\3\2\2\2\u04cb\u04c9\3\2\2\2\u04cb\u04ca\3\2\2\2\u04cc")
        buf.write("\u00b7\3\2\2\2\u04cd\u04cf\5\u00b6\\\2\u04ce\u04cd\3\2")
        buf.write("\2\2\u04cf\u04d2\3\2\2\2\u04d0\u04ce\3\2\2\2\u04d0\u04d1")
        buf.write("\3\2\2\2\u04d1\u00b9\3\2\2\2\u04d2\u04d0\3\2\2\2\u04d3")
        buf.write("\u04d7\5\u00e8u\2\u04d4\u04d7\7\u0080\2\2\u04d5\u04d7")
        buf.write("\7\u0081\2\2\u04d6\u04d3\3\2\2\2\u04d6\u04d4\3\2\2\2\u04d6")
        buf.write("\u04d5\3\2\2\2\u04d7\u00bb\3\2\2\2\u04d8\u04db\5\u00e8")
        buf.write("u\2\u04d9\u04db\7\u0080\2\2\u04da\u04d8\3\2\2\2\u04da")
        buf.write("\u04d9\3\2\2\2\u04db\u00bd\3\2\2\2\u04dc\u04dd\7\u008f")
        buf.write("\2\2\u04dd\u04e2\5\u00bc_\2\u04de\u04df\7\u008d\2\2\u04df")
        buf.write("\u04e1\5\u00bc_\2\u04e0\u04de\3\2\2\2\u04e1\u04e4\3\2")
        buf.write("\2\2\u04e2\u04e0\3\2\2\2\u04e2\u04e3\3\2\2\2\u04e3\u04e5")
        buf.write("\3\2\2\2\u04e4\u04e2\3\2\2\2\u04e5\u04e6\7\u0090\2\2\u04e6")
        buf.write("\u00bf\3\2\2\2\u04e7\u04e9\5\u0112\u008a\2\u04e8\u04e7")
        buf.write("\3\2\2\2\u04e8\u04e9\3\2\2\2\u04e9\u04ea\3\2\2\2\u04ea")
        buf.write("\u04ec\7\36\2\2\u04eb\u04ed\5\u00e8u\2\u04ec\u04eb\3\2")
        buf.write("\2\2\u04ec\u04ed\3\2\2\2\u04ed\u04f0\3\2\2\2\u04ee\u04ef")
        buf.write("\7n\2\2\u04ef\u04f1\5l\67\2\u04f0\u04ee\3\2\2\2\u04f0")
        buf.write("\u04f1\3\2\2\2\u04f1\u04f2\3\2\2\2\u04f2\u04f3\7\u008c")
        buf.write("\2\2\u04f3\u00c1\3\2\2\2\u04f4\u04fa\5\u0180\u00c1\2\u04f5")
        buf.write("\u04f6\5\u011e\u0090\2\u04f6\u04f7\5\u0180\u00c1\2\u04f7")
        buf.write("\u04f9\3\2\2\2\u04f8\u04f5\3\2\2\2\u04f9\u04fc\3\2\2\2")
        buf.write("\u04fa\u04f8\3\2\2\2\u04fa\u04fb\3\2\2\2\u04fb\u00c3\3")
        buf.write("\2\2\2\u04fc\u04fa\3\2\2\2\u04fd\u0500\5\u0158\u00ad\2")
        buf.write("\u04fe\u04ff\7\u0083\2\2\u04ff\u0501\5\u0158\u00ad\2\u0500")
        buf.write("\u04fe\3\2\2\2\u0500\u0501\3\2\2\2\u0501\u0507\3\2\2\2")
        buf.write("\u0502\u0503\7\3\2\2\u0503\u0507\5\u0158\u00ad\2\u0504")
        buf.write("\u0505\7:\2\2\u0505\u0507\5\u0158\u00ad\2\u0506\u04fd")
        buf.write("\3\2\2\2\u0506\u0502\3\2\2\2\u0506\u0504\3\2\2\2\u0507")
        buf.write("\u00c5\3\2\2\2\u0508\u0509\7\37\2\2\u0509\u050a\5\u00ea")
        buf.write("v\2\u050a\u050b\7\u0093\2\2\u050b\u050d\5\u01d8\u00ed")
        buf.write("\2\u050c\u050e\5\u00caf\2\u050d\u050c\3\2\2\2\u050d\u050e")
        buf.write("\3\2\2\2\u050e\u050f\3\2\2\2\u050f\u0510\7\u008c\2\2\u0510")
        buf.write("\u00c7\3\2\2\2\u0511\u0512\5\u00c2b\2\u0512\u00c9\3\2")
        buf.write("\2\2\u0513\u0514\7>\2\2\u0514\u0516\5\u00c2b\2\u0515\u0513")
        buf.write("\3\2\2\2\u0515\u0516\3\2\2\2\u0516\u0517\3\2\2\2\u0517")
        buf.write("\u0518\7+\2\2\u0518\u0519\5\u00c8e\2\u0519\u00cb\3\2\2")
        buf.write("\2\u051a\u051b\7\37\2\2\u051b\u051c\7<\2\2\u051c\u051d")
        buf.write("\5\u01d8\u00ed\2\u051d\u00cd\3\2\2\2\u051e\u051f\5\u0104")
        buf.write("\u0083\2\u051f\u00cf\3\2\2\2\u0520\u0527\5\u00e8u\2\u0521")
        buf.write("\u0522\5\u00e8u\2\u0522\u0523\7\u008f\2\2\u0523\u0524")
        buf.write("\5\u0178\u00bd\2\u0524\u0525\7\u0090\2\2\u0525\u0527\3")
        buf.write("\2\2\2\u0526\u0520\3\2\2\2\u0526\u0521\3\2\2\2\u0527\u00d1")
        buf.write("\3\2\2\2\u0528\u0529\7I\2\2\u0529\u052a\5\u00eav\2\u052a")
        buf.write("\u052b\7\u0093\2\2\u052b\u052e\5\u01d8\u00ed\2\u052c\u052d")
        buf.write("\7\u0089\2\2\u052d\u052f\5\u00c2b\2\u052e\u052c\3\2\2")
        buf.write("\2\u052e\u052f\3\2\2\2\u052f\u0530\3\2\2\2\u0530\u0531")
        buf.write("\7\u008c\2\2\u0531\u00d3\3\2\2\2\u0532\u0533\5\u0112\u008a")
        buf.write("\2\u0533\u0534\5\u00d6l\2\u0534\u053c\7\"\2\2\u0535\u0537")
        buf.write("\5:\36\2\u0536\u0535\3\2\2\2\u0537\u053a\3\2\2\2\u0538")
        buf.write("\u0536\3\2\2\2\u0538\u0539\3\2\2\2\u0539\u053b\3\2\2\2")
        buf.write("\u053a\u0538\3\2\2\2\u053b\u053d\7\16\2\2\u053c\u0538")
        buf.write("\3\2\2\2\u053c\u053d\3\2\2\2\u053d\u0541\3\2\2\2\u053e")
        buf.write("\u0540\5\36\20\2\u053f\u053e\3\2\2\2\u0540\u0543\3\2\2")
        buf.write("\2\u0541\u053f\3\2\2\2\u0541\u0542\3\2\2\2\u0542\u0544")
        buf.write("\3\2\2\2\u0543\u0541\3\2\2\2\u0544\u0545\7\32\2\2\u0545")
        buf.write("\u0547\7\"\2\2\u0546\u0548\5\u00e8u\2\u0547\u0546\3\2")
        buf.write("\2\2\u0547\u0548\3\2\2\2\u0548\u0549\3\2\2\2\u0549\u054a")
        buf.write("\7\u008c\2\2\u054a\u00d5\3\2\2\2\u054b\u054c\7 \2\2\u054c")
        buf.write("\u0550\5\u014c\u00a7\2\u054d\u054e\7&\2\2\u054e\u0550")
        buf.write("\5l\67\2\u054f\u054b\3\2\2\2\u054f\u054d\3\2\2\2\u0550")
        buf.write("\u00d7\3\2\2\2\u0551\u0552\7#\2\2\u0552\u0553\7\u008f")
        buf.write("\2\2\u0553\u0554\5\u00dan\2\u0554\u0555\7\u0090\2\2\u0555")
        buf.write("\u0556\7\u008c\2\2\u0556\u00d9\3\2\2\2\u0557\u055c\5\u00f8")
        buf.write("}\2\u0558\u0559\7\u008c\2\2\u0559\u055b\5\u00f8}\2\u055a")
        buf.write("\u0558\3\2\2\2\u055b\u055e\3\2\2\2\u055c\u055a\3\2\2\2")
        buf.write("\u055c\u055d\3\2\2\2\u055d\u00db\3\2\2\2\u055e\u055c\3")
        buf.write("\2\2\2\u055f\u0560\7#\2\2\u0560\u0561\7\62\2\2\u0561\u0562")
        buf.write("\7\u008f\2\2\u0562\u0563\5,\27\2\u0563\u0564\7\u0090\2")
        buf.write("\2\u0564\u00dd\3\2\2\2\u0565\u0568\5\u0126\u0094\2\u0566")
        buf.write("\u0568\7\u0080\2\2\u0567\u0565\3\2\2\2\u0567\u0566\3\2")
        buf.write("\2\2\u0568\u00df\3\2\2\2\u0569\u056e\5\u00dep\2\u056a")
        buf.write("\u056b\7\u008d\2\2\u056b\u056d\5\u00dep\2\u056c\u056a")
        buf.write("\3\2\2\2\u056d\u0570\3\2\2\2\u056e\u056c\3\2\2\2\u056e")
        buf.write("\u056f\3\2\2\2\u056f\u00e1\3\2\2\2\u0570\u056e\3\2\2\2")
        buf.write("\u0571\u0572\7$\2\2\u0572\u0573\5\u0112\u008a\2\u0573")
        buf.write("\u0574\5\u0126\u0094\2\u0574\u0575\7\u008f\2\2\u0575\u0576")
        buf.write("\5\u00e0q\2\u0576\u0577\7\u0090\2\2\u0577\u0578\7\u008c")
        buf.write("\2\2\u0578\u00e3\3\2\2\2\u0579\u057a\7$\2\2\u057a\u057b")
        buf.write("\5\u00e8u\2\u057b\u057c\7+\2\2\u057c\u057d\7\u008f\2\2")
        buf.write("\u057d\u057e\5\u00a6T\2\u057e\u057f\7\u0090\2\2\u057f")
        buf.write("\u0580\7\u008c\2\2\u0580\u00e5\3\2\2\2\u0581\u0582\5\u01a6")
        buf.write("\u00d4\2\u0582\u0583\7\u0093\2\2\u0583\u0584\5\u0126\u0094")
        buf.write("\2\u0584\u00e7\3\2\2\2\u0585\u0586\t\6\2\2\u0586\u00e9")
        buf.write("\3\2\2\2\u0587\u058c\5\u00e8u\2\u0588\u0589\7\u008d\2")
        buf.write("\2\u0589\u058b\5\u00e8u\2\u058a\u0588\3\2\2\2\u058b\u058e")
        buf.write("\3\2\2\2\u058c\u058a\3\2\2\2\u058c\u058d\3\2\2\2\u058d")
        buf.write("\u00eb\3\2\2\2\u058e\u058c\3\2\2\2\u058f\u0591\5\u0112")
        buf.write("\u008a\2\u0590\u058f\3\2\2\2\u0590\u0591\3\2\2\2\u0591")
        buf.write("\u0592\3\2\2\2\u0592\u0593\7&\2\2\u0593\u0594\5l\67\2")
        buf.write("\u0594\u0595\7a\2\2\u0595\u059d\5\u0198\u00cd\2\u0596")
        buf.write("\u0597\7\35\2\2\u0597\u0598\5l\67\2\u0598\u0599\7a\2\2")
        buf.write("\u0599\u059a\5\u0198\u00cd\2\u059a\u059c\3\2\2\2\u059b")
        buf.write("\u0596\3\2\2\2\u059c\u059f\3\2\2\2\u059d\u059b\3\2\2\2")
        buf.write("\u059d\u059e\3\2\2\2\u059e\u05a2\3\2\2\2\u059f\u059d\3")
        buf.write("\2\2\2\u05a0\u05a1\7\34\2\2\u05a1\u05a3\5\u0198\u00cd")
        buf.write("\2\u05a2\u05a0\3\2\2\2\u05a2\u05a3\3\2\2\2\u05a3\u05a4")
        buf.write("\3\2\2\2\u05a4\u05a5\7\32\2\2\u05a5\u05a7\7&\2\2\u05a6")
        buf.write("\u05a8\5\u00e8u\2\u05a7\u05a6\3\2\2\2\u05a7\u05a8\3\2")
        buf.write("\2\2\u05a8\u05a9\3\2\2\2\u05a9\u05aa\7\u008c\2\2\u05aa")
        buf.write("\u00ed\3\2\2\2\u05ab\u05ac\7\u008f\2\2\u05ac\u05b1\5\u0096")
        buf.write("L\2\u05ad\u05ae\7\u008d\2\2\u05ae\u05b0\5\u0096L\2\u05af")
        buf.write("\u05ad\3\2\2\2\u05b0\u05b3\3\2\2\2\u05b1\u05af\3\2\2\2")
        buf.write("\u05b1\u05b2\3\2\2\2\u05b2\u05b4\3\2\2\2\u05b3\u05b1\3")
        buf.write("\2\2\2\u05b4\u05b5\7\u0090\2\2\u05b5\u00ef\3\2\2\2\u05b6")
        buf.write("\u05b9\5\u0096L\2\u05b7\u05b9\5\u00c2b\2\u05b8\u05b6\3")
        buf.write("\2\2\2\u05b8\u05b7\3\2\2\2\u05b9\u00f1\3\2\2\2\u05ba\u05bb")
        buf.write("\5\u0126\u0094\2\u05bb\u05bc\7J\2\2\u05bc\u05bd\7\u008a")
        buf.write("\2\2\u05bd\u00f3\3\2\2\2\u05be\u05c0\7\25\2\2\u05bf\u05be")
        buf.write("\3\2\2\2\u05bf\u05c0\3\2\2\2\u05c0\u05c1\3\2\2\2\u05c1")
        buf.write("\u05cd\5\u0126\u0094\2\u05c2\u05c3\7\33\2\2\u05c3\u05c8")
        buf.write("\5\u0126\u0094\2\u05c4\u05c5\7\u008f\2\2\u05c5\u05c6\5")
        buf.write("\u00e8u\2\u05c6\u05c7\7\u0090\2\2\u05c7\u05c9\3\2\2\2")
        buf.write("\u05c8\u05c4\3\2\2\2\u05c8\u05c9\3\2\2\2\u05c9\u05cd\3")
        buf.write("\2\2\2\u05ca\u05cb\7\26\2\2\u05cb\u05cd\5\u0126\u0094")
        buf.write("\2\u05cc\u05bf\3\2\2\2\u05cc\u05c2\3\2\2\2\u05cc\u05ca")
        buf.write("\3\2\2\2\u05cd\u00f5\3\2\2\2\u05ce\u05d3\5\u00e8u\2\u05cf")
        buf.write("\u05d0\7\u008d\2\2\u05d0\u05d2\5\u00e8u\2\u05d1\u05cf")
        buf.write("\3\2\2\2\u05d2\u05d5\3\2\2\2\u05d3\u05d1\3\2\2\2\u05d3")
        buf.write("\u05d4\3\2\2\2\u05d4\u05d9\3\2\2\2\u05d5\u05d3\3\2\2\2")
        buf.write("\u05d6\u05d9\7@\2\2\u05d7\u05d9\7\b\2\2\u05d8\u05ce\3")
        buf.write("\2\2\2\u05d8\u05d6\3\2\2\2\u05d8\u05d7\3\2\2\2\u05d9\u00f7")
        buf.write("\3\2\2\2\u05da\u05dc\7\27\2\2\u05db\u05da\3\2\2\2\u05db")
        buf.write("\u05dc\3\2\2\2\u05dc\u05dd\3\2\2\2\u05dd\u05de\5\u00ea")
        buf.write("v\2\u05de\u05e0\7\u0093\2\2\u05df\u05e1\7(\2\2\u05e0\u05df")
        buf.write("\3\2\2\2\u05e0\u05e1\3\2\2\2\u05e1\u05e2\3\2\2\2\u05e2")
        buf.write("\u05e5\5\u01d8\u00ed\2\u05e3\u05e4\7\u0089\2\2\u05e4\u05e6")
        buf.write("\5\u00c2b\2\u05e5\u05e3\3\2\2\2\u05e5\u05e6\3\2\2\2\u05e6")
        buf.write("\u00f9\3\2\2\2\u05e7\u05ee\5\u00f8}\2\u05e8\u05ee\5\u010a")
        buf.write("\u0086\2\u05e9\u05ee\5\u010e\u0088\2\u05ea\u05ee\5\u00fe")
        buf.write("\u0080\2\u05eb\u05ee\5\u010c\u0087\2\u05ec\u05ee\5\u0106")
        buf.write("\u0084\2\u05ed\u05e7\3\2\2\2\u05ed\u05e8\3\2\2\2\u05ed")
        buf.write("\u05e9\3\2\2\2\u05ed\u05ea\3\2\2\2\u05ed\u05eb\3\2\2\2")
        buf.write("\u05ed\u05ec\3\2\2\2\u05ee\u00fb\3\2\2\2\u05ef\u05f0\5")
        buf.write("\u00fa~\2\u05f0\u00fd\3\2\2\2\u05f1\u05f2\7\37\2\2\u05f2")
        buf.write("\u05f3\5\u00eav\2\u05f3\u05f4\7\u0093\2\2\u05f4\u05f5")
        buf.write("\5\u01d8\u00ed\2\u05f5\u00ff\3\2\2\2\u05f6\u05fb\5\u010a")
        buf.write("\u0086\2\u05f7\u05f8\7\u008c\2\2\u05f8\u05fa\5\u010a\u0086")
        buf.write("\2\u05f9\u05f7\3\2\2\2\u05fa\u05fd\3\2\2\2\u05fb\u05f9")
        buf.write("\3\2\2\2\u05fb\u05fc\3\2\2\2\u05fc\u0101\3\2\2\2\u05fd")
        buf.write("\u05fb\3\2\2\2\u05fe\u0603\5\u0108\u0085\2\u05ff\u0600")
        buf.write("\7\u008c\2\2\u0600\u0602\5\u0108\u0085\2\u0601\u05ff\3")
        buf.write("\2\2\2\u0602\u0605\3\2\2\2\u0603\u0601\3\2\2\2\u0603\u0604")
        buf.write("\3\2\2\2\u0604\u0103\3\2\2\2\u0605\u0603\3\2\2\2\u0606")
        buf.write("\u060b\5\u00fc\177\2\u0607\u0608\7\u008c\2\2\u0608\u060a")
        buf.write("\5\u00fc\177\2\u0609\u0607\3\2\2\2\u060a\u060d\3\2\2\2")
        buf.write("\u060b\u0609\3\2\2\2\u060b\u060c\3\2\2\2\u060c\u0105\3")
        buf.write("\2\2\2\u060d\u060b\3\2\2\2\u060e\u060f\7I\2\2\u060f\u0610")
        buf.write("\5\u00eav\2\u0610\u0612\7\u0093\2\2\u0611\u0613\t\7\2")
        buf.write("\2\u0612\u0611\3\2\2\2\u0612\u0613\3\2\2\2\u0613\u0614")
        buf.write("\3\2\2\2\u0614\u0617\5\u01d8\u00ed\2\u0615\u0616\7\u0089")
        buf.write("\2\2\u0616\u0618\5\u00c2b\2\u0617\u0615\3\2\2\2\u0617")
        buf.write("\u0618\3\2\2\2\u0618\u0107\3\2\2\2\u0619\u061a\5\u00ea")
        buf.write("v\2\u061a\u061b\7\u0093\2\2\u061b\u061c\5\u0122\u0092")
        buf.write("\2\u061c\u061e\5\u01d8\u00ed\2\u061d\u061f\7\23\2\2\u061e")
        buf.write("\u061d\3\2\2\2\u061e\u061f\3\2\2\2\u061f\u0622\3\2\2\2")
        buf.write("\u0620\u0621\7\u0089\2\2\u0621\u0623\5\u00c2b\2\u0622")
        buf.write("\u0620\3\2\2\2\u0622\u0623\3\2\2\2\u0623\u0109\3\2\2\2")
        buf.write("\u0624\u0625\7X\2\2\u0625\u0626\5\u00eav\2\u0626\u0627")
        buf.write("\7\u0093\2\2\u0627\u0629\5\u01d8\u00ed\2\u0628\u062a\7")
        buf.write("\23\2\2\u0629\u0628\3\2\2\2\u0629\u062a\3\2\2\2\u062a")
        buf.write("\u062d\3\2\2\2\u062b\u062c\7\u0089\2\2\u062c\u062e\5\u00c2")
        buf.write("b\2\u062d\u062b\3\2\2\2\u062d\u062e\3\2\2\2\u062e\u010b")
        buf.write("\3\2\2\2\u062f\u0630\7`\2\2\u0630\u0631\5\u00eav\2\u0631")
        buf.write("\u0632\7\u0093\2\2\u0632\u0633\5\u01c2\u00e2\2\u0633\u010d")
        buf.write("\3\2\2\2\u0634\u0636\7k\2\2\u0635\u0634\3\2\2\2\u0635")
        buf.write("\u0636\3\2\2\2\u0636\u0637\3\2\2\2\u0637\u0638\5\u00ea")
        buf.write("v\2\u0638\u063a\7\u0093\2\2\u0639\u063b\5\u0122\u0092")
        buf.write("\2\u063a\u0639\3\2\2\2\u063a\u063b\3\2\2\2\u063b\u063c")
        buf.write("\3\2\2\2\u063c\u063f\5\u01d8\u00ed\2\u063d\u063e\7\u0089")
        buf.write("\2\2\u063e\u0640\5\u00c2b\2\u063f\u063d\3\2\2\2\u063f")
        buf.write("\u0640\3\2\2\2\u0640\u010f\3\2\2\2\u0641\u0642\7o\2\2")
        buf.write("\u0642\u0646\5l\67\2\u0643\u0644\7 \2\2\u0644\u0646\5")
        buf.write("\u014c\u00a7\2\u0645\u0641\3\2\2\2\u0645\u0643\3\2\2\2")
        buf.write("\u0646\u0111\3\2\2\2\u0647\u0648\5\u00e8u\2\u0648\u0649")
        buf.write("\7\u0093\2\2\u0649\u0113\3\2\2\2\u064a\u064b\7-\2\2\u064b")
        buf.write("\u064c\5\u011c\u008f\2\u064c\u064d\7\u008c\2\2\u064d\u0115")
        buf.write("\3\2\2\2\u064e\u0651\5\u018c\u00c7\2\u064f\u0651\5\u015a")
        buf.write("\u00ae\2\u0650\u064e\3\2\2\2\u0650\u064f\3\2\2\2\u0651")
        buf.write("\u0117\3\2\2\2\u0652\u0658\7;\2\2\u0653\u0658\7s\2\2\u0654")
        buf.write("\u0658\7\u0081\2\2\u0655\u0658\5\u00bc_\2\u0656\u0658")
        buf.write("\5\u013a\u009e\2\u0657\u0652\3\2\2\2\u0657\u0653\3\2\2")
        buf.write("\2\u0657\u0654\3\2\2\2\u0657\u0655\3\2\2\2\u0657\u0656")
        buf.write("\3\2\2\2\u0658\u0119\3\2\2\2\u0659\u065a\5\u00e8u\2\u065a")
        buf.write("\u011b\3\2\2\2\u065b\u0660\5\u011a\u008e\2\u065c\u065d")
        buf.write("\7\u008d\2\2\u065d\u065f\5\u011a\u008e\2\u065e\u065c\3")
        buf.write("\2\2\2\u065f\u0662\3\2\2\2\u0660\u065e\3\2\2\2\u0660\u0661")
        buf.write("\3\2\2\2\u0661\u011d\3\2\2\2\u0662\u0660\3\2\2\2\u0663")
        buf.write("\u0664\t\b\2\2\u0664\u011f\3\2\2\2\u0665\u0667\5\u0112")
        buf.write("\u008a\2\u0666\u0665\3\2\2\2\u0666\u0667\3\2\2\2\u0667")
        buf.write("\u0669\3\2\2\2\u0668\u066a\5\u0110\u0089\2\u0669\u0668")
        buf.write("\3\2\2\2\u0669\u066a\3\2\2\2\u066a\u066b\3\2\2\2\u066b")
        buf.write("\u066c\7\61\2\2\u066c\u066d\5\u0198\u00cd\2\u066d\u066e")
        buf.write("\7\32\2\2\u066e\u0670\7\61\2\2\u066f\u0671\5\u00e8u\2")
        buf.write("\u0670\u066f\3\2\2\2\u0670\u0671\3\2\2\2\u0671\u0672\3")
        buf.write("\2\2\2\u0672\u0673\7\u008c\2\2\u0673\u0121\3\2\2\2\u0674")
        buf.write("\u0675\t\t\2\2\u0675\u0123\3\2\2\2\u0676\u0677\t\n\2\2")
        buf.write("\u0677\u0125\3\2\2\2\u0678\u0682\5\u0130\u0099\2\u0679")
        buf.write("\u067e\5\u0128\u0095\2\u067a\u067b\7\u009c\2\2\u067b\u067d")
        buf.write("\5\u0128\u0095\2\u067c\u067a\3\2\2\2\u067d\u0680\3\2\2")
        buf.write("\2\u067e\u067c\3\2\2\2\u067e\u067f\3\2\2\2\u067f\u0682")
        buf.write("\3\2\2\2\u0680\u067e\3\2\2\2\u0681\u0678\3\2\2\2\u0681")
        buf.write("\u0679\3\2\2\2\u0682\u0127\3\2\2\2\u0683\u0687\5\u0130")
        buf.write("\u0099\2\u0684\u0688\5\u012a\u0096\2\u0685\u0688\5\u012c")
        buf.write("\u0097\2\u0686\u0688\5\u012e\u0098\2\u0687\u0684\3\2\2")
        buf.write("\2\u0687\u0685\3\2\2\2\u0687\u0686\3\2\2\2\u0687\u0688")
        buf.write("\3\2\2\2\u0688\u0129\3\2\2\2\u0689\u068a\7\u00a4\2\2\u068a")
        buf.write("\u0693\5\60\31\2\u068b\u0690\5\u00c2b\2\u068c\u068d\7")
        buf.write("\u008d\2\2\u068d\u068f\5\u00c2b\2\u068e\u068c\3\2\2\2")
        buf.write("\u068f\u0692\3\2\2\2\u0690\u068e\3\2\2\2\u0690\u0691\3")
        buf.write("\2\2\2\u0691\u0694\3\2\2\2\u0692\u0690\3\2\2\2\u0693\u068b")
        buf.write("\3\2\2\2\u0693\u0694\3\2\2\2\u0694\u012b\3\2\2\2\u0695")
        buf.write("\u0697\7\u008f\2\2\u0696\u0698\5\n\6\2\u0697\u0696\3\2")
        buf.write("\2\2\u0697\u0698\3\2\2\2\u0698\u0699\3\2\2\2\u0699\u069a")
        buf.write("\7\u0090\2\2\u069a\u012d\3\2\2\2\u069b\u069c\7\u008f\2")
        buf.write("\2\u069c\u06a1\5\u0178\u00bd\2\u069d\u069e\7\u008d\2\2")
        buf.write("\u069e\u06a0\5\u0178\u00bd\2\u069f\u069d\3\2\2\2\u06a0")
        buf.write("\u06a3\3\2\2\2\u06a1\u069f\3\2\2\2\u06a1\u06a2\3\2\2\2")
        buf.write("\u06a2\u06a4\3\2\2\2\u06a3\u06a1\3\2\2\2\u06a4\u06a5\7")
        buf.write("\u0090\2\2\u06a5\u012f\3\2\2\2\u06a6\u06ab\5\u00e8u\2")
        buf.write("\u06a7\u06a8\7\u009c\2\2\u06a8\u06aa\5\u01da\u00ee\2\u06a9")
        buf.write("\u06a7\3\2\2\2\u06aa\u06ad\3\2\2\2\u06ab\u06a9\3\2\2\2")
        buf.write("\u06ab\u06ac\3\2\2\2\u06ac\u0131\3\2\2\2\u06ad\u06ab\3")
        buf.write("\2\2\2\u06ae\u06af\7\65\2\2\u06af\u06b0\5\u00e8u\2\u06b0")
        buf.write("\u06b1\7+\2\2\u06b1\u06b2\5\u0134\u009b\2\u06b2\u06b3")
        buf.write("\7\u008c\2\2\u06b3\u0133\3\2\2\2\u06b4\u06b7\5\u0188\u00c5")
        buf.write("\2\u06b5\u06b7\5`\61\2\u06b6\u06b4\3\2\2\2\u06b6\u06b5")
        buf.write("\3\2\2\2\u06b7\u0135\3\2\2\2\u06b8\u06b9\5\u00eav\2\u06b9")
        buf.write("\u06ba\7\u0093\2\2\u06ba\u06bb\5\u009cO\2\u06bb\u0137")
        buf.write("\3\2\2\2\u06bc\u06be\5\u0112\u008a\2\u06bd\u06bc\3\2\2")
        buf.write("\2\u06bd\u06be\3\2\2\2\u06be\u06bf\3\2\2\2\u06bf\u06c1")
        buf.write("\7\67\2\2\u06c0\u06c2\5\u00e8u\2\u06c1\u06c0\3\2\2\2\u06c1")
        buf.write("\u06c2\3\2\2\2\u06c2\u06c5\3\2\2\2\u06c3\u06c4\7n\2\2")
        buf.write("\u06c4\u06c6\5l\67\2\u06c5\u06c3\3\2\2\2\u06c5\u06c6\3")
        buf.write("\2\2\2\u06c6\u06c7\3\2\2\2\u06c7\u06c8\7\u008c\2\2\u06c8")
        buf.write("\u0139\3\2\2\2\u06c9\u06cc\5\2\2\2\u06ca\u06cc\5\u014e")
        buf.write("\u00a8\2\u06cb\u06c9\3\2\2\2\u06cb\u06ca\3\2\2\2\u06cc")
        buf.write("\u013b\3\2\2\2\u06cd\u06d4\5~@\2\u06ce\u06d4\5\u01a2\u00d2")
        buf.write("\2\u06cf\u06d4\5\u01f6\u00fc\2\u06d0\u06d4\5\u00c6d\2")
        buf.write("\u06d1\u06d4\5\u01e2\u00f2\2\u06d2\u06d4\5\u0170\u00b9")
        buf.write("\2\u06d3\u06cd\3\2\2\2\u06d3\u06ce\3\2\2\2\u06d3\u06cf")
        buf.write("\3\2\2\2\u06d3\u06d0\3\2\2\2\u06d3\u06d1\3\2\2\2\u06d3")
        buf.write("\u06d2\3\2\2\2\u06d4\u013d\3\2\2\2\u06d5\u06d7\7%\2\2")
        buf.write("\u06d6\u06d5\3\2\2\2\u06d6\u06d7\3\2\2\2\u06d7\u06d9\3")
        buf.write("\2\2\2\u06d8\u06da\5\u008aF\2\u06d9\u06d8\3\2\2\2\u06d9")
        buf.write("\u06da\3\2\2\2\u06da\u013f\3\2\2\2\u06db\u06dc\7B\2\2")
        buf.write("\u06dc\u06dd\7\20\2\2\u06dd\u06de\5\u00e8u\2\u06de\u06df")
        buf.write("\7+\2\2\u06df\u06e0\5\u0144\u00a3\2\u06e0\u06e3\7\32\2")
        buf.write("\2\u06e1\u06e2\7B\2\2\u06e2\u06e4\7\20\2\2\u06e3\u06e1")
        buf.write("\3\2\2\2\u06e3\u06e4\3\2\2\2\u06e4\u06e6\3\2\2\2\u06e5")
        buf.write("\u06e7\5\u00e8u\2\u06e6\u06e5\3\2\2\2\u06e6\u06e7\3\2")
        buf.write("\2\2\u06e7\u06e8\3\2\2\2\u06e8\u06e9\7\u008c\2\2\u06e9")
        buf.write("\u0141\3\2\2\2\u06ea\u06f6\5\u01c6\u00e4\2\u06eb\u06f6")
        buf.write("\5\u01c4\u00e3\2\u06ec\u06f6\5\u01ea\u00f6\2\u06ed\u06f6")
        buf.write("\5\u01d6\u00ec\2\u06ee\u06f6\5~@\2\u06ef\u06f6\5\u01f6")
        buf.write("\u00fc\2\u06f0\u06f6\5\u00c6d\2\u06f1\u06f6\5\22\n\2\u06f2")
        buf.write("\u06f6\5\u01f2\u00fa\2\u06f3\u06f6\5\u00e4s\2\u06f4\u06f6")
        buf.write("\5\u00e2r\2\u06f5\u06ea\3\2\2\2\u06f5\u06eb\3\2\2\2\u06f5")
        buf.write("\u06ec\3\2\2\2\u06f5\u06ed\3\2\2\2\u06f5\u06ee\3\2\2\2")
        buf.write("\u06f5\u06ef\3\2\2\2\u06f5\u06f0\3\2\2\2\u06f5\u06f1\3")
        buf.write("\2\2\2\u06f5\u06f2\3\2\2\2\u06f5\u06f3\3\2\2\2\u06f5\u06f4")
        buf.write("\3\2\2\2\u06f6\u0143\3\2\2\2\u06f7\u06f9\5\u0142\u00a2")
        buf.write("\2\u06f8\u06f7\3\2\2\2\u06f9\u06fc\3\2\2\2\u06fa\u06f8")
        buf.write("\3\2\2\2\u06fa\u06fb\3\2\2\2\u06fb\u0145\3\2\2\2\u06fc")
        buf.write("\u06fa\3\2\2\2\u06fd\u06fe\7B\2\2\u06fe\u06ff\5\u00e8")
        buf.write("u\2\u06ff\u0700\7+\2\2\u0700\u0701\5\u014a\u00a6\2\u0701")
        buf.write("\u0703\7\32\2\2\u0702\u0704\7B\2\2\u0703\u0702\3\2\2\2")
        buf.write("\u0703\u0704\3\2\2\2\u0704\u0706\3\2\2\2\u0705\u0707\5")
        buf.write("\u00e8u\2\u0706\u0705\3\2\2\2\u0706\u0707\3\2\2\2\u0707")
        buf.write("\u0708\3\2\2\2\u0708\u0709\7\u008c\2\2\u0709\u0147\3\2")
        buf.write("\2\2\u070a\u071d\5\u01c6\u00e4\2\u070b\u071d\5\u01ea\u00f6")
        buf.write("\2\u070c\u071d\5\u01d6\u00ec\2\u070d\u071d\5~@\2\u070e")
        buf.write("\u071d\5\u01a2\u00d2\2\u070f\u071d\5\u01f6\u00fc\2\u0710")
        buf.write("\u071d\5\u00c6d\2\u0711\u071d\5\22\n\2\u0712\u071d\5Z")
        buf.write(".\2\u0713\u071d\5.\30\2\u0714\u071d\5\62\32\2\u0715\u071d")
        buf.write("\5\u0094K\2\u0716\u071d\5\u01f2\u00fa\2\u0717\u071d\5")
        buf.write("\u00e4s\2\u0718\u071d\5\u00e2r\2\u0719\u071d\5\u0132\u009a")
        buf.write("\2\u071a\u071d\5\u01c0\u00e1\2\u071b\u071d\5\u01e2\u00f2")
        buf.write("\2\u071c\u070a\3\2\2\2\u071c\u070b\3\2\2\2\u071c\u070c")
        buf.write("\3\2\2\2\u071c\u070d\3\2\2\2\u071c\u070e\3\2\2\2\u071c")
        buf.write("\u070f\3\2\2\2\u071c\u0710\3\2\2\2\u071c\u0711\3\2\2\2")
        buf.write("\u071c\u0712\3\2\2\2\u071c\u0713\3\2\2\2\u071c\u0714\3")
        buf.write("\2\2\2\u071c\u0715\3\2\2\2\u071c\u0716\3\2\2\2\u071c\u0717")
        buf.write("\3\2\2\2\u071c\u0718\3\2\2\2\u071c\u0719\3\2\2\2\u071c")
        buf.write("\u071a\3\2\2\2\u071c\u071b\3\2\2\2\u071d\u0149\3\2\2\2")
        buf.write("\u071e\u0720\5\u0148\u00a5\2\u071f\u071e\3\2\2\2\u0720")
        buf.write("\u0723\3\2\2\2\u0721\u071f\3\2\2\2\u0721\u0722\3\2\2\2")
        buf.write("\u0722\u014b\3\2\2\2\u0723\u0721\3\2\2\2\u0724\u0725\5")
        buf.write("\u00e8u\2\u0725\u0726\7(\2\2\u0726\u0727\5\u0096L\2\u0727")
        buf.write("\u014d\3\2\2\2\u0728\u0729\5\2\2\2\u0729\u072a\5\u00e8")
        buf.write("u\2\u072a\u014f\3\2\2\2\u072b\u072c\5\u017a\u00be\2\u072c")
        buf.write("\u072d\7h\2\2\u072d\u0731\5\64\33\2\u072e\u0730\5\u018e")
        buf.write("\u00c8\2\u072f\u072e\3\2\2\2\u0730\u0733\3\2\2\2\u0731")
        buf.write("\u072f\3\2\2\2\u0731\u0732\3\2\2\2\u0732\u0734\3\2\2\2")
        buf.write("\u0733\u0731\3\2\2\2\u0734\u0735\7\32\2\2\u0735\u0737")
        buf.write("\7h\2\2\u0736\u0738\5\u00e8u\2\u0737\u0736\3\2\2\2\u0737")
        buf.write("\u0738\3\2\2\2\u0738\u0151\3\2\2\2\u0739\u073a\7C\2\2")
        buf.write("\u073a\u073b\7\u008f\2\2\u073b\u073c\5\u0154\u00ab\2\u073c")
        buf.write("\u073d\7\u0090\2\2\u073d\u073e\7\u008c\2\2\u073e\u0153")
        buf.write("\3\2\2\2\u073f\u0740\5\u0102\u0082\2\u0740\u0155\3\2\2")
        buf.write("\2\u0741\u0742\7C\2\2\u0742\u0743\7\62\2\2\u0743\u0744")
        buf.write("\7\u008f\2\2\u0744\u0745\5,\27\2\u0745\u0746\7\u0090\2")
        buf.write("\2\u0746\u0157\3\2\2\2\u0747\u0751\5\u0118\u008d\2\u0748")
        buf.write("\u0751\5\u016e\u00b8\2\u0749\u074a\7\u008f\2\2\u074a\u074b")
        buf.write("\5\u00c2b\2\u074b\u074c\7\u0090\2\2\u074c\u0751\3\2\2")
        buf.write("\2\u074d\u0751\5\30\r\2\u074e\u0751\5\20\t\2\u074f\u0751")
        buf.write("\5\u0126\u0094\2\u0750\u0747\3\2\2\2\u0750\u0748\3\2\2")
        buf.write("\2\u0750\u0749\3\2\2\2\u0750\u074d\3\2\2\2\u0750\u074e")
        buf.write("\3\2\2\2\u0750\u074f\3\2\2\2\u0751\u0159\3\2\2\2\u0752")
        buf.write("\u0756\5\u00a8U\2\u0753\u0756\5t;\2\u0754\u0756\5\u0146")
        buf.write("\u00a4\2\u0755\u0752\3\2\2\2\u0755\u0753\3\2\2\2\u0755")
        buf.write("\u0754\3\2\2\2\u0756\u015b\3\2\2\2\u0757\u0764\5\u01c6")
        buf.write("\u00e4\2\u0758\u0764\5\u01c4\u00e3\2\u0759\u0764\5\u01ea")
        buf.write("\u00f6\2\u075a\u0764\5\u01d6\u00ec\2\u075b\u0764\5~@\2")
        buf.write("\u075c\u0764\5\u01f6\u00fc\2\u075d\u0764\5\22\n\2\u075e")
        buf.write("\u0764\5.\30\2\u075f\u0764\5\62\32\2\u0760\u0764\5\u01f2")
        buf.write("\u00fa\2\u0761\u0764\5\u00e4s\2\u0762\u0764\5\u00e2r\2")
        buf.write("\u0763\u0757\3\2\2\2\u0763\u0758\3\2\2\2\u0763\u0759\3")
        buf.write("\2\2\2\u0763\u075a\3\2\2\2\u0763\u075b\3\2\2\2\u0763\u075c")
        buf.write("\3\2\2\2\u0763\u075d\3\2\2\2\u0763\u075e\3\2\2\2\u0763")
        buf.write("\u075f\3\2\2\2\u0763\u0760\3\2\2\2\u0763\u0761\3\2\2\2")
        buf.write("\u0763\u0762\3\2\2\2\u0764\u015d\3\2\2\2\u0765\u0767\5")
        buf.write("\u015c\u00af\2\u0766\u0765\3\2\2\2\u0767\u076a\3\2\2\2")
        buf.write("\u0768\u0766\3\2\2\2\u0768\u0769\3\2\2\2\u0769\u015f\3")
        buf.write("\2\2\2\u076a\u0768\3\2\2\2\u076b\u076d\5\u019a\u00ce\2")
        buf.write("\u076c\u076b\3\2\2\2\u076d\u0770\3\2\2\2\u076e\u076c\3")
        buf.write("\2\2\2\u076e\u076f\3\2\2\2\u076f\u0161\3\2\2\2\u0770\u076e")
        buf.write("\3\2\2\2\u0771\u0776\5\u0130\u0099\2\u0772\u0773\7\u008f")
        buf.write("\2\2\u0773\u0774\5\n\6\2\u0774\u0775\7\u0090\2\2\u0775")
        buf.write("\u0777\3\2\2\2\u0776\u0772\3\2\2\2\u0776\u0777\3\2\2\2")
        buf.write("\u0777\u0163\3\2\2\2\u0778\u077a\5\u0112\u008a\2\u0779")
        buf.write("\u0778\3\2\2\2\u0779\u077a\3\2\2\2\u077a\u077b\3\2\2\2")
        buf.write("\u077b\u077c\5\u0162\u00b2\2\u077c\u077d\7\u008c\2\2\u077d")
        buf.write("\u0165\3\2\2\2\u077e\u078c\5\u01c6\u00e4\2\u077f\u078c")
        buf.write("\5\u01c4\u00e3\2\u0780\u078c\5\u01ea\u00f6\2\u0781\u078c")
        buf.write("\5\u01d6\u00ec\2\u0782\u078c\5~@\2\u0783\u078c\5\u01f6")
        buf.write("\u00fc\2\u0784\u078c\5\u00c6d\2\u0785\u078c\5\22\n\2\u0786")
        buf.write("\u078c\5.\30\2\u0787\u078c\5\62\32\2\u0788\u078c\5\u01f2")
        buf.write("\u00fa\2\u0789\u078c\5\u00e4s\2\u078a\u078c\5\u00e2r\2")
        buf.write("\u078b\u077e\3\2\2\2\u078b\u077f\3\2\2\2\u078b\u0780\3")
        buf.write("\2\2\2\u078b\u0781\3\2\2\2\u078b\u0782\3\2\2\2\u078b\u0783")
        buf.write("\3\2\2\2\u078b\u0784\3\2\2\2\u078b\u0785\3\2\2\2\u078b")
        buf.write("\u0786\3\2\2\2\u078b\u0787\3\2\2\2\u078b\u0788\3\2\2\2")
        buf.write("\u078b\u0789\3\2\2\2\u078b\u078a\3\2\2\2\u078c\u0167\3")
        buf.write("\2\2\2\u078d\u078f\5\u0166\u00b4\2\u078e\u078d\3\2\2\2")
        buf.write("\u078f\u0792\3\2\2\2\u0790\u078e\3\2\2\2\u0790\u0791\3")
        buf.write("\2\2\2\u0791\u0169\3\2\2\2\u0792\u0790\3\2\2\2\u0793\u0795")
        buf.write("\5\u0112\u008a\2\u0794\u0793\3\2\2\2\u0794\u0795\3\2\2")
        buf.write("\2\u0795\u0797\3\2\2\2\u0796\u0798\7D\2\2\u0797\u0796")
        buf.write("\3\2\2\2\u0797\u0798\3\2\2\2\u0798\u0799\3\2\2\2\u0799")
        buf.write("\u079e\7E\2\2\u079a\u079b\7\u008f\2\2\u079b\u079c\5\u0196")
        buf.write("\u00cc\2\u079c\u079d\7\u0090\2\2\u079d\u079f\3\2\2\2\u079e")
        buf.write("\u079a\3\2\2\2\u079e\u079f\3\2\2\2\u079f\u07a1\3\2\2\2")
        buf.write("\u07a0\u07a2\7+\2\2\u07a1\u07a0\3\2\2\2\u07a1\u07a2\3")
        buf.write("\2\2\2\u07a2\u07a3\3\2\2\2\u07a3\u07a4\5\u0168\u00b5\2")
        buf.write("\u07a4\u07a5\7\16\2\2\u07a5\u07a6\5\u016c\u00b7\2\u07a6")
        buf.write("\u07a8\7\32\2\2\u07a7\u07a9\7D\2\2\u07a8\u07a7\3\2\2\2")
        buf.write("\u07a8\u07a9\3\2\2\2\u07a9\u07aa\3\2\2\2\u07aa\u07ac\7")
        buf.write("E\2\2\u07ab\u07ad\5\u00e8u\2\u07ac\u07ab\3\2\2\2\u07ac")
        buf.write("\u07ad\3\2\2\2\u07ad\u07ae\3\2\2\2\u07ae\u07af\7\u008c")
        buf.write("\2\2\u07af\u016b\3\2\2\2\u07b0\u07b2\5\u019a\u00ce\2\u07b1")
        buf.write("\u07b0\3\2\2\2\u07b2\u07b5\3\2\2\2\u07b3\u07b1\3\2\2\2")
        buf.write("\u07b3\u07b4\3\2\2\2\u07b4\u016d\3\2\2\2\u07b5\u07b3\3")
        buf.write("\2\2\2\u07b6\u07b7\5\u01d8\u00ed\2\u07b7\u07bd\7\u00a4")
        buf.write("\2\2\u07b8\u07be\5\20\t\2\u07b9\u07ba\7\u008f\2\2\u07ba")
        buf.write("\u07bb\5\u00c2b\2\u07bb\u07bc\7\u0090\2\2\u07bc\u07be")
        buf.write("\3\2\2\2\u07bd\u07b8\3\2\2\2\u07bd\u07b9\3\2\2\2\u07be")
        buf.write("\u016f\3\2\2\2\u07bf\u07c3\5\u00d2j\2\u07c0\u07c3\5F$")
        buf.write("\2\u07c1\u07c3\5\u01bc\u00df\2\u07c2\u07bf\3\2\2\2\u07c2")
        buf.write("\u07c0\3\2\2\2\u07c2\u07c1\3\2\2\2\u07c3\u0171\3\2\2\2")
        buf.write("\u07c4\u07c9\5\u0126\u0094\2\u07c5\u07c6\7\u008d\2\2\u07c6")
        buf.write("\u07c8\5\u0126\u0094\2\u07c7\u07c5\3\2\2\2\u07c8\u07cb")
        buf.write("\3\2\2\2\u07c9\u07c7\3\2\2\2\u07c9\u07ca\3\2\2\2\u07ca")
        buf.write("\u07cf\3\2\2\2\u07cb\u07c9\3\2\2\2\u07cc\u07cf\7@\2\2")
        buf.write("\u07cd\u07cf\7\b\2\2\u07ce\u07c4\3\2\2\2\u07ce\u07cc\3")
        buf.write("\2\2\2\u07ce\u07cd\3\2\2\2\u07cf\u0173\3\2\2\2\u07d0\u07d1")
        buf.write("\5\u0172\u00ba\2\u07d1\u07d2\7\u0093\2\2\u07d2\u07d3\5")
        buf.write("\u0126\u0094\2\u07d3\u0175\3\2\2\2\u07d4\u07d7\5\u0178")
        buf.write("\u00bd\2\u07d5\u07d7\5\u0126\u0094\2\u07d6\u07d4\3\2\2")
        buf.write("\2\u07d6\u07d5\3\2\2\2\u07d7\u0177\3\2\2\2\u07d8\u07d9")
        buf.write("\5\u01aa\u00d6\2\u07d9\u07da\5\u0092J\2\u07da\u07db\5")
        buf.write("\u01aa\u00d6\2\u07db\u0179\3\2\2\2\u07dc\u07dd\7J\2\2")
        buf.write("\u07dd\u07de\5\u0176\u00bc\2\u07de\u017b\3\2\2\2\u07df")
        buf.write("\u07e1\7N\2\2\u07e0\u07e2\5\u0136\u009c\2\u07e1\u07e0")
        buf.write("\3\2\2\2\u07e2\u07e3\3\2\2\2\u07e3\u07e1\3\2\2\2\u07e3")
        buf.write("\u07e4\3\2\2\2\u07e4\u07e5\3\2\2\2\u07e5\u07e6\7\32\2")
        buf.write("\2\u07e6\u07e8\7N\2\2\u07e7\u07e9\5\u00e8u\2\u07e8\u07e7")
        buf.write("\3\2\2\2\u07e8\u07e9\3\2\2\2\u07e9\u017d\3\2\2\2\u07ea")
        buf.write("\u07ec\7N\2\2\u07eb\u07ed\5\u009aN\2\u07ec\u07eb\3\2\2")
        buf.write("\2\u07ed\u07ee\3\2\2\2\u07ee\u07ec\3\2\2\2\u07ee\u07ef")
        buf.write("\3\2\2\2\u07ef\u07f0\3\2\2\2\u07f0\u07f1\7\32\2\2\u07f1")
        buf.write("\u07f3\7N\2\2\u07f2\u07f4\5\u00e8u\2\u07f3\u07f2\3\2\2")
        buf.write("\2\u07f3\u07f4\3\2\2\2\u07f4\u017f\3\2\2\2\u07f5\u07f9")
        buf.write("\5\u019c\u00cf\2\u07f6\u07f7\5\u0182\u00c2\2\u07f7\u07f8")
        buf.write("\5\u019c\u00cf\2\u07f8\u07fa\3\2\2\2\u07f9\u07f6\3\2\2")
        buf.write("\2\u07f9\u07fa\3\2\2\2\u07fa\u0181\3\2\2\2\u07fb\u07fc")
        buf.write("\t\13\2\2\u07fc\u0183\3\2\2\2\u07fd\u07ff\5\u0112\u008a")
        buf.write("\2\u07fe\u07fd\3\2\2\2\u07fe\u07ff\3\2\2\2\u07ff\u0800")
        buf.write("\3\2\2\2\u0800\u0801\7Q\2\2\u0801\u0804\5\u00c2b\2\u0802")
        buf.write("\u0803\7V\2\2\u0803\u0805\5\u00c2b\2\u0804\u0802\3\2\2")
        buf.write("\2\u0804\u0805\3\2\2\2\u0805\u0806\3\2\2\2\u0806\u0807")
        buf.write("\7\u008c\2\2\u0807\u0185\3\2\2\2\u0808\u080a\5\u0112\u008a")
        buf.write("\2\u0809\u0808\3\2\2\2\u0809\u080a\3\2\2\2\u080a\u080b")
        buf.write("\3\2\2\2\u080b\u080d\7R\2\2\u080c\u080e\5\u00c2b\2\u080d")
        buf.write("\u080c\3\2\2\2\u080d\u080e\3\2\2\2\u080e\u080f\3\2\2\2")
        buf.write("\u080f\u0810\7\u008c\2\2\u0810\u0187\3\2\2\2\u0811\u0812")
        buf.write("\5\u0126\u0094\2\u0812\u0813\7\5\2\2\u0813\u0814\5\u0126")
        buf.write("\u0094\2\u0814\u0815\7b\2\2\u0815\u0816\5\u0126\u0094")
        buf.write("\2\u0816\u0817\7O\2\2\u0817\u0189\3\2\2\2\u0818\u081c")
        buf.write("\5\u0150\u00a9\2\u0819\u081c\5\u00be`\2\u081a\u081c\5")
        buf.write("\u017a\u00be\2\u081b\u0818\3\2\2\2\u081b\u0819\3\2\2\2")
        buf.write("\u081b\u081a\3\2\2\2\u081c\u018b\3\2\2\2\u081d\u0820\5")
        buf.write("\32\16\2\u081e\u0820\5\u0140\u00a1\2\u081f\u081d\3\2\2")
        buf.write("\2\u081f\u081e\3\2\2\2\u0820\u018d\3\2\2\2\u0821\u0822")
        buf.write("\5\u00e8u\2\u0822\u0823\7\u009a\2\2\u0823\u0824\5\u014e")
        buf.write("\u00a8\2\u0824\u0825\7\u008c\2\2\u0825\u018f\3\2\2\2\u0826")
        buf.write("\u0827\7m\2\2\u0827\u0828\5\u00c2b\2\u0828\u0829\7U\2")
        buf.write("\2\u0829\u082a\5\u01dc\u00ef\2\u082a\u082b\7\u0085\2\2")
        buf.write("\u082b\u082c\5\u013e\u00a0\2\u082c\u082d\5\u0192\u00ca")
        buf.write("\2\u082d\u082e\7\u008c\2\2\u082e\u0191\3\2\2\2\u082f\u0830")
        buf.write("\5\u01fa\u00fe\2\u0830\u0831\7n\2\2\u0831\u0839\5V,\2")
        buf.write("\u0832\u0833\7\u008d\2\2\u0833\u0834\5\u01fa\u00fe\2\u0834")
        buf.write("\u0835\7n\2\2\u0835\u0836\5V,\2\u0836\u0838\3\2\2\2\u0837")
        buf.write("\u0832\3\2\2\2\u0838\u083b\3\2\2\2\u0839\u0837\3\2\2\2")
        buf.write("\u0839\u083a\3\2\2\2\u083a\u0193\3\2\2\2\u083b\u0839\3")
        buf.write("\2\2\2\u083c\u083d\7=\2\2\u083d\u083e\5\u0196\u00cc\2")
        buf.write("\u083e\u0195\3\2\2\2\u083f\u0844\5\u0126\u0094\2\u0840")
        buf.write("\u0841\7\u008d\2\2\u0841\u0843\5\u0126\u0094\2\u0842\u0840")
        buf.write("\3\2\2\2\u0843\u0846\3\2\2\2\u0844\u0842\3\2\2\2\u0844")
        buf.write("\u0845\3\2\2\2\u0845\u0197\3\2\2\2\u0846\u0844\3\2\2\2")
        buf.write("\u0847\u0849\5\u019a\u00ce\2\u0848\u0847\3\2\2\2\u0849")
        buf.write("\u084c\3\2\2\2\u084a\u0848\3\2\2\2\u084a\u084b\3\2\2\2")
        buf.write("\u084b\u0199\3\2\2\2\u084c\u084a\3\2\2\2\u084d\u0860\5")
        buf.write("\u01f8\u00fd\2\u084e\u0860\5(\25\2\u084f\u0860\5\u0184")
        buf.write("\u00c3\2\u0850\u0860\5\u01a0\u00d1\2\u0851\u0860\5\u01f4")
        buf.write("\u00fb\2\u0852\u0860\5\u00ecw\2\u0853\u0860\5P)\2\u0854")
        buf.write("\u0860\5\u0120\u0091\2\u0855\u0860\5\u0138\u009d\2\u0856")
        buf.write("\u0860\5\u00c0a\2\u0857\u0860\5\u0186\u00c4\2\u0858\u085a")
        buf.write("\5\u0112\u008a\2\u0859\u0858\3\2\2\2\u0859\u085a\3\2\2")
        buf.write("\2\u085a\u085b\3\2\2\2\u085b\u085c\7;\2\2\u085c\u0860")
        buf.write("\7\u008c\2\2\u085d\u0860\5N(\2\u085e\u0860\5\u0164\u00b3")
        buf.write("\2\u085f\u084d\3\2\2\2\u085f\u084e\3\2\2\2\u085f\u084f")
        buf.write("\3\2\2\2\u085f\u0850\3\2\2\2\u085f\u0851\3\2\2\2\u085f")
        buf.write("\u0852\3\2\2\2\u085f\u0853\3\2\2\2\u085f\u0854\3\2\2\2")
        buf.write("\u085f\u0855\3\2\2\2\u085f\u0856\3\2\2\2\u085f\u0857\3")
        buf.write("\2\2\2\u085f\u0859\3\2\2\2\u085f\u085d\3\2\2\2\u085f\u085e")
        buf.write("\3\2\2\2\u0860\u019b\3\2\2\2\u0861\u0865\5\u01aa\u00d6")
        buf.write("\2\u0862\u0863\5\u019e\u00d0\2\u0863\u0864\5\u01aa\u00d6")
        buf.write("\2\u0864\u0866\3\2\2\2\u0865\u0862\3\2\2\2\u0865\u0866")
        buf.write("\3\2\2\2\u0866\u019d\3\2\2\2\u0867\u0868\t\f\2\2\u0868")
        buf.write("\u019f\3\2\2\2\u0869\u086b\5\u0112\u008a\2\u086a\u0869")
        buf.write("\3\2\2\2\u086a\u086b\3\2\2\2\u086b\u086c\3\2\2\2\u086c")
        buf.write("\u086d\5\u01dc\u00ef\2\u086d\u086f\7\u0085\2\2\u086e\u0870")
        buf.write("\5\u008aF\2\u086f\u086e\3\2\2\2\u086f\u0870\3\2\2\2\u0870")
        buf.write("\u0871\3\2\2\2\u0871\u0872\5\u01fa\u00fe\2\u0872\u0873")
        buf.write("\7\u008c\2\2\u0873\u01a1\3\2\2\2\u0874\u0875\7X\2\2\u0875")
        buf.write("\u0876\5\u00eav\2\u0876\u0877\7\u0093\2\2\u0877\u0879")
        buf.write("\5\u01d8\u00ed\2\u0878\u087a\5\u01a4\u00d3\2\u0879\u0878")
        buf.write("\3\2\2\2\u0879\u087a\3\2\2\2\u087a\u087d\3\2\2\2\u087b")
        buf.write("\u087c\7\u0089\2\2\u087c\u087e\5\u00c2b\2\u087d\u087b")
        buf.write("\3\2\2\2\u087d\u087e\3\2\2\2\u087e\u087f\3\2\2\2\u087f")
        buf.write("\u0880\7\u008c\2\2\u0880\u01a3\3\2\2\2\u0881\u0882\t\r")
        buf.write("\2\2\u0882\u01a5\3\2\2\2\u0883\u0888\5\u0126\u0094\2\u0884")
        buf.write("\u0885\7\u008d\2\2\u0885\u0887\5\u0126\u0094\2\u0886\u0884")
        buf.write("\3\2\2\2\u0887\u088a\3\2\2\2\u0888\u0886\3\2\2\2\u0888")
        buf.write("\u0889\3\2\2\2\u0889\u088e\3\2\2\2\u088a\u0888\3\2\2\2")
        buf.write("\u088b\u088e\7@\2\2\u088c\u088e\7\b\2\2\u088d\u0883\3")
        buf.write("\2\2\2\u088d\u088b\3\2\2\2\u088d\u088c\3\2\2\2\u088e\u01a7")
        buf.write("\3\2\2\2\u088f\u0898\7\u0091\2\2\u0890\u0895\5\u0126\u0094")
        buf.write("\2\u0891\u0892\7\u008d\2\2\u0892\u0894\5\u0126\u0094\2")
        buf.write("\u0893\u0891\3\2\2\2\u0894\u0897\3\2\2\2\u0895\u0893\3")
        buf.write("\2\2\2\u0895\u0896\3\2\2\2\u0896\u0899\3\2\2\2\u0897\u0895")
        buf.write("\3\2\2\2\u0898\u0890\3\2\2\2\u0898\u0899\3\2\2\2\u0899")
        buf.write("\u089c\3\2\2\2\u089a\u089b\7R\2\2\u089b\u089d\5\u0126")
        buf.write("\u0094\2\u089c\u089a\3\2\2\2\u089c\u089d\3\2\2\2\u089d")
        buf.write("\u089e\3\2\2\2\u089e\u089f\7\u0092\2\2\u089f\u01a9\3\2")
        buf.write("\2\2\u08a0\u08a2\t\16\2\2\u08a1\u08a0\3\2\2\2\u08a1\u08a2")
        buf.write("\3\2\2\2\u08a2\u08a3\3\2\2\2\u08a3\u08a9\5\u01de\u00f0")
        buf.write("\2\u08a4\u08a5\5\16\b\2\u08a5\u08a6\5\u01de\u00f0\2\u08a6")
        buf.write("\u08a8\3\2\2\2\u08a7\u08a4\3\2\2\2\u08a8\u08ab\3\2\2\2")
        buf.write("\u08a9\u08a7\3\2\2\2\u08a9\u08aa\3\2\2\2\u08aa\u01ab\3")
        buf.write("\2\2\2\u08ab\u08a9\3\2\2\2\u08ac\u08ae\5\u0112\u008a\2")
        buf.write("\u08ad\u08ac\3\2\2\2\u08ad\u08ae\3\2\2\2\u08ae\u08af\3")
        buf.write("\2\2\2\u08af\u08b0\5\u01aa\u00d6\2\u08b0\u08b1\7\u0084")
        buf.write("\2\2\u08b1\u08b3\5\u01aa\u00d6\2\u08b2\u08b4\5\u01e8\u00f5")
        buf.write("\2\u08b3\u08b2\3\2\2\2\u08b3\u08b4\3\2\2\2\u08b4\u08b5")
        buf.write("\3\2\2\2\u08b5\u08b6\7\u008c\2\2\u08b6\u01ad\3\2\2\2\u08b7")
        buf.write("\u08b8\7n\2\2\u08b8\u08b9\5V,\2\u08b9\u08ba\7\u0087\2")
        buf.write("\2\u08ba\u08bb\5\u01b8\u00dd\2\u08bb\u01af\3\2\2\2\u08bc")
        buf.write("\u08be\5\u0112\u008a\2\u08bd\u08bc\3\2\2\2\u08bd\u08be")
        buf.write("\3\2\2\2\u08be\u08bf\3\2\2\2\u08bf\u08c0\7\24\2\2\u08c0")
        buf.write("\u08c1\5\u00c2b\2\u08c1\u08c3\7j\2\2\u08c2\u08c4\5\u01ae")
        buf.write("\u00d8\2\u08c3\u08c2\3\2\2\2\u08c4\u08c5\3\2\2\2\u08c5")
        buf.write("\u08c3\3\2\2\2\u08c5\u08c6\3\2\2\2\u08c6\u08c7\3\2\2\2")
        buf.write("\u08c7\u08c8\7\32\2\2\u08c8\u08ca\7\24\2\2\u08c9\u08cb")
        buf.write("\5\u00e8u\2\u08ca\u08c9\3\2\2\2\u08ca\u08cb\3\2\2\2\u08cb")
        buf.write("\u08cc\3\2\2\2\u08cc\u08cd\7\u008c\2\2\u08cd\u01b1\3\2")
        buf.write("\2\2\u08ce\u08d0\5\u0112\u008a\2\u08cf\u08ce\3\2\2\2\u08cf")
        buf.write("\u08d0\3\2\2\2\u08d0\u08d1\3\2\2\2\u08d1\u08d2\7&\2\2")
        buf.write("\u08d2\u08d3\5l\67\2\u08d3\u08d4\7j\2\2\u08d4\u08dc\5")
        buf.write("\u01b8\u00dd\2\u08d5\u08d6\7\35\2\2\u08d6\u08d7\5l\67")
        buf.write("\2\u08d7\u08d8\7j\2\2\u08d8\u08d9\5\u01b8\u00dd\2\u08d9")
        buf.write("\u08db\3\2\2\2\u08da\u08d5\3\2\2\2\u08db\u08de\3\2\2\2")
        buf.write("\u08dc\u08da\3\2\2\2\u08dc\u08dd\3\2\2\2\u08dd\u08e1\3")
        buf.write("\2\2\2\u08de\u08dc\3\2\2\2\u08df\u08e0\7\34\2\2\u08e0")
        buf.write("\u08e2\5\u01b8\u00dd\2\u08e1\u08df\3\2\2\2\u08e1\u08e2")
        buf.write("\3\2\2\2\u08e2\u08e3\3\2\2\2\u08e3\u08e4\7\32\2\2\u08e4")
        buf.write("\u08e6\7j\2\2\u08e5\u08e7\5\u00e8u\2\u08e6\u08e5\3\2\2")
        buf.write("\2\u08e6\u08e7\3\2\2\2\u08e7\u08e8\3\2\2\2\u08e8\u08e9")
        buf.write("\7\u008c\2\2\u08e9\u01b3\3\2\2\2\u08ea\u08ec\5\u0112\u008a")
        buf.write("\2\u08eb\u08ea\3\2\2\2\u08eb\u08ec\3\2\2\2\u08ec\u08ed")
        buf.write("\3\2\2\2\u08ed\u08ef\7G\2\2\u08ee\u08f0\7+\2\2\u08ef\u08ee")
        buf.write("\3\2\2\2\u08ef\u08f0\3\2\2\2\u08f0\u08f1\3\2\2\2\u08f1")
        buf.write("\u08f2\5\u015e\u00b0\2\u08f2\u08f3\7\16\2\2\u08f3\u08f4")
        buf.write("\5\u0160\u00b1\2\u08f4\u08f5\7\32\2\2\u08f5\u08f7\7G\2")
        buf.write("\2\u08f6\u08f8\5\u00e8u\2\u08f7\u08f6\3\2\2\2\u08f7\u08f8")
        buf.write("\3\2\2\2\u08f8\u08f9\3\2\2\2\u08f9\u08fa\7\u008c\2\2\u08fa")
        buf.write("\u01b5\3\2\2\2\u08fb\u0905\5\u01ac\u00d7\2\u08fc\u0905")
        buf.write("\5\u01b2\u00da\2\u08fd\u0905\5\u01b0\u00d9\2\u08fe\u0905")
        buf.write("\5\u01b4\u00db\2\u08ff\u0901\5\u0112\u008a\2\u0900\u08ff")
        buf.write("\3\2\2\2\u0900\u0901\3\2\2\2\u0901\u0902\3\2\2\2\u0902")
        buf.write("\u0903\7;\2\2\u0903\u0905\7\u008c\2\2\u0904\u08fb\3\2")
        buf.write("\2\2\u0904\u08fc\3\2\2\2\u0904\u08fd\3\2\2\2\u0904\u08fe")
        buf.write("\3\2\2\2\u0904\u0900\3\2\2\2\u0905\u01b7\3\2\2\2\u0906")
        buf.write("\u0908\5\u01b6\u00dc\2\u0907\u0906\3\2\2\2\u0908\u090b")
        buf.write("\3\2\2\2\u0909\u0907\3\2\2\2\u0909\u090a\3\2\2\2\u090a")
        buf.write("\u01b9\3\2\2\2\u090b\u0909\3\2\2\2\u090c\u090d\7[\2\2")
        buf.write("\u090d\u090e\5\u01aa\u00d6\2\u090e\u090f\7\u008d\2\2\u090f")
        buf.write("\u0910\5\u01aa\u00d6\2\u0910\u0914\3\2\2\2\u0911\u0912")
        buf.write("\78\2\2\u0912\u0914\5\u01aa\u00d6\2\u0913\u090c\3\2\2")
        buf.write("\2\u0913\u0911\3\2\2\2\u0914\u01bb\3\2\2\2\u0915\u0916")
        buf.write("\7I\2\2\u0916\u0917\5\u00eav\2\u0917\u0918\7\u0093\2\2")
        buf.write("\u0918\u0919\5\u01d8\u00ed\2\u0919\u091a\5\u01ba\u00de")
        buf.write("\2\u091a\u091b\7\u008c\2\2\u091b\u01bd\3\2\2\2\u091c\u091d")
        buf.write("\7.\2\2\u091d\u091e\5\u0174\u00bb\2\u091e\u091f\7m\2\2")
        buf.write("\u091f\u0920\5\u00c2b\2\u0920\u0921\7\u008c\2\2\u0921")
        buf.write("\u01bf\3\2\2\2\u0922\u0923\7^\2\2\u0923\u0924\5\u00e8")
        buf.write("u\2\u0924\u0925\7+\2\2\u0925\u0926\5\u01c2\u00e2\2\u0926")
        buf.write("\u0927\7\u008c\2\2\u0927\u01c1\3\2\2\2\u0928\u092a\5\u0126")
        buf.write("\u0094\2\u0929\u092b\5\u00eex\2\u092a\u0929\3\2\2\2\u092a")
        buf.write("\u092b\3\2\2\2\u092b\u0932\3\2\2\2\u092c\u092d\7d\2\2")
        buf.write("\u092d\u092e\5\u00c2b\2\u092e\u092f\7\5\2\2\u092f\u0930")
        buf.write("\5\u00c2b\2\u0930\u0931\7b\2\2\u0931\u0933\3\2\2\2\u0932")
        buf.write("\u092c\3\2\2\2\u0932\u0933\3\2\2\2\u0933\u01c3\3\2\2\2")
        buf.write("\u0934\u0935\5\u01ce\u00e8\2\u0935\u0936\7+\2\2\u0936")
        buf.write("\u0937\5\u01ca\u00e6\2\u0937\u0938\7\16\2\2\u0938\u0939")
        buf.write("\5\u01d4\u00eb\2\u0939\u093b\7\32\2\2\u093a\u093c\5\u01cc")
        buf.write("\u00e7\2\u093b\u093a\3\2\2\2\u093b\u093c\3\2\2\2\u093c")
        buf.write("\u093e\3\2\2\2\u093d\u093f\5\u0090I\2\u093e\u093d\3\2")
        buf.write("\2\2\u093e\u093f\3\2\2\2\u093f\u0940\3\2\2\2\u0940\u0941")
        buf.write("\7\u008c\2\2\u0941\u01c5\3\2\2\2\u0942\u0943\5\u01ce\u00e8")
        buf.write("\2\u0943\u0944\7\u008c\2\2\u0944\u01c7\3\2\2\2\u0945\u0953")
        buf.write("\5\u01c6\u00e4\2\u0946\u0953\5\u01c4\u00e3\2\u0947\u0953")
        buf.write("\5\u01ea\u00f6\2\u0948\u0953\5\u01d6\u00ec\2\u0949\u0953")
        buf.write("\5~@\2\u094a\u0953\5\u01f6\u00fc\2\u094b\u0953\5\u00c6")
        buf.write("d\2\u094c\u0953\5\22\n\2\u094d\u0953\5.\30\2\u094e\u0953")
        buf.write("\5\62\32\2\u094f\u0953\5\u01f2\u00fa\2\u0950\u0953\5\u00e4")
        buf.write("s\2\u0951\u0953\5\u00e2r\2\u0952\u0945\3\2\2\2\u0952\u0946")
        buf.write("\3\2\2\2\u0952\u0947\3\2\2\2\u0952\u0948\3\2\2\2\u0952")
        buf.write("\u0949\3\2\2\2\u0952\u094a\3\2\2\2\u0952\u094b\3\2\2\2")
        buf.write("\u0952\u094c\3\2\2\2\u0952\u094d\3\2\2\2\u0952\u094e\3")
        buf.write("\2\2\2\u0952\u094f\3\2\2\2\u0952\u0950\3\2\2\2\u0952\u0951")
        buf.write("\3\2\2\2\u0953\u01c9\3\2\2\2\u0954\u0956\5\u01c8\u00e5")
        buf.write("\2\u0955\u0954\3\2\2\2\u0956\u0959\3\2\2\2\u0957\u0955")
        buf.write("\3\2\2\2\u0957\u0958\3\2\2\2\u0958\u01cb\3\2\2\2\u0959")
        buf.write("\u0957\3\2\2\2\u095a\u095b\t\17\2\2\u095b\u01cd\3\2\2")
        buf.write("\2\u095c\u095f\5\u01d0\u00e9\2\u095d\u095f\5\u01d2\u00ea")
        buf.write("\2\u095e\u095c\3\2\2\2\u095e\u095d\3\2\2\2\u095f\u01cf")
        buf.write("\3\2\2\2\u0960\u0961\7F\2\2\u0961\u0966\5\u0090I\2\u0962")
        buf.write("\u0963\7\u008f\2\2\u0963\u0964\5\u00ceh\2\u0964\u0965")
        buf.write("\7\u0090\2\2\u0965\u0967\3\2\2\2\u0966\u0962\3\2\2\2\u0966")
        buf.write("\u0967\3\2\2\2\u0967\u01d1\3\2\2\2\u0968\u096a\t\20\2")
        buf.write("\2\u0969\u0968\3\2\2\2\u0969\u096a\3\2\2\2\u096a\u096b")
        buf.write("\3\2\2\2\u096b\u096c\7!\2\2\u096c\u0971\5\u0090I\2\u096d")
        buf.write("\u096e\7\u008f\2\2\u096e\u096f\5\u00ceh\2\u096f\u0970")
        buf.write("\7\u0090\2\2\u0970\u0972\3\2\2\2\u0971\u096d\3\2\2\2\u0971")
        buf.write("\u0972\3\2\2\2\u0972\u0973\3\2\2\2\u0973\u0974\7R\2\2")
        buf.write("\u0974\u0975\5\u01d8\u00ed\2\u0975\u01d3\3\2\2\2\u0976")
        buf.write("\u0978\5\u019a\u00ce\2\u0977\u0976\3\2\2\2\u0978\u097b")
        buf.write("\3\2\2\2\u0979\u0977\3\2\2\2\u0979\u097a\3\2\2\2\u097a")
        buf.write("\u01d5\3\2\2\2\u097b\u0979\3\2\2\2\u097c\u097d\7_\2\2")
        buf.write("\u097d\u097e\5\u00e8u\2\u097e\u097f\7+\2\2\u097f\u0980")
        buf.write("\5\u01d8\u00ed\2\u0980\u0981\7\u008c\2\2\u0981\u01d7\3")
        buf.write("\2\2\2\u0982\u0984\5\u0130\u0099\2\u0983\u0985\5\u0130")
        buf.write("\u0099\2\u0984\u0983\3\2\2\2\u0984\u0985\3\2\2\2\u0985")
        buf.write("\u0987\3\2\2\2\u0986\u0988\5\u0084C\2\u0987\u0986\3\2")
        buf.write("\2\2\u0987\u0988\3\2\2\2\u0988\u098a\3\2\2\2\u0989\u098b")
        buf.write("\5\u01e8\u00f5\2\u098a\u0989\3\2\2\2\u098a\u098b\3\2\2")
        buf.write("\2\u098b\u01d9\3\2\2\2\u098c\u0991\5\u00e8u\2\u098d\u0991")
        buf.write("\7\u0080\2\2\u098e\u0991\7\u0081\2\2\u098f\u0991\7\b\2")
        buf.write("\2\u0990\u098c\3\2\2\2\u0990\u098d\3\2\2\2\u0990\u098e")
        buf.write("\3\2\2\2\u0990\u098f\3\2\2\2\u0991\u01db\3\2\2\2\u0992")
        buf.write("\u0995\5\u0126\u0094\2\u0993\u0995\5\20\t\2\u0994\u0992")
        buf.write("\3\2\2\2\u0994\u0993\3\2\2\2\u0995\u01dd\3\2\2\2\u0996")
        buf.write("\u099c\5\u00c4c\2\u0997\u0998\5\u0124\u0093\2\u0998\u0999")
        buf.write("\5\u00c4c\2\u0999\u099b\3\2\2\2\u099a\u0997\3\2\2\2\u099b")
        buf.write("\u099e\3\2\2\2\u099c\u099a\3\2\2\2\u099c\u099d\3\2\2\2")
        buf.write("\u099d\u01df\3\2\2\2\u099e\u099c\3\2\2\2\u099f\u09a2\5")
        buf.write("\u0126\u0094\2\u09a0\u09a1\7c\2\2\u09a1\u09a3\5\u0126")
        buf.write("\u0094\2\u09a2\u09a0\3\2\2\2\u09a2\u09a3\3\2\2\2\u09a3")
        buf.write("\u01e1\3\2\2\2\u09a4\u09a5\7`\2\2\u09a5\u09a6\5\u00ea")
        buf.write("v\2\u09a6\u09a7\7\u0093\2\2\u09a7\u09a8\5\u01c2\u00e2")
        buf.write("\2\u09a8\u09a9\7\u008c\2\2\u09a9\u01e3\3\2\2\2\u09aa\u09ac")
        buf.write("\5\u00eav\2\u09ab\u09ad\5\u01e8\u00f5\2\u09ac\u09ab\3")
        buf.write("\2\2\2\u09ac\u09ad\3\2\2\2\u09ad\u09b0\3\2\2\2\u09ae\u09af")
        buf.write("\7\u0089\2\2\u09af\u09b1\5\u00c2b\2\u09b0\u09ae\3\2\2")
        buf.write("\2\u09b0\u09b1\3\2\2\2\u09b1\u09b2\3\2\2\2\u09b2\u09b3")
        buf.write("\7b\2\2\u09b3\u01e5\3\2\2\2\u09b4\u09b5\7 \2\2\u09b5\u09b6")
        buf.write("\5\u00c2b\2\u09b6\u01e7\3\2\2\2\u09b7\u09b8\7d\2\2\u09b8")
        buf.write("\u09b9\5\u00c2b\2\u09b9\u01e9\3\2\2\2\u09ba\u09bb\7f\2")
        buf.write("\2\u09bb\u09be\5\u00e8u\2\u09bc\u09bd\7+\2\2\u09bd\u09bf")
        buf.write("\5\u01ec\u00f7\2\u09be\u09bc\3\2\2\2\u09be\u09bf\3\2\2")
        buf.write("\2\u09bf\u09c0\3\2\2\2\u09c0\u09c1\7\u008c\2\2\u09c1\u01eb")
        buf.write("\3\2\2\2\u09c2\u09c7\5\u018a\u00c6\2\u09c3\u09c7\5b\62")
        buf.write("\2\u09c4\u09c7\5\4\3\2\u09c5\u09c7\5\u00ccg\2\u09c6\u09c2")
        buf.write("\3\2\2\2\u09c6\u09c3\3\2\2\2\u09c6\u09c4\3\2\2\2\u09c6")
        buf.write("\u09c5\3\2\2\2\u09c7\u01ed\3\2\2\2\u09c8\u09c9\7\13\2")
        buf.write("\2\u09c9\u09ca\7\u008f\2\2\u09ca\u09cf\5\u00f2z\2\u09cb")
        buf.write("\u09cc\7\u008d\2\2\u09cc\u09ce\5\u00f2z\2\u09cd\u09cb")
        buf.write("\3\2\2\2\u09ce\u09d1\3\2\2\2\u09cf\u09cd\3\2\2\2\u09cf")
        buf.write("\u09d0\3\2\2\2\u09d0\u09d2\3\2\2\2\u09d1\u09cf\3\2\2\2")
        buf.write("\u09d2\u09d3\7\u0090\2\2\u09d3\u09d4\7<\2\2\u09d4\u09d5")
        buf.write("\5\u01d8\u00ed\2\u09d5\u01ef\3\2\2\2\u09d6\u09d7\7\13")
        buf.write("\2\2\u09d7\u09d8\7\u008f\2\2\u09d8\u09dd\5\u00f2z\2\u09d9")
        buf.write("\u09da\7\u008d\2\2\u09da\u09dc\5\u00f2z\2\u09db\u09d9")
        buf.write("\3\2\2\2\u09dc\u09df\3\2\2\2\u09dd\u09db\3\2\2\2\u09dd")
        buf.write("\u09de\3\2\2\2\u09de\u09e0\3\2\2\2\u09df\u09dd\3\2\2\2")
        buf.write("\u09e0\u09e1\7\u0090\2\2\u09e1\u09e2\7<\2\2\u09e2\u09e3")
        buf.write("\5\u01c2\u00e2\2\u09e3\u01f1\3\2\2\2\u09e4\u09e5\7j\2")
        buf.write("\2\u09e5\u09ea\5\u0130\u0099\2\u09e6\u09e7\7\u008d\2\2")
        buf.write("\u09e7\u09e9\5\u0130\u0099\2\u09e8\u09e6\3\2\2\2\u09e9")
        buf.write("\u09ec\3\2\2\2\u09ea\u09e8\3\2\2\2\u09ea\u09eb\3\2\2\2")
        buf.write("\u09eb\u09ed\3\2\2\2\u09ec\u09ea\3\2\2\2\u09ed\u09ee\7")
        buf.write("\u008c\2\2\u09ee\u01f3\3\2\2\2\u09ef\u09f1\5\u0112\u008a")
        buf.write("\2\u09f0\u09ef\3\2\2\2\u09f0\u09f1\3\2\2\2\u09f1\u09f2")
        buf.write("\3\2\2\2\u09f2\u09f3\5\u01dc\u00ef\2\u09f3\u09f4\7\u0089")
        buf.write("\2\2\u09f4\u09f5\5\u00c2b\2\u09f5\u09f6\7\u008c\2\2\u09f6")
        buf.write("\u01f5\3\2\2\2\u09f7\u09f9\7W\2\2\u09f8\u09f7\3\2\2\2")
        buf.write("\u09f8\u09f9\3\2\2\2\u09f9\u09fa\3\2\2\2\u09fa\u09fb\7")
        buf.write("k\2\2\u09fb\u09fc\5\u00eav\2\u09fc\u09fd\7\u0093\2\2\u09fd")
        buf.write("\u0a00\5\u01d8\u00ed\2\u09fe\u09ff\7\u0089\2\2\u09ff\u0a01")
        buf.write("\5\u00c2b\2\u0a00\u09fe\3\2\2\2\u0a00\u0a01\3\2\2\2\u0a01")
        buf.write("\u0a02\3\2\2\2\u0a02\u0a03\7\u008c\2\2\u0a03\u01f7\3\2")
        buf.write("\2\2\u0a04\u0a06\5\u0112\u008a\2\u0a05\u0a04\3\2\2\2\u0a05")
        buf.write("\u0a06\3\2\2\2\u0a06\u0a07\3\2\2\2\u0a07\u0a09\7l\2\2")
        buf.write("\u0a08\u0a0a\5\u0194\u00cb\2\u0a09\u0a08\3\2\2\2\u0a09")
        buf.write("\u0a0a\3\2\2\2\u0a0a\u0a0c\3\2\2\2\u0a0b\u0a0d\5n8\2\u0a0c")
        buf.write("\u0a0b\3\2\2\2\u0a0c\u0a0d\3\2\2\2\u0a0d\u0a0f\3\2\2\2")
        buf.write("\u0a0e\u0a10\5\u01e6\u00f4\2\u0a0f\u0a0e\3\2\2\2\u0a0f")
        buf.write("\u0a10\3\2\2\2\u0a10\u0a11\3\2\2\2\u0a11\u0a12\7\u008c")
        buf.write("\2\2\u0a12\u01f9\3\2\2\2\u0a13\u0a18\5\u01fc\u00ff\2\u0a14")
        buf.write("\u0a15\7\u008d\2\2\u0a15\u0a17\5\u01fc\u00ff\2\u0a16\u0a14")
        buf.write("\3\2\2\2\u0a17\u0a1a\3\2\2\2\u0a18\u0a16\3\2\2\2\u0a18")
        buf.write("\u0a19\3\2\2\2\u0a19\u0a1d\3\2\2\2\u0a1a\u0a18\3\2\2\2")
        buf.write("\u0a1b\u0a1d\7g\2\2\u0a1c\u0a13\3\2\2\2\u0a1c\u0a1b\3")
        buf.write("\2\2\2\u0a1d\u01fb\3\2\2\2\u0a1e\u0a21\5\u00c2b\2\u0a1f")
        buf.write("\u0a20\7\6\2\2\u0a20\u0a22\5\u00c2b\2\u0a21\u0a1f\3\2")
        buf.write("\2\2\u0a21\u0a22\3\2\2\2\u0a22\u01fd\3\2\2\2\u0126\u0205")
        buf.write("\u0209\u020f\u0219\u0223\u022c\u0231\u0238\u023c\u0241")
        buf.write("\u024d\u0250\u0257\u025d\u0261\u0265\u0268\u026f\u0274")
        buf.write("\u0279\u027d\u0283\u0287\u028a\u0292\u029b\u02aa\u02b9")
        buf.write("\u02bc\u02bf\u02c6\u02cc\u02e9\u02ee\u02f5\u02f7\u02fd")
        buf.write("\u02ff\u0306\u0309\u0311\u0314\u031d\u0324\u0329\u032c")
        buf.write("\u0332\u033d\u0345\u0349\u034d\u0352\u035a\u035f\u036c")
        buf.write("\u0373\u037b\u037e\u0387\u038a\u038d\u0392\u0399\u039c")
        buf.write("\u03a6\u03aa\u03ad\u03b0\u03b6\u03ba\u03bd\u03c1\u03c6")
        buf.write("\u03c9\u03cf\u03d2\u03d6\u03e8\u03ea\u03f5\u03f8\u03ff")
        buf.write("\u0404\u0409\u0416\u0426\u042b\u0430\u0435\u0438\u043d")
        buf.write("\u0447\u0453\u0458\u046b\u0470\u0476\u047d\u0487\u048b")
        buf.write("\u048e\u04a6\u04ab\u04b0\u04b3\u04b6\u04bd\u04c2\u04cb")
        buf.write("\u04d0\u04d6\u04da\u04e2\u04e8\u04ec\u04f0\u04fa\u0500")
        buf.write("\u0506\u050d\u0515\u0526\u052e\u0538\u053c\u0541\u0547")
        buf.write("\u054f\u055c\u0567\u056e\u058c\u0590\u059d\u05a2\u05a7")
        buf.write("\u05b1\u05b8\u05bf\u05c8\u05cc\u05d3\u05d8\u05db\u05e0")
        buf.write("\u05e5\u05ed\u05fb\u0603\u060b\u0612\u0617\u061e\u0622")
        buf.write("\u0629\u062d\u0635\u063a\u063f\u0645\u0650\u0657\u0660")
        buf.write("\u0666\u0669\u0670\u067e\u0681\u0687\u0690\u0693\u0697")
        buf.write("\u06a1\u06ab\u06b6\u06bd\u06c1\u06c5\u06cb\u06d3\u06d6")
        buf.write("\u06d9\u06e3\u06e6\u06f5\u06fa\u0703\u0706\u071c\u0721")
        buf.write("\u0731\u0737\u0750\u0755\u0763\u0768\u076e\u0776\u0779")
        buf.write("\u078b\u0790\u0794\u0797\u079e\u07a1\u07a8\u07ac\u07b3")
        buf.write("\u07bd\u07c2\u07c9\u07ce\u07d6\u07e3\u07e8\u07ee\u07f3")
        buf.write("\u07f9\u07fe\u0804\u0809\u080d\u081b\u081f\u0839\u0844")
        buf.write("\u084a\u0859\u085f\u0865\u086a\u086f\u0879\u087d\u0888")
        buf.write("\u088d\u0895\u0898\u089c\u08a1\u08a9\u08ad\u08b3\u08bd")
        buf.write("\u08c5\u08ca\u08cf\u08dc\u08e1\u08e6\u08eb\u08ef\u08f7")
        buf.write("\u0900\u0904\u0909\u0913\u092a\u0932\u093b\u093e\u0952")
        buf.write("\u0957\u095e\u0966\u0969\u0971\u0979\u0984\u0987\u098a")
        buf.write("\u0990\u0994\u099c\u09a2\u09ac\u09b0\u09be\u09c6\u09cf")
        buf.write("\u09dd\u09ea\u09f0\u09f8\u0a00\u0a05\u0a09\u0a0c\u0a0f")
        buf.write("\u0a18\u0a1c\u0a21")
        return buf.getvalue()


class vhdlParser (Parser):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = np.array([ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"'\n'", u"'\r'", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"'**'", u"'=='", u"'<='", u"'>='", u"'=>'", u"'/='",
                     u"':='", u"'<>'", u"'\"'", u"';'", u"','", u"'&'",
                     u"'('", u"')'", u"'['", u"']'", u"':'", u"'*'", u"'/'",
                     u"'+'", u"'-'", u"'<'", u"'>'", u"'='", u"'|'", u"'.'",
                     u"'\\'", u"<INVALID>", u"<INVALID>", u"<INVALID>",
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"'''" ])

    symbolicNames = np.array([ u"<INVALID>", u"ABS", u"ACCESS", u"ACROSS", u"AFTER",
                      u"ALIAS", u"ALL", u"AND", u"ARCHITECTURE", u"ARRAY",
                      u"ASSERT", u"ATTRIBUTE", u"BEGIN", u"BLOCK", u"BODY",
                      u"BREAK", u"BUFFER", u"BUS", u"CASE", u"COMPONENT",
                      u"CONFIGURATION", u"CONSTANT", u"DISCONNECT", u"DOWNTO",
                      u"END", u"ENTITY", u"ELSE", u"ELSIF", u"EXIT", u"FILE",
                      u"FOR", u"FUNCTION", u"GENERATE", u"GENERIC", u"GROUP",
                      u"GUARDED", u"IF", u"IMPURE", u"IN", u"INERTIAL",
                      u"INOUT", u"IS", u"LABEL", u"LIBRARY", u"LIMIT", u"LINKAGE",
                      u"LITERAL", u"LOOP", u"MAP", u"MOD", u"NAND", u"NATURE",
                      u"NEW", u"NEXT", u"NOISE", u"NOR", u"NOT", u"NULL",
                      u"OF", u"ON", u"OPEN", u"OR", u"OTHERS", u"OUT", u"PACKAGE",
                      u"PORT", u"POSTPONED", u"PROCESS", u"PROCEDURE", u"PROCEDURAL",
                      u"PURE", u"QUANTITY", u"RANGE", u"REVERSE_RANGE",
                      u"REJECT", u"REM", u"RECORD", u"REFERENCE", u"REGISTER",
                      u"REPORT", u"RETURN", u"ROL", u"ROR", u"SELECT", u"SEVERITY",
                      u"SHARED", u"SIGNAL", u"SLA", u"SLL", u"SPECTRUM",
                      u"SRA", u"SRL", u"SUBNATURE", u"SUBTYPE", u"TERMINAL",
                      u"THEN", u"THROUGH", u"TO", u"TOLERANCE", u"TRANSPORT",
                      u"TYPE", u"UNAFFECTED", u"UNITS", u"UNTIL", u"USE",
                      u"VARIABLE", u"WAIT", u"WITH", u"WHEN", u"WHILE",
                      u"XNOR", u"XOR", u"BASE_LITERAL", u"BIT_STRING_LITERAL",
                      u"BIT_STRING_LITERAL_BINARY", u"BIT_STRING_LITERAL_OCTAL",
                      u"BIT_STRING_LITERAL_HEX", u"REAL_LITERAL", u"BASIC_IDENTIFIER",
                      u"EXTENDED_IDENTIFIER", u"LETTER", u"COMMENT", u"TAB",
                      u"SPACE", u"NEWLINE", u"CR", u"CHARACTER_LITERAL",
                      u"STRING_LITERAL", u"OTHER_SPECIAL_CHARACTER", u"DOUBLESTAR",
                      u"ASSIGN", u"LE", u"GE", u"ARROW", u"NEQ", u"VARASGN",
                      u"BOX", u"DBLQUOTE", u"SEMI", u"COMMA", u"AMPERSAND",
                      u"LPAREN", u"RPAREN", u"LBRACKET", u"RBRACKET", u"COLON",
                      u"MUL", u"DIV", u"PLUS", u"MINUS", u"LOWERTHAN", u"GREATERTHAN",
                      u"EQ", u"BAR", u"DOT", u"BACKSLASH", u"EXPONENT",
                      u"HEXDIGIT", u"INTEGER", u"DIGIT", u"BASED_INTEGER",
                      u"EXTENDED_DIGIT", u"APOSTROPHE" ])

    RULE_abstract_literal = 0
    RULE_access_type_definition = 1
    RULE_across_aspect = 2
    RULE_actual_designator = 3
    RULE_actual_parameter_part = 4
    RULE_actual_part = 5
    RULE_adding_operator = 6
    RULE_aggregate = 7
    RULE_alias_declaration = 8
    RULE_alias_designator = 9
    RULE_alias_indication = 10
    RULE_allocator = 11
    RULE_architecture_body = 12
    RULE_architecture_declarative_part = 13
    RULE_architecture_statement = 14
    RULE_architecture_statement_part = 15
    RULE_array_nature_definition = 16
    RULE_array_type_definition = 17
    RULE_assertion = 18
    RULE_assertion_statement = 19
    RULE_association_element = 20
    RULE_association_list = 21
    RULE_attribute_declaration = 22
    RULE_attribute_designator = 23
    RULE_attribute_specification = 24
    RULE_base_unit_declaration = 25
    RULE_binding_indication = 26
    RULE_block_configuration = 27
    RULE_block_declarative_item = 28
    RULE_block_declarative_part = 29
    RULE_block_header = 30
    RULE_block_specification = 31
    RULE_block_statement = 32
    RULE_block_statement_part = 33
    RULE_branch_quantity_declaration = 34
    RULE_break_element = 35
    RULE_break_list = 36
    RULE_break_selector_clause = 37
    RULE_break_statement = 38
    RULE_case_statement = 39
    RULE_case_statement_alternative = 40
    RULE_choice = 41
    RULE_choices = 42
    RULE_component_configuration = 43
    RULE_component_declaration = 44
    RULE_component_instantiation_statement = 45
    RULE_component_specification = 46
    RULE_composite_nature_definition = 47
    RULE_composite_type_definition = 48
    RULE_concurrent_assertion_statement = 49
    RULE_concurrent_break_statement = 50
    RULE_concurrent_procedure_call_statement = 51
    RULE_concurrent_signal_assignment_statement = 52
    RULE_condition = 53
    RULE_condition_clause = 54
    RULE_conditional_signal_assignment = 55
    RULE_conditional_waveforms = 56
    RULE_configuration_declaration = 57
    RULE_configuration_declarative_item = 58
    RULE_configuration_declarative_part = 59
    RULE_configuration_item = 60
    RULE_configuration_specification = 61
    RULE_constant_declaration = 62
    RULE_constrained_array_definition = 63
    RULE_constrained_nature_definition = 64
    RULE_constraint = 65
    RULE_context_clause = 66
    RULE_context_item = 67
    RULE_delay_mechanism = 68
    RULE_design_file = 69
    RULE_design_unit = 70
    RULE_designator = 71
    RULE_direction = 72
    RULE_disconnection_specification = 73
    RULE_discrete_range = 74
    RULE_element_association = 75
    RULE_element_declaration = 76
    RULE_element_subnature_definition = 77
    RULE_element_subtype_definition = 78
    RULE_entity_aspect = 79
    RULE_entity_class = 80
    RULE_entity_class_entry = 81
    RULE_entity_class_entry_list = 82
    RULE_entity_declaration = 83
    RULE_entity_declarative_item = 84
    RULE_entity_declarative_part = 85
    RULE_entity_designator = 86
    RULE_entity_header = 87
    RULE_entity_name_list = 88
    RULE_entity_specification = 89
    RULE_entity_statement = 90
    RULE_entity_statement_part = 91
    RULE_entity_tag = 92
    RULE_enumeration_literal = 93
    RULE_enumeration_type_definition = 94
    RULE_exit_statement = 95
    RULE_expression = 96
    RULE_factor = 97
    RULE_file_declaration = 98
    RULE_file_logical_name = 99
    RULE_file_open_information = 100
    RULE_file_type_definition = 101
    RULE_formal_parameter_list = 102
    RULE_formal_part = 103
    RULE_free_quantity_declaration = 104
    RULE_generate_statement = 105
    RULE_generation_scheme = 106
    RULE_generic_clause = 107
    RULE_generic_list = 108
    RULE_generic_map_aspect = 109
    RULE_group_constituent = 110
    RULE_group_constituent_list = 111
    RULE_group_declaration = 112
    RULE_group_template_declaration = 113
    RULE_guarded_signal_specification = 114
    RULE_identifier = 115
    RULE_identifier_list = 116
    RULE_if_statement = 117
    RULE_index_constraint = 118
    RULE_index_specification = 119
    RULE_index_subtype_definition = 120
    RULE_instantiated_unit = 121
    RULE_instantiation_list = 122
    RULE_interface_constant_declaration = 123
    RULE_interface_declaration = 124
    RULE_interface_element = 125
    RULE_interface_file_declaration = 126
    RULE_interface_signal_list = 127
    RULE_interface_port_list = 128
    RULE_interface_list = 129
    RULE_interface_quantity_declaration = 130
    RULE_interface_port_declaration = 131
    RULE_interface_signal_declaration = 132
    RULE_interface_terminal_declaration = 133
    RULE_interface_variable_declaration = 134
    RULE_iteration_scheme = 135
    RULE_label_colon = 136
    RULE_library_clause = 137
    RULE_library_unit = 138
    RULE_literal = 139
    RULE_logical_name = 140
    RULE_logical_name_list = 141
    RULE_logical_operator = 142
    RULE_loop_statement = 143
    RULE_signal_mode = 144
    RULE_multiplying_operator = 145
    RULE_name = 146
    RULE_name_part = 147
    RULE_name_attribute_part = 148
    RULE_name_function_call_or_indexed_part = 149
    RULE_name_slice_part = 150
    RULE_selected_name = 151
    RULE_nature_declaration = 152
    RULE_nature_definition = 153
    RULE_nature_element_declaration = 154
    RULE_next_statement = 155
    RULE_numeric_literal = 156
    RULE_object_declaration = 157
    RULE_opts = 158
    RULE_package_body = 159
    RULE_package_body_declarative_item = 160
    RULE_package_body_declarative_part = 161
    RULE_package_declaration = 162
    RULE_package_declarative_item = 163
    RULE_package_declarative_part = 164
    RULE_parameter_specification = 165
    RULE_physical_literal = 166
    RULE_physical_type_definition = 167
    RULE_port_clause = 168
    RULE_port_list = 169
    RULE_port_map_aspect = 170
    RULE_primary = 171
    RULE_primary_unit = 172
    RULE_procedural_declarative_item = 173
    RULE_procedural_declarative_part = 174
    RULE_procedural_statement_part = 175
    RULE_procedure_call = 176
    RULE_procedure_call_statement = 177
    RULE_process_declarative_item = 178
    RULE_process_declarative_part = 179
    RULE_process_statement = 180
    RULE_process_statement_part = 181
    RULE_qualified_expression = 182
    RULE_quantity_declaration = 183
    RULE_quantity_list = 184
    RULE_quantity_specification = 185
    RULE_range = 186
    RULE_explicit_range = 187
    RULE_range_constraint = 188
    RULE_record_nature_definition = 189
    RULE_record_type_definition = 190
    RULE_relation = 191
    RULE_relational_operator = 192
    RULE_report_statement = 193
    RULE_return_statement = 194
    RULE_scalar_nature_definition = 195
    RULE_scalar_type_definition = 196
    RULE_secondary_unit = 197
    RULE_secondary_unit_declaration = 198
    RULE_selected_signal_assignment = 199
    RULE_selected_waveforms = 200
    RULE_sensitivity_clause = 201
    RULE_sensitivity_list = 202
    RULE_sequence_of_statements = 203
    RULE_sequential_statement = 204
    RULE_shift_expression = 205
    RULE_shift_operator = 206
    RULE_signal_assignment_statement = 207
    RULE_signal_declaration = 208
    RULE_signal_kind = 209
    RULE_signal_list = 210
    RULE_signature = 211
    RULE_simple_expression = 212
    RULE_simple_simultaneous_statement = 213
    RULE_simultaneous_alternative = 214
    RULE_simultaneous_case_statement = 215
    RULE_simultaneous_if_statement = 216
    RULE_simultaneous_procedural_statement = 217
    RULE_simultaneous_statement = 218
    RULE_simultaneous_statement_part = 219
    RULE_source_aspect = 220
    RULE_source_quantity_declaration = 221
    RULE_step_limit_specification = 222
    RULE_subnature_declaration = 223
    RULE_subnature_indication = 224
    RULE_subprogram_body = 225
    RULE_subprogram_declaration = 226
    RULE_subprogram_declarative_item = 227
    RULE_subprogram_declarative_part = 228
    RULE_subprogram_kind = 229
    RULE_subprogram_specification = 230
    RULE_procedure_specification = 231
    RULE_function_specification = 232
    RULE_subprogram_statement_part = 233
    RULE_subtype_declaration = 234
    RULE_subtype_indication = 235
    RULE_suffix = 236
    RULE_target = 237
    RULE_term = 238
    RULE_terminal_aspect = 239
    RULE_terminal_declaration = 240
    RULE_through_aspect = 241
    RULE_timeout_clause = 242
    RULE_tolerance_aspect = 243
    RULE_type_declaration = 244
    RULE_type_definition = 245
    RULE_unconstrained_array_definition = 246
    RULE_unconstrained_nature_definition = 247
    RULE_use_clause = 248
    RULE_variable_assignment_statement = 249
    RULE_variable_declaration = 250
    RULE_wait_statement = 251
    RULE_waveform = 252
    RULE_waveform_element = 253

    ruleNames = np.array([ "abstract_literal", "access_type_definition", "across_aspect",
                   "actual_designator", "actual_parameter_part", "actual_part",
                   "adding_operator", "aggregate", "alias_declaration",
                   "alias_designator", "alias_indication", "allocator",
                   "architecture_body", "architecture_declarative_part",
                   "architecture_statement", "architecture_statement_part",
                   "array_nature_definition", "array_type_definition", "assertion",
                   "assertion_statement", "association_element", "association_list",
                   "attribute_declaration", "attribute_designator", "attribute_specification",
                   "base_unit_declaration", "binding_indication", "block_configuration",
                   "block_declarative_item", "block_declarative_part", "block_header",
                   "block_specification", "block_statement", "block_statement_part",
                   "branch_quantity_declaration", "break_element", "break_list",
                   "break_selector_clause", "break_statement", "case_statement",
                   "case_statement_alternative", "choice", "choices", "component_configuration",
                   "component_declaration", "component_instantiation_statement",
                   "component_specification", "composite_nature_definition",
                   "composite_type_definition", "concurrent_assertion_statement",
                   "concurrent_break_statement", "concurrent_procedure_call_statement",
                   "concurrent_signal_assignment_statement", "condition",
                   "condition_clause", "conditional_signal_assignment",
                   "conditional_waveforms", "configuration_declaration",
                   "configuration_declarative_item", "configuration_declarative_part",
                   "configuration_item", "configuration_specification",
                   "constant_declaration", "constrained_array_definition",
                   "constrained_nature_definition", "constraint", "context_clause",
                   "context_item", "delay_mechanism", "design_file", "design_unit",
                   "designator", "direction", "disconnection_specification",
                   "discrete_range", "element_association", "element_declaration",
                   "element_subnature_definition", "element_subtype_definition",
                   "entity_aspect", "entity_class", "entity_class_entry",
                   "entity_class_entry_list", "entity_declaration", "entity_declarative_item",
                   "entity_declarative_part", "entity_designator", "entity_header",
                   "entity_name_list", "entity_specification", "entity_statement",
                   "entity_statement_part", "entity_tag", "enumeration_literal",
                   "enumeration_type_definition", "exit_statement", "expression",
                   "factor", "file_declaration", "file_logical_name", "file_open_information",
                   "file_type_definition", "formal_parameter_list", "formal_part",
                   "free_quantity_declaration", "generate_statement", "generation_scheme",
                   "generic_clause", "generic_list", "generic_map_aspect",
                   "group_constituent", "group_constituent_list", "group_declaration",
                   "group_template_declaration", "guarded_signal_specification",
                   "identifier", "identifier_list", "if_statement", "index_constraint",
                   "index_specification", "index_subtype_definition", "instantiated_unit",
                   "instantiation_list", "interface_constant_declaration",
                   "interface_declaration", "interface_element", "interface_file_declaration",
                   "interface_signal_list", "interface_port_list", "interface_list",
                   "interface_quantity_declaration", "interface_port_declaration",
                   "interface_signal_declaration", "interface_terminal_declaration",
                   "interface_variable_declaration", "iteration_scheme",
                   "label_colon", "library_clause", "library_unit", "literal",
                   "logical_name", "logical_name_list", "logical_operator",
                   "loop_statement", "signal_mode", "multiplying_operator",
                   "name", "name_part", "name_attribute_part", "name_function_call_or_indexed_part",
                   "name_slice_part", "selected_name", "nature_declaration",
                   "nature_definition", "nature_element_declaration", "next_statement",
                   "numeric_literal", "object_declaration", "opts", "package_body",
                   "package_body_declarative_item", "package_body_declarative_part",
                   "package_declaration", "package_declarative_item", "package_declarative_part",
                   "parameter_specification", "physical_literal", "physical_type_definition",
                   "port_clause", "port_list", "port_map_aspect", "primary",
                   "primary_unit", "procedural_declarative_item", "procedural_declarative_part",
                   "procedural_statement_part", "procedure_call", "procedure_call_statement",
                   "process_declarative_item", "process_declarative_part",
                   "process_statement", "process_statement_part", "qualified_expression",
                   "quantity_declaration", "quantity_list", "quantity_specification",
                   "range", "explicit_range", "range_constraint", "record_nature_definition",
                   "record_type_definition", "relation", "relational_operator",
                   "report_statement", "return_statement", "scalar_nature_definition",
                   "scalar_type_definition", "secondary_unit", "secondary_unit_declaration",
                   "selected_signal_assignment", "selected_waveforms", "sensitivity_clause",
                   "sensitivity_list", "sequence_of_statements", "sequential_statement",
                   "shift_expression", "shift_operator", "signal_assignment_statement",
                   "signal_declaration", "signal_kind", "signal_list", "signature",
                   "simple_expression", "simple_simultaneous_statement",
                   "simultaneous_alternative", "simultaneous_case_statement",
                   "simultaneous_if_statement", "simultaneous_procedural_statement",
                   "simultaneous_statement", "simultaneous_statement_part",
                   "source_aspect", "source_quantity_declaration", "step_limit_specification",
                   "subnature_declaration", "subnature_indication", "subprogram_body",
                   "subprogram_declaration", "subprogram_declarative_item",
                   "subprogram_declarative_part", "subprogram_kind", "subprogram_specification",
                   "procedure_specification", "function_specification",
                   "subprogram_statement_part", "subtype_declaration", "subtype_indication",
                   "suffix", "target", "term", "terminal_aspect", "terminal_declaration",
                   "through_aspect", "timeout_clause", "tolerance_aspect",
                   "type_declaration", "type_definition", "unconstrained_array_definition",
                   "unconstrained_nature_definition", "use_clause", "variable_assignment_statement",
                   "variable_declaration", "wait_statement", "waveform",
                   "waveform_element" ])

    EOF = Token.EOF
    ABS = 1
    ACCESS = 2
    ACROSS = 3
    AFTER = 4
    ALIAS = 5
    ALL = 6
    AND = 7
    ARCHITECTURE = 8
    ARRAY = 9
    ASSERT = 10
    ATTRIBUTE = 11
    BEGIN = 12
    BLOCK = 13
    BODY = 14
    BREAK = 15
    BUFFER = 16
    BUS = 17
    CASE = 18
    COMPONENT = 19
    CONFIGURATION = 20
    CONSTANT = 21
    DISCONNECT = 22
    DOWNTO = 23
    END = 24
    ENTITY = 25
    ELSE = 26
    ELSIF = 27
    EXIT = 28
    FILE = 29
    FOR = 30
    FUNCTION = 31
    GENERATE = 32
    GENERIC = 33
    GROUP = 34
    GUARDED = 35
    IF = 36
    IMPURE = 37
    IN = 38
    INERTIAL = 39
    INOUT = 40
    IS = 41
    LABEL = 42
    LIBRARY = 43
    LIMIT = 44
    LINKAGE = 45
    LITERAL = 46
    LOOP = 47
    MAP = 48
    MOD = 49
    NAND = 50
    NATURE = 51
    NEW = 52
    NEXT = 53
    NOISE = 54
    NOR = 55
    NOT = 56
    NULL = 57
    OF = 58
    ON = 59
    OPEN = 60
    OR = 61
    OTHERS = 62
    OUT = 63
    PACKAGE = 64
    PORT = 65
    POSTPONED = 66
    PROCESS = 67
    PROCEDURE = 68
    PROCEDURAL = 69
    PURE = 70
    QUANTITY = 71
    RANGE = 72
    REVERSE_RANGE = 73
    REJECT = 74
    REM = 75
    RECORD = 76
    REFERENCE = 77
    REGISTER = 78
    REPORT = 79
    RETURN = 80
    ROL = 81
    ROR = 82
    SELECT = 83
    SEVERITY = 84
    SHARED = 85
    SIGNAL = 86
    SLA = 87
    SLL = 88
    SPECTRUM = 89
    SRA = 90
    SRL = 91
    SUBNATURE = 92
    SUBTYPE = 93
    TERMINAL = 94
    THEN = 95
    THROUGH = 96
    TO = 97
    TOLERANCE = 98
    TRANSPORT = 99
    TYPE = 100
    UNAFFECTED = 101
    UNITS = 102
    UNTIL = 103
    USE = 104
    VARIABLE = 105
    WAIT = 106
    WITH = 107
    WHEN = 108
    WHILE = 109
    XNOR = 110
    XOR = 111
    BASE_LITERAL = 112
    BIT_STRING_LITERAL = 113
    BIT_STRING_LITERAL_BINARY = 114
    BIT_STRING_LITERAL_OCTAL = 115
    BIT_STRING_LITERAL_HEX = 116
    REAL_LITERAL = 117
    BASIC_IDENTIFIER = 118
    EXTENDED_IDENTIFIER = 119
    LETTER = 120
    COMMENT = 121
    TAB = 122
    SPACE = 123
    NEWLINE = 124
    CR = 125
    CHARACTER_LITERAL = 126
    STRING_LITERAL = 127
    OTHER_SPECIAL_CHARACTER = 128
    DOUBLESTAR = 129
    ASSIGN = 130
    LE = 131
    GE = 132
    ARROW = 133
    NEQ = 134
    VARASGN = 135
    BOX = 136
    DBLQUOTE = 137
    SEMI = 138
    COMMA = 139
    AMPERSAND = 140
    LPAREN = 141
    RPAREN = 142
    LBRACKET = 143
    RBRACKET = 144
    COLON = 145
    MUL = 146
    DIV = 147
    PLUS = 148
    MINUS = 149
    LOWERTHAN = 150
    GREATERTHAN = 151
    EQ = 152
    BAR = 153
    DOT = 154
    BACKSLASH = 155
    EXPONENT = 156
    HEXDIGIT = 157
    INTEGER = 158
    DIGIT = 159
    BASED_INTEGER = 160
    EXTENDED_DIGIT = 161
    APOSTROPHE = 162

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class Abstract_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(vhdlParser.INTEGER, 0)

        def REAL_LITERAL(self):
            return self.getToken(vhdlParser.REAL_LITERAL, 0)

        def BASE_LITERAL(self):
            return self.getToken(vhdlParser.BASE_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_abstract_literal

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAbstract_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAbstract_literal(self)




    def abstract_literal(self):

        localctx = vhdlParser.Abstract_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_abstract_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 508
            _la = self._input.LA(1)
            if not(((((_la - 112)) & ~0x3f) == 0 and ((1 << (_la - 112)) & ((1 << (vhdlParser.BASE_LITERAL - 112)) | (1 << (vhdlParser.REAL_LITERAL - 112)) | (1 << (vhdlParser.INTEGER - 112)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Access_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ACCESS(self):
            return self.getToken(vhdlParser.ACCESS, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_access_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAccess_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAccess_type_definition(self)




    def access_type_definition(self):

        localctx = vhdlParser.Access_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_access_type_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 510
            self.match(vhdlParser.ACCESS)
            self.state = 511
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Across_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def ACROSS(self):
            return self.getToken(vhdlParser.ACROSS, 0)

        def tolerance_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Tolerance_aspectContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_across_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAcross_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAcross_aspect(self)




    def across_aspect(self):

        localctx = vhdlParser.Across_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_across_aspect)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 513
            self.identifier_list()
            self.state = 515
            _la = self._input.LA(1)
            if _la == vhdlParser.TOLERANCE:
                self.state = 514
                self.tolerance_aspect()


            self.state = 519
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 517
                self.match(vhdlParser.VARASGN)
                self.state = 518
                self.expression()


            self.state = 521
            self.match(vhdlParser.ACROSS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_designatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def OPEN(self):
            return self.getToken(vhdlParser.OPEN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_actual_designator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterActual_designator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitActual_designator(self)




    def actual_designator(self):

        localctx = vhdlParser.Actual_designatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_actual_designator)
        try:
            self.state = 525
            token = self._input.LA(1)
            if token in [vhdlParser.ABS, vhdlParser.NEW, vhdlParser.NOT, vhdlParser.NULL, vhdlParser.BASE_LITERAL, vhdlParser.BIT_STRING_LITERAL, vhdlParser.REAL_LITERAL, vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.CHARACTER_LITERAL, vhdlParser.STRING_LITERAL, vhdlParser.LPAREN, vhdlParser.PLUS, vhdlParser.MINUS, vhdlParser.INTEGER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 523
                self.expression()

            elif token == vhdlParser.OPEN:
                self.enterOuterAlt(localctx, 2)
                self.state = 524
                self.match(vhdlParser.OPEN)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_parameter_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def association_list(self):
            return self.getTypedRuleContext(vhdlParser.Association_listContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_actual_parameter_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterActual_parameter_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitActual_parameter_part(self)




    def actual_parameter_part(self):

        localctx = vhdlParser.Actual_parameter_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_actual_parameter_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 527
            self.association_list()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def actual_designator(self):
            return self.getTypedRuleContext(vhdlParser.Actual_designatorContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_actual_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterActual_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitActual_part(self)




    def actual_part(self):

        localctx = vhdlParser.Actual_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_actual_part)
        try:
            self.state = 535
            la_ = self._interp.adaptivePredict(self._input, 3, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 529
                self.name()
                self.state = 530
                self.match(vhdlParser.LPAREN)
                self.state = 531
                self.actual_designator()
                self.state = 532
                self.match(vhdlParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 534
                self.actual_designator()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Adding_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(vhdlParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(vhdlParser.MINUS, 0)

        def AMPERSAND(self):
            return self.getToken(vhdlParser.AMPERSAND, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_adding_operator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAdding_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAdding_operator(self)




    def adding_operator(self):

        localctx = vhdlParser.Adding_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_adding_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 537
            _la = self._input.LA(1)
            if not(((((_la - 140)) & ~0x3f) == 0 and ((1 << (_la - 140)) & ((1 << (vhdlParser.AMPERSAND - 140)) | (1 << (vhdlParser.PLUS - 140)) | (1 << (vhdlParser.MINUS - 140)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AggregateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def element_association(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Element_associationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Element_associationContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_aggregate

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAggregate(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAggregate(self)




    def aggregate(self):

        localctx = vhdlParser.AggregateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_aggregate)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 539
            self.match(vhdlParser.LPAREN)
            self.state = 540
            self.element_association()
            self.state = 545
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 541
                self.match(vhdlParser.COMMA)
                self.state = 542
                self.element_association()
                self.state = 547
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 548
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Alias_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ALIAS(self):
            return self.getToken(vhdlParser.ALIAS, 0)

        def alias_designator(self):
            return self.getTypedRuleContext(vhdlParser.Alias_designatorContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def alias_indication(self):
            return self.getTypedRuleContext(vhdlParser.Alias_indicationContext, 0)


        def signature(self):
            return self.getTypedRuleContext(vhdlParser.SignatureContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_alias_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAlias_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAlias_declaration(self)




    def alias_declaration(self):

        localctx = vhdlParser.Alias_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_alias_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 550
            self.match(vhdlParser.ALIAS)
            self.state = 551
            self.alias_designator()
            self.state = 554
            _la = self._input.LA(1)
            if _la == vhdlParser.COLON:
                self.state = 552
                self.match(vhdlParser.COLON)
                self.state = 553
                self.alias_indication()


            self.state = 556
            self.match(vhdlParser.IS)
            self.state = 557
            self.name()
            self.state = 559
            _la = self._input.LA(1)
            if _la == vhdlParser.LBRACKET:
                self.state = 558
                self.signature()


            self.state = 561
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Alias_designatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def CHARACTER_LITERAL(self):
            return self.getToken(vhdlParser.CHARACTER_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(vhdlParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_alias_designator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAlias_designator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAlias_designator(self)




    def alias_designator(self):

        localctx = vhdlParser.Alias_designatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_alias_designator)
        try:
            self.state = 566
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 563
                self.identifier()

            elif token == vhdlParser.CHARACTER_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 564
                self.match(vhdlParser.CHARACTER_LITERAL)

            elif token == vhdlParser.STRING_LITERAL:
                self.enterOuterAlt(localctx, 3)
                self.state = 565
                self.match(vhdlParser.STRING_LITERAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Alias_indicationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_alias_indication

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAlias_indication(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAlias_indication(self)




    def alias_indication(self):

        localctx = vhdlParser.Alias_indicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_alias_indication)
        try:
            self.state = 570
            la_ = self._interp.adaptivePredict(self._input, 8, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 568
                self.subnature_indication()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 569
                self.subtype_indication()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AllocatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEW(self):
            return self.getToken(vhdlParser.NEW, 0)

        def qualified_expression(self):
            return self.getTypedRuleContext(vhdlParser.Qualified_expressionContext, 0)


        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_allocator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAllocator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAllocator(self)




    def allocator(self):

        localctx = vhdlParser.AllocatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_allocator)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 572
            self.match(vhdlParser.NEW)
            self.state = 575
            la_ = self._interp.adaptivePredict(self._input, 9, self._ctx)
            if la_ == 1:
                self.state = 573
                self.qualified_expression()
                pass

            elif la_ == 2:
                self.state = 574
                self.subtype_indication()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Architecture_bodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARCHITECTURE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.ARCHITECTURE)
            else:
                return self.getToken(vhdlParser.ARCHITECTURE, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def architecture_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Architecture_declarative_partContext, 0)


        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def architecture_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Architecture_statement_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_architecture_body

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArchitecture_body(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArchitecture_body(self)




    def architecture_body(self):

        localctx = vhdlParser.Architecture_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_architecture_body)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 577
            self.match(vhdlParser.ARCHITECTURE)
            self.state = 578
            self.identifier()
            self.state = 579
            self.match(vhdlParser.OF)
            self.state = 580
            self.identifier()
            self.state = 581
            self.match(vhdlParser.IS)
            self.state = 582
            self.architecture_declarative_part()
            self.state = 583
            self.match(vhdlParser.BEGIN)
            self.state = 584
            self.architecture_statement_part()
            self.state = 585
            self.match(vhdlParser.END)
            self.state = 587
            _la = self._input.LA(1)
            if _la == vhdlParser.ARCHITECTURE:
                self.state = 586
                self.match(vhdlParser.ARCHITECTURE)


            self.state = 590
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 589
                self.identifier()


            self.state = 592
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Architecture_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Block_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Block_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_architecture_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArchitecture_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArchitecture_declarative_part(self)




    def architecture_declarative_part(self):

        localctx = vhdlParser.Architecture_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_architecture_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 597
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FOR) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.LIMIT) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.QUANTITY - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 594
                self.block_declarative_item()
                self.state = 599
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Architecture_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block_statement(self):
            return self.getTypedRuleContext(vhdlParser.Block_statementContext, 0)


        def process_statement(self):
            return self.getTypedRuleContext(vhdlParser.Process_statementContext, 0)


        def concurrent_procedure_call_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_procedure_call_statementContext, 0)


        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def concurrent_assertion_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_assertion_statementContext, 0)


        def concurrent_signal_assignment_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_signal_assignment_statementContext, 0)


        def POSTPONED(self):
            return self.getToken(vhdlParser.POSTPONED, 0)

        def component_instantiation_statement(self):
            return self.getTypedRuleContext(vhdlParser.Component_instantiation_statementContext, 0)


        def generate_statement(self):
            return self.getTypedRuleContext(vhdlParser.Generate_statementContext, 0)


        def concurrent_break_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_break_statementContext, 0)


        def simultaneous_statement(self):
            return self.getTypedRuleContext(vhdlParser.Simultaneous_statementContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_architecture_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArchitecture_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArchitecture_statement(self)




    def architecture_statement(self):

        localctx = vhdlParser.Architecture_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_architecture_statement)
        try:
            self.state = 621
            la_ = self._interp.adaptivePredict(self._input, 17, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 600
                self.block_statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 601
                self.process_statement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 603
                la_ = self._interp.adaptivePredict(self._input, 13, self._ctx)
                if la_ == 1:
                    self.state = 602
                    self.label_colon()


                self.state = 605
                self.concurrent_procedure_call_statement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 607
                la_ = self._interp.adaptivePredict(self._input, 14, self._ctx)
                if la_ == 1:
                    self.state = 606
                    self.label_colon()


                self.state = 609
                self.concurrent_assertion_statement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 611
                la_ = self._interp.adaptivePredict(self._input, 15, self._ctx)
                if la_ == 1:
                    self.state = 610
                    self.label_colon()


                self.state = 614
                la_ = self._interp.adaptivePredict(self._input, 16, self._ctx)
                if la_ == 1:
                    self.state = 613
                    self.match(vhdlParser.POSTPONED)


                self.state = 616
                self.concurrent_signal_assignment_statement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 617
                self.component_instantiation_statement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 618
                self.generate_statement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 619
                self.concurrent_break_statement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 620
                self.simultaneous_statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Architecture_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def architecture_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Architecture_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Architecture_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_architecture_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArchitecture_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArchitecture_statement_part(self)




    def architecture_statement_part(self):

        localctx = vhdlParser.Architecture_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_architecture_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 626
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.IF) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (vhdlParser.POSTPONED - 66)) | (1 << (vhdlParser.PROCESS - 66)) | (1 << (vhdlParser.PROCEDURAL - 66)) | (1 << (vhdlParser.WITH - 66)) | (1 << (vhdlParser.BASE_LITERAL - 66)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 66)) | (1 << (vhdlParser.REAL_LITERAL - 66)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 66)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 66)) | (1 << (vhdlParser.CHARACTER_LITERAL - 66)) | (1 << (vhdlParser.STRING_LITERAL - 66)))) != 0) or ((((_la - 141)) & ~0x3f) == 0 and ((1 << (_la - 141)) & ((1 << (vhdlParser.LPAREN - 141)) | (1 << (vhdlParser.PLUS - 141)) | (1 << (vhdlParser.MINUS - 141)) | (1 << (vhdlParser.INTEGER - 141)))) != 0):
                self.state = 623
                self.architecture_statement()
                self.state = 628
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Array_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unconstrained_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Unconstrained_nature_definitionContext, 0)


        def constrained_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Constrained_nature_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_array_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArray_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArray_nature_definition(self)




    def array_nature_definition(self):

        localctx = vhdlParser.Array_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_array_nature_definition)
        try:
            self.state = 631
            la_ = self._interp.adaptivePredict(self._input, 19, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 629
                self.unconstrained_nature_definition()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 630
                self.constrained_nature_definition()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Array_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unconstrained_array_definition(self):
            return self.getTypedRuleContext(vhdlParser.Unconstrained_array_definitionContext, 0)


        def constrained_array_definition(self):
            return self.getTypedRuleContext(vhdlParser.Constrained_array_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_array_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterArray_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitArray_type_definition(self)




    def array_type_definition(self):

        localctx = vhdlParser.Array_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_array_type_definition)
        try:
            self.state = 635
            la_ = self._interp.adaptivePredict(self._input, 20, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 633
                self.unconstrained_array_definition()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 634
                self.constrained_array_definition()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AssertionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSERT(self):
            return self.getToken(vhdlParser.ASSERT, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def REPORT(self):
            return self.getToken(vhdlParser.REPORT, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ExpressionContext, i)


        def SEVERITY(self):
            return self.getToken(vhdlParser.SEVERITY, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_assertion

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAssertion(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAssertion(self)




    def assertion(self):

        localctx = vhdlParser.AssertionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_assertion)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 637
            self.match(vhdlParser.ASSERT)
            self.state = 638
            self.condition()
            self.state = 641
            _la = self._input.LA(1)
            if _la == vhdlParser.REPORT:
                self.state = 639
                self.match(vhdlParser.REPORT)
                self.state = 640
                self.expression()


            self.state = 645
            _la = self._input.LA(1)
            if _la == vhdlParser.SEVERITY:
                self.state = 643
                self.match(vhdlParser.SEVERITY)
                self.state = 644
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Assertion_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assertion(self):
            return self.getTypedRuleContext(vhdlParser.AssertionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_assertion_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAssertion_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAssertion_statement(self)




    def assertion_statement(self):

        localctx = vhdlParser.Assertion_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_assertion_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 648
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 647
                self.label_colon()


            self.state = 650
            self.assertion()
            self.state = 651
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Association_elementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def actual_part(self):
            return self.getTypedRuleContext(vhdlParser.Actual_partContext, 0)


        def formal_part(self):
            return self.getTypedRuleContext(vhdlParser.Formal_partContext, 0)


        def ARROW(self):
            return self.getToken(vhdlParser.ARROW, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_association_element

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAssociation_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAssociation_element(self)




    def association_element(self):

        localctx = vhdlParser.Association_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_association_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 656
            la_ = self._interp.adaptivePredict(self._input, 24, self._ctx)
            if la_ == 1:
                self.state = 653
                self.formal_part()
                self.state = 654
                self.match(vhdlParser.ARROW)


            self.state = 658
            self.actual_part()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Association_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def association_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Association_elementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Association_elementContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_association_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAssociation_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAssociation_list(self)




    def association_list(self):

        localctx = vhdlParser.Association_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_association_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 660
            self.association_element()
            self.state = 665
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 661
                self.match(vhdlParser.COMMA)
                self.state = 662
                self.association_element()
                self.state = 667
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attribute_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ATTRIBUTE(self):
            return self.getToken(vhdlParser.ATTRIBUTE, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_attribute_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAttribute_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAttribute_declaration(self)




    def attribute_declaration(self):

        localctx = vhdlParser.Attribute_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_attribute_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 668
            self.match(vhdlParser.ATTRIBUTE)
            self.state = 669
            self.label_colon()
            self.state = 670
            self.name()
            self.state = 671
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attribute_designatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def RANGE(self):
            return self.getToken(vhdlParser.RANGE, 0)

        def REVERSE_RANGE(self):
            return self.getToken(vhdlParser.REVERSE_RANGE, 0)

        def ACROSS(self):
            return self.getToken(vhdlParser.ACROSS, 0)

        def THROUGH(self):
            return self.getToken(vhdlParser.THROUGH, 0)

        def REFERENCE(self):
            return self.getToken(vhdlParser.REFERENCE, 0)

        def TOLERANCE(self):
            return self.getToken(vhdlParser.TOLERANCE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_attribute_designator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAttribute_designator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAttribute_designator(self)




    def attribute_designator(self):

        localctx = vhdlParser.Attribute_designatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_attribute_designator)
        try:
            self.state = 680
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 673
                self.identifier()

            elif token == vhdlParser.RANGE:
                self.enterOuterAlt(localctx, 2)
                self.state = 674
                self.match(vhdlParser.RANGE)

            elif token == vhdlParser.REVERSE_RANGE:
                self.enterOuterAlt(localctx, 3)
                self.state = 675
                self.match(vhdlParser.REVERSE_RANGE)

            elif token == vhdlParser.ACROSS:
                self.enterOuterAlt(localctx, 4)
                self.state = 676
                self.match(vhdlParser.ACROSS)

            elif token == vhdlParser.THROUGH:
                self.enterOuterAlt(localctx, 5)
                self.state = 677
                self.match(vhdlParser.THROUGH)

            elif token == vhdlParser.REFERENCE:
                self.enterOuterAlt(localctx, 6)
                self.state = 678
                self.match(vhdlParser.REFERENCE)

            elif token == vhdlParser.TOLERANCE:
                self.enterOuterAlt(localctx, 7)
                self.state = 679
                self.match(vhdlParser.TOLERANCE)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attribute_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ATTRIBUTE(self):
            return self.getToken(vhdlParser.ATTRIBUTE, 0)

        def attribute_designator(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_designatorContext, 0)


        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def entity_specification(self):
            return self.getTypedRuleContext(vhdlParser.Entity_specificationContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_attribute_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterAttribute_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitAttribute_specification(self)




    def attribute_specification(self):

        localctx = vhdlParser.Attribute_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_attribute_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 682
            self.match(vhdlParser.ATTRIBUTE)
            self.state = 683
            self.attribute_designator()
            self.state = 684
            self.match(vhdlParser.OF)
            self.state = 685
            self.entity_specification()
            self.state = 686
            self.match(vhdlParser.IS)
            self.state = 687
            self.expression()
            self.state = 688
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Base_unit_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_base_unit_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBase_unit_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBase_unit_declaration(self)




    def base_unit_declaration(self):

        localctx = vhdlParser.Base_unit_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_base_unit_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 690
            self.identifier()
            self.state = 691
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Binding_indicationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE(self):
            return self.getToken(vhdlParser.USE, 0)

        def entity_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Entity_aspectContext, 0)


        def generic_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Generic_map_aspectContext, 0)


        def port_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Port_map_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_binding_indication

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBinding_indication(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBinding_indication(self)




    def binding_indication(self):

        localctx = vhdlParser.Binding_indicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_binding_indication)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 695
            _la = self._input.LA(1)
            if _la == vhdlParser.USE:
                self.state = 693
                self.match(vhdlParser.USE)
                self.state = 694
                self.entity_aspect()


            self.state = 698
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC:
                self.state = 697
                self.generic_map_aspect()


            self.state = 701
            _la = self._input.LA(1)
            if _la == vhdlParser.PORT:
                self.state = 700
                self.port_map_aspect()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_configurationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.FOR)
            else:
                return self.getToken(vhdlParser.FOR, i)

        def block_specification(self):
            return self.getTypedRuleContext(vhdlParser.Block_specificationContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def use_clause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Use_clauseContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Use_clauseContext, i)


        def configuration_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Configuration_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Configuration_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_configuration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_configuration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_configuration(self)




    def block_configuration(self):

        localctx = vhdlParser.Block_configurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_block_configuration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 703
            self.match(vhdlParser.FOR)
            self.state = 704
            self.block_specification()
            self.state = 708
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.USE:
                self.state = 705
                self.use_clause()
                self.state = 710
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 714
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.FOR:
                self.state = 711
                self.configuration_item()
                self.state = 716
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 717
            self.match(vhdlParser.END)
            self.state = 718
            self.match(vhdlParser.FOR)
            self.state = 719
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def signal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Signal_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def component_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Component_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def configuration_specification(self):
            return self.getTypedRuleContext(vhdlParser.Configuration_specificationContext, 0)


        def disconnection_specification(self):
            return self.getTypedRuleContext(vhdlParser.Disconnection_specificationContext, 0)


        def step_limit_specification(self):
            return self.getTypedRuleContext(vhdlParser.Step_limit_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def nature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Nature_declarationContext, 0)


        def subnature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_declarationContext, 0)


        def quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Quantity_declarationContext, 0)


        def terminal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Terminal_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_declarative_item(self)




    def block_declarative_item(self):

        localctx = vhdlParser.Block_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_block_declarative_item)
        try:
            self.state = 743
            la_ = self._interp.adaptivePredict(self._input, 32, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 721
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 722
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 723
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 724
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 725
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 726
                self.signal_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 727
                self.variable_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 728
                self.file_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 729
                self.alias_declaration()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 730
                self.component_declaration()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 731
                self.attribute_declaration()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 732
                self.attribute_specification()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 733
                self.configuration_specification()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 734
                self.disconnection_specification()
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 735
                self.step_limit_specification()
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 736
                self.use_clause()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 737
                self.group_template_declaration()
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 738
                self.group_declaration()
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 739
                self.nature_declaration()
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 740
                self.subnature_declaration()
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 741
                self.quantity_declaration()
                pass

            elif la_ == 22:
                self.enterOuterAlt(localctx, 22)
                self.state = 742
                self.terminal_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Block_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Block_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_declarative_part(self)




    def block_declarative_part(self):

        localctx = vhdlParser.Block_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_block_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 748
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FOR) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.LIMIT) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.QUANTITY - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 745
                self.block_declarative_item()
                self.state = 750
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_headerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def generic_clause(self):
            return self.getTypedRuleContext(vhdlParser.Generic_clauseContext, 0)


        def port_clause(self):
            return self.getTypedRuleContext(vhdlParser.Port_clauseContext, 0)


        def generic_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Generic_map_aspectContext, 0)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def port_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Port_map_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_header

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_header(self)




    def block_header(self):

        localctx = vhdlParser.Block_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_block_header)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 757
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC:
                self.state = 751
                self.generic_clause()
                self.state = 755
                _la = self._input.LA(1)
                if _la == vhdlParser.GENERIC:
                    self.state = 752
                    self.generic_map_aspect()
                    self.state = 753
                    self.match(vhdlParser.SEMI)




            self.state = 765
            _la = self._input.LA(1)
            if _la == vhdlParser.PORT:
                self.state = 759
                self.port_clause()
                self.state = 763
                _la = self._input.LA(1)
                if _la == vhdlParser.PORT:
                    self.state = 760
                    self.port_map_aspect()
                    self.state = 761
                    self.match(vhdlParser.SEMI)




        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def index_specification(self):
            return self.getTypedRuleContext(vhdlParser.Index_specificationContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_specification(self)




    def block_specification(self):

        localctx = vhdlParser.Block_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_block_specification)
        self._la = 0  # Token type
        try:
            self.state = 775
            la_ = self._interp.adaptivePredict(self._input, 39, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 767
                self.identifier()
                self.state = 772
                _la = self._input.LA(1)
                if _la == vhdlParser.LPAREN:
                    self.state = 768
                    self.match(vhdlParser.LPAREN)
                    self.state = 769
                    self.index_specification()
                    self.state = 770
                    self.match(vhdlParser.RPAREN)


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 774
                self.name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def BLOCK(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.BLOCK)
            else:
                return self.getToken(vhdlParser.BLOCK, i)

        def block_header(self):
            return self.getTypedRuleContext(vhdlParser.Block_headerContext, 0)


        def block_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Block_declarative_partContext, 0)


        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def block_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Block_statement_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_statement(self)




    def block_statement(self):

        localctx = vhdlParser.Block_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_block_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 777
            self.label_colon()
            self.state = 778
            self.match(vhdlParser.BLOCK)
            self.state = 783
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 779
                self.match(vhdlParser.LPAREN)
                self.state = 780
                self.expression()
                self.state = 781
                self.match(vhdlParser.RPAREN)


            self.state = 786
            _la = self._input.LA(1)
            if _la == vhdlParser.IS:
                self.state = 785
                self.match(vhdlParser.IS)


            self.state = 788
            self.block_header()
            self.state = 789
            self.block_declarative_part()
            self.state = 790
            self.match(vhdlParser.BEGIN)
            self.state = 791
            self.block_statement_part()
            self.state = 792
            self.match(vhdlParser.END)
            self.state = 793
            self.match(vhdlParser.BLOCK)
            self.state = 795
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 794
                self.identifier()


            self.state = 797
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def architecture_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Architecture_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Architecture_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_block_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBlock_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBlock_statement_part(self)




    def block_statement_part(self):

        localctx = vhdlParser.Block_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_block_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 802
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.IF) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (vhdlParser.POSTPONED - 66)) | (1 << (vhdlParser.PROCESS - 66)) | (1 << (vhdlParser.PROCEDURAL - 66)) | (1 << (vhdlParser.WITH - 66)) | (1 << (vhdlParser.BASE_LITERAL - 66)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 66)) | (1 << (vhdlParser.REAL_LITERAL - 66)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 66)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 66)) | (1 << (vhdlParser.CHARACTER_LITERAL - 66)) | (1 << (vhdlParser.STRING_LITERAL - 66)))) != 0) or ((((_la - 141)) & ~0x3f) == 0 and ((1 << (_la - 141)) & ((1 << (vhdlParser.LPAREN - 141)) | (1 << (vhdlParser.PLUS - 141)) | (1 << (vhdlParser.MINUS - 141)) | (1 << (vhdlParser.INTEGER - 141)))) != 0):
                self.state = 799
                self.architecture_statement()
                self.state = 804
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Branch_quantity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUANTITY(self):
            return self.getToken(vhdlParser.QUANTITY, 0)

        def terminal_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Terminal_aspectContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def across_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Across_aspectContext, 0)


        def through_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Through_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_branch_quantity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBranch_quantity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBranch_quantity_declaration(self)




    def branch_quantity_declaration(self):

        localctx = vhdlParser.Branch_quantity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_branch_quantity_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 805
            self.match(vhdlParser.QUANTITY)
            self.state = 807
            la_ = self._interp.adaptivePredict(self._input, 44, self._ctx)
            if la_ == 1:
                self.state = 806
                self.across_aspect()


            self.state = 810
            la_ = self._interp.adaptivePredict(self._input, 45, self._ctx)
            if la_ == 1:
                self.state = 809
                self.through_aspect()


            self.state = 812
            self.terminal_aspect()
            self.state = 813
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Break_elementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def ARROW(self):
            return self.getToken(vhdlParser.ARROW, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def break_selector_clause(self):
            return self.getTypedRuleContext(vhdlParser.Break_selector_clauseContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_break_element

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBreak_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBreak_element(self)




    def break_element(self):

        localctx = vhdlParser.Break_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_break_element)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 816
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR:
                self.state = 815
                self.break_selector_clause()


            self.state = 818
            self.name()
            self.state = 819
            self.match(vhdlParser.ARROW)
            self.state = 820
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Break_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def break_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Break_elementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Break_elementContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_break_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBreak_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBreak_list(self)




    def break_list(self):

        localctx = vhdlParser.Break_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_break_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 822
            self.break_element()
            self.state = 827
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 823
                self.match(vhdlParser.COMMA)
                self.state = 824
                self.break_element()
                self.state = 829
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Break_selector_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(vhdlParser.FOR, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def USE(self):
            return self.getToken(vhdlParser.USE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_break_selector_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBreak_selector_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBreak_selector_clause(self)




    def break_selector_clause(self):

        localctx = vhdlParser.Break_selector_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_break_selector_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 830
            self.match(vhdlParser.FOR)
            self.state = 831
            self.name()
            self.state = 832
            self.match(vhdlParser.USE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Break_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(vhdlParser.BREAK, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def break_list(self):
            return self.getTypedRuleContext(vhdlParser.Break_listContext, 0)


        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_break_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterBreak_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitBreak_statement(self)




    def break_statement(self):

        localctx = vhdlParser.Break_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_break_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 835
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 834
                self.label_colon()


            self.state = 837
            self.match(vhdlParser.BREAK)
            self.state = 839
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR or _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 838
                self.break_list()


            self.state = 843
            _la = self._input.LA(1)
            if _la == vhdlParser.WHEN:
                self.state = 841
                self.match(vhdlParser.WHEN)
                self.state = 842
                self.condition()


            self.state = 845
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Case_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CASE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.CASE)
            else:
                return self.getToken(vhdlParser.CASE, i)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def case_statement_alternative(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Case_statement_alternativeContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Case_statement_alternativeContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_case_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterCase_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitCase_statement(self)




    def case_statement(self):

        localctx = vhdlParser.Case_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_case_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 848
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 847
                self.label_colon()


            self.state = 850
            self.match(vhdlParser.CASE)
            self.state = 851
            self.expression()
            self.state = 852
            self.match(vhdlParser.IS)
            self.state = 854 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 853
                self.case_statement_alternative()
                self.state = 856 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la == vhdlParser.WHEN):
                    break

            self.state = 858
            self.match(vhdlParser.END)
            self.state = 859
            self.match(vhdlParser.CASE)
            self.state = 861
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 860
                self.identifier()


            self.state = 863
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Case_statement_alternativeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def choices(self):
            return self.getTypedRuleContext(vhdlParser.ChoicesContext, 0)


        def ARROW(self):
            return self.getToken(vhdlParser.ARROW, 0)

        def sequence_of_statements(self):
            return self.getTypedRuleContext(vhdlParser.Sequence_of_statementsContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_case_statement_alternative

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterCase_statement_alternative(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitCase_statement_alternative(self)




    def case_statement_alternative(self):

        localctx = vhdlParser.Case_statement_alternativeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_case_statement_alternative)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 865
            self.match(vhdlParser.WHEN)
            self.state = 866
            self.choices()
            self.state = 867
            self.match(vhdlParser.ARROW)
            self.state = 868
            self.sequence_of_statements()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ChoiceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def discrete_range(self):
            return self.getTypedRuleContext(vhdlParser.Discrete_rangeContext, 0)


        def simple_expression(self):
            return self.getTypedRuleContext(vhdlParser.Simple_expressionContext, 0)


        def OTHERS(self):
            return self.getToken(vhdlParser.OTHERS, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_choice

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterChoice(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitChoice(self)




    def choice(self):

        localctx = vhdlParser.ChoiceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_choice)
        try:
            self.state = 874
            la_ = self._interp.adaptivePredict(self._input, 54, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 870
                self.identifier()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 871
                self.discrete_range()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 872
                self.simple_expression()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 873
                self.match(vhdlParser.OTHERS)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ChoicesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def choice(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ChoiceContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ChoiceContext, i)


        def BAR(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.BAR)
            else:
                return self.getToken(vhdlParser.BAR, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_choices

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterChoices(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitChoices(self)




    def choices(self):

        localctx = vhdlParser.ChoicesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_choices)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 876
            self.choice()
            self.state = 881
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.BAR:
                self.state = 877
                self.match(vhdlParser.BAR)
                self.state = 878
                self.choice()
                self.state = 883
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Component_configurationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.FOR)
            else:
                return self.getToken(vhdlParser.FOR, i)

        def component_specification(self):
            return self.getTypedRuleContext(vhdlParser.Component_specificationContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def binding_indication(self):
            return self.getTypedRuleContext(vhdlParser.Binding_indicationContext, 0)


        def block_configuration(self):
            return self.getTypedRuleContext(vhdlParser.Block_configurationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_component_configuration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComponent_configuration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComponent_configuration(self)




    def component_configuration(self):

        localctx = vhdlParser.Component_configurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_component_configuration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 884
            self.match(vhdlParser.FOR)
            self.state = 885
            self.component_specification()
            self.state = 889
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC or _la == vhdlParser.PORT or _la == vhdlParser.USE or _la == vhdlParser.SEMI:
                self.state = 886
                self.binding_indication()
                self.state = 887
                self.match(vhdlParser.SEMI)


            self.state = 892
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR:
                self.state = 891
                self.block_configuration()


            self.state = 894
            self.match(vhdlParser.END)
            self.state = 895
            self.match(vhdlParser.FOR)
            self.state = 896
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Component_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMPONENT(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMPONENT)
            else:
                return self.getToken(vhdlParser.COMPONENT, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def generic_clause(self):
            return self.getTypedRuleContext(vhdlParser.Generic_clauseContext, 0)


        def port_clause(self):
            return self.getTypedRuleContext(vhdlParser.Port_clauseContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_component_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComponent_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComponent_declaration(self)




    def component_declaration(self):

        localctx = vhdlParser.Component_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_component_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 898
            self.match(vhdlParser.COMPONENT)
            self.state = 899
            self.identifier()
            self.state = 901
            _la = self._input.LA(1)
            if _la == vhdlParser.IS:
                self.state = 900
                self.match(vhdlParser.IS)


            self.state = 904
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC:
                self.state = 903
                self.generic_clause()


            self.state = 907
            _la = self._input.LA(1)
            if _la == vhdlParser.PORT:
                self.state = 906
                self.port_clause()


            self.state = 909
            self.match(vhdlParser.END)
            self.state = 910
            self.match(vhdlParser.COMPONENT)
            self.state = 912
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 911
                self.identifier()


            self.state = 914
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Component_instantiation_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def instantiated_unit(self):
            return self.getTypedRuleContext(vhdlParser.Instantiated_unitContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def generic_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Generic_map_aspectContext, 0)


        def port_map_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Port_map_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_component_instantiation_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComponent_instantiation_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComponent_instantiation_statement(self)




    def component_instantiation_statement(self):

        localctx = vhdlParser.Component_instantiation_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_component_instantiation_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 916
            self.label_colon()
            self.state = 917
            self.instantiated_unit()
            self.state = 919
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC:
                self.state = 918
                self.generic_map_aspect()


            self.state = 922
            _la = self._input.LA(1)
            if _la == vhdlParser.PORT:
                self.state = 921
                self.port_map_aspect()


            self.state = 924
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Component_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def instantiation_list(self):
            return self.getTypedRuleContext(vhdlParser.Instantiation_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_component_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComponent_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComponent_specification(self)




    def component_specification(self):

        localctx = vhdlParser.Component_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_component_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 926
            self.instantiation_list()
            self.state = 927
            self.match(vhdlParser.COLON)
            self.state = 928
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Composite_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def array_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Array_nature_definitionContext, 0)


        def record_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Record_nature_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_composite_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComposite_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComposite_nature_definition(self)




    def composite_nature_definition(self):

        localctx = vhdlParser.Composite_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_composite_nature_definition)
        try:
            self.state = 932
            token = self._input.LA(1)
            if token == vhdlParser.ARRAY:
                self.enterOuterAlt(localctx, 1)
                self.state = 930
                self.array_nature_definition()

            elif token == vhdlParser.RECORD:
                self.enterOuterAlt(localctx, 2)
                self.state = 931
                self.record_nature_definition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Composite_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def array_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Array_type_definitionContext, 0)


        def record_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Record_type_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_composite_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterComposite_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitComposite_type_definition(self)




    def composite_type_definition(self):

        localctx = vhdlParser.Composite_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_composite_type_definition)
        try:
            self.state = 936
            token = self._input.LA(1)
            if token == vhdlParser.ARRAY:
                self.enterOuterAlt(localctx, 1)
                self.state = 934
                self.array_type_definition()

            elif token == vhdlParser.RECORD:
                self.enterOuterAlt(localctx, 2)
                self.state = 935
                self.record_type_definition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Concurrent_assertion_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assertion(self):
            return self.getTypedRuleContext(vhdlParser.AssertionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def POSTPONED(self):
            return self.getToken(vhdlParser.POSTPONED, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_concurrent_assertion_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConcurrent_assertion_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConcurrent_assertion_statement(self)




    def concurrent_assertion_statement(self):

        localctx = vhdlParser.Concurrent_assertion_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_concurrent_assertion_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 939
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 938
                self.label_colon()


            self.state = 942
            _la = self._input.LA(1)
            if _la == vhdlParser.POSTPONED:
                self.state = 941
                self.match(vhdlParser.POSTPONED)


            self.state = 944
            self.assertion()
            self.state = 945
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Concurrent_break_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(vhdlParser.BREAK, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def break_list(self):
            return self.getTypedRuleContext(vhdlParser.Break_listContext, 0)


        def sensitivity_clause(self):
            return self.getTypedRuleContext(vhdlParser.Sensitivity_clauseContext, 0)


        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_concurrent_break_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConcurrent_break_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConcurrent_break_statement(self)




    def concurrent_break_statement(self):

        localctx = vhdlParser.Concurrent_break_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_concurrent_break_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 948
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 947
                self.label_colon()


            self.state = 950
            self.match(vhdlParser.BREAK)
            self.state = 952
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR or _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 951
                self.break_list()


            self.state = 955
            _la = self._input.LA(1)
            if _la == vhdlParser.ON:
                self.state = 954
                self.sensitivity_clause()


            self.state = 959
            _la = self._input.LA(1)
            if _la == vhdlParser.WHEN:
                self.state = 957
                self.match(vhdlParser.WHEN)
                self.state = 958
                self.condition()


            self.state = 961
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Concurrent_procedure_call_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procedure_call(self):
            return self.getTypedRuleContext(vhdlParser.Procedure_callContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def POSTPONED(self):
            return self.getToken(vhdlParser.POSTPONED, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_concurrent_procedure_call_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConcurrent_procedure_call_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConcurrent_procedure_call_statement(self)




    def concurrent_procedure_call_statement(self):

        localctx = vhdlParser.Concurrent_procedure_call_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_concurrent_procedure_call_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 964
            la_ = self._interp.adaptivePredict(self._input, 72, self._ctx)
            if la_ == 1:
                self.state = 963
                self.label_colon()


            self.state = 967
            _la = self._input.LA(1)
            if _la == vhdlParser.POSTPONED:
                self.state = 966
                self.match(vhdlParser.POSTPONED)


            self.state = 969
            self.procedure_call()
            self.state = 970
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Concurrent_signal_assignment_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conditional_signal_assignment(self):
            return self.getTypedRuleContext(vhdlParser.Conditional_signal_assignmentContext, 0)


        def selected_signal_assignment(self):
            return self.getTypedRuleContext(vhdlParser.Selected_signal_assignmentContext, 0)


        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def POSTPONED(self):
            return self.getToken(vhdlParser.POSTPONED, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_concurrent_signal_assignment_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConcurrent_signal_assignment_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConcurrent_signal_assignment_statement(self)




    def concurrent_signal_assignment_statement(self):

        localctx = vhdlParser.Concurrent_signal_assignment_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_concurrent_signal_assignment_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 973
            la_ = self._interp.adaptivePredict(self._input, 74, self._ctx)
            if la_ == 1:
                self.state = 972
                self.label_colon()


            self.state = 976
            _la = self._input.LA(1)
            if _la == vhdlParser.POSTPONED:
                self.state = 975
                self.match(vhdlParser.POSTPONED)


            self.state = 980
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.LPAREN]:
                self.state = 978
                self.conditional_signal_assignment()

            elif token == vhdlParser.WITH:
                self.state = 979
                self.selected_signal_assignment()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConditionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitCondition(self)




    def condition(self):

        localctx = vhdlParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 982
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Condition_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UNTIL(self):
            return self.getToken(vhdlParser.UNTIL, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_condition_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterCondition_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitCondition_clause(self)




    def condition_clause(self):

        localctx = vhdlParser.Condition_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_condition_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 984
            self.match(vhdlParser.UNTIL)
            self.state = 985
            self.condition()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Conditional_signal_assignmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(vhdlParser.TargetContext, 0)


        def LE(self):
            return self.getToken(vhdlParser.LE, 0)

        def opts(self):
            return self.getTypedRuleContext(vhdlParser.OptsContext, 0)


        def conditional_waveforms(self):
            return self.getTypedRuleContext(vhdlParser.Conditional_waveformsContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_conditional_signal_assignment

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConditional_signal_assignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConditional_signal_assignment(self)




    def conditional_signal_assignment(self):

        localctx = vhdlParser.Conditional_signal_assignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_conditional_signal_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 987
            self.target()
            self.state = 988
            self.match(vhdlParser.LE)
            self.state = 989
            self.opts()
            self.state = 990
            self.conditional_waveforms()
            self.state = 991
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Conditional_waveformsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def waveform(self):
            return self.getTypedRuleContext(vhdlParser.WaveformContext, 0)


        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def ELSE(self):
            return self.getToken(vhdlParser.ELSE, 0)

        def conditional_waveforms(self):
            return self.getTypedRuleContext(vhdlParser.Conditional_waveformsContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_conditional_waveforms

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConditional_waveforms(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConditional_waveforms(self)




    def conditional_waveforms(self):

        localctx = vhdlParser.Conditional_waveformsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_conditional_waveforms)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 993
            self.waveform()
            self.state = 1000
            _la = self._input.LA(1)
            if _la == vhdlParser.WHEN:
                self.state = 994
                self.match(vhdlParser.WHEN)
                self.state = 995
                self.condition()
                self.state = 998
                _la = self._input.LA(1)
                if _la == vhdlParser.ELSE:
                    self.state = 996
                    self.match(vhdlParser.ELSE)
                    self.state = 997
                    self.conditional_waveforms()




        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Configuration_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONFIGURATION(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.CONFIGURATION)
            else:
                return self.getToken(vhdlParser.CONFIGURATION, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def configuration_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Configuration_declarative_partContext, 0)


        def block_configuration(self):
            return self.getTypedRuleContext(vhdlParser.Block_configurationContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_configuration_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConfiguration_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConfiguration_declaration(self)




    def configuration_declaration(self):

        localctx = vhdlParser.Configuration_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 114, self.RULE_configuration_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1002
            self.match(vhdlParser.CONFIGURATION)
            self.state = 1003
            self.identifier()
            self.state = 1004
            self.match(vhdlParser.OF)
            self.state = 1005
            self.name()
            self.state = 1006
            self.match(vhdlParser.IS)
            self.state = 1007
            self.configuration_declarative_part()
            self.state = 1008
            self.block_configuration()
            self.state = 1009
            self.match(vhdlParser.END)
            self.state = 1011
            _la = self._input.LA(1)
            if _la == vhdlParser.CONFIGURATION:
                self.state = 1010
                self.match(vhdlParser.CONFIGURATION)


            self.state = 1014
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1013
                self.identifier()


            self.state = 1016
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Configuration_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_configuration_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConfiguration_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConfiguration_declarative_item(self)




    def configuration_declarative_item(self):

        localctx = vhdlParser.Configuration_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 116, self.RULE_configuration_declarative_item)
        try:
            self.state = 1021
            token = self._input.LA(1)
            if token == vhdlParser.USE:
                self.enterOuterAlt(localctx, 1)
                self.state = 1018
                self.use_clause()

            elif token == vhdlParser.ATTRIBUTE:
                self.enterOuterAlt(localctx, 2)
                self.state = 1019
                self.attribute_specification()

            elif token == vhdlParser.GROUP:
                self.enterOuterAlt(localctx, 3)
                self.state = 1020
                self.group_declaration()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Configuration_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def configuration_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Configuration_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Configuration_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_configuration_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConfiguration_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConfiguration_declarative_part(self)




    def configuration_declarative_part(self):

        localctx = vhdlParser.Configuration_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 118, self.RULE_configuration_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1026
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.ATTRIBUTE or _la == vhdlParser.GROUP or _la == vhdlParser.USE:
                self.state = 1023
                self.configuration_declarative_item()
                self.state = 1028
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Configuration_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block_configuration(self):
            return self.getTypedRuleContext(vhdlParser.Block_configurationContext, 0)


        def component_configuration(self):
            return self.getTypedRuleContext(vhdlParser.Component_configurationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_configuration_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConfiguration_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConfiguration_item(self)




    def configuration_item(self):

        localctx = vhdlParser.Configuration_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 120, self.RULE_configuration_item)
        try:
            self.state = 1031
            la_ = self._interp.adaptivePredict(self._input, 83, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1029
                self.block_configuration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1030
                self.component_configuration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Configuration_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(vhdlParser.FOR, 0)

        def component_specification(self):
            return self.getTypedRuleContext(vhdlParser.Component_specificationContext, 0)


        def binding_indication(self):
            return self.getTypedRuleContext(vhdlParser.Binding_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_configuration_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConfiguration_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConfiguration_specification(self)




    def configuration_specification(self):

        localctx = vhdlParser.Configuration_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 122, self.RULE_configuration_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1033
            self.match(vhdlParser.FOR)
            self.state = 1034
            self.component_specification()
            self.state = 1035
            self.binding_indication()
            self.state = 1036
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Constant_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONSTANT(self):
            return self.getToken(vhdlParser.CONSTANT, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_constant_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConstant_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConstant_declaration(self)




    def constant_declaration(self):

        localctx = vhdlParser.Constant_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 124, self.RULE_constant_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1038
            self.match(vhdlParser.CONSTANT)
            self.state = 1039
            self.identifier_list()
            self.state = 1040
            self.match(vhdlParser.COLON)
            self.state = 1041
            self.subtype_indication()
            self.state = 1044
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1042
                self.match(vhdlParser.VARASGN)
                self.state = 1043
                self.expression()


            self.state = 1046
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Constrained_array_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARRAY(self):
            return self.getToken(vhdlParser.ARRAY, 0)

        def index_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Index_constraintContext, 0)


        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_constrained_array_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConstrained_array_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConstrained_array_definition(self)




    def constrained_array_definition(self):

        localctx = vhdlParser.Constrained_array_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 126, self.RULE_constrained_array_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1048
            self.match(vhdlParser.ARRAY)
            self.state = 1049
            self.index_constraint()
            self.state = 1050
            self.match(vhdlParser.OF)
            self.state = 1051
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Constrained_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARRAY(self):
            return self.getToken(vhdlParser.ARRAY, 0)

        def index_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Index_constraintContext, 0)


        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_constrained_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConstrained_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConstrained_nature_definition(self)




    def constrained_nature_definition(self):

        localctx = vhdlParser.Constrained_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 128, self.RULE_constrained_nature_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1053
            self.match(vhdlParser.ARRAY)
            self.state = 1054
            self.index_constraint()
            self.state = 1055
            self.match(vhdlParser.OF)
            self.state = 1056
            self.subnature_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConstraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def range_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Range_constraintContext, 0)


        def index_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Index_constraintContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_constraint

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterConstraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitConstraint(self)




    def constraint(self):

        localctx = vhdlParser.ConstraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 130, self.RULE_constraint)
        try:
            self.state = 1060
            token = self._input.LA(1)
            if token == vhdlParser.RANGE:
                self.enterOuterAlt(localctx, 1)
                self.state = 1058
                self.range_constraint()

            elif token == vhdlParser.LPAREN:
                self.enterOuterAlt(localctx, 2)
                self.state = 1059
                self.index_constraint()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Context_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def context_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Context_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Context_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_context_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterContext_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitContext_clause(self)




    def context_clause(self):

        localctx = vhdlParser.Context_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 132, self.RULE_context_clause)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1065
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.LIBRARY or _la == vhdlParser.USE:
                self.state = 1062
                self.context_item()
                self.state = 1067
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Context_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def library_clause(self):
            return self.getTypedRuleContext(vhdlParser.Library_clauseContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_context_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterContext_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitContext_item(self)




    def context_item(self):

        localctx = vhdlParser.Context_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 134, self.RULE_context_item)
        try:
            self.state = 1070
            token = self._input.LA(1)
            if token == vhdlParser.LIBRARY:
                self.enterOuterAlt(localctx, 1)
                self.state = 1068
                self.library_clause()

            elif token == vhdlParser.USE:
                self.enterOuterAlt(localctx, 2)
                self.state = 1069
                self.use_clause()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Delay_mechanismContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRANSPORT(self):
            return self.getToken(vhdlParser.TRANSPORT, 0)

        def INERTIAL(self):
            return self.getToken(vhdlParser.INERTIAL, 0)

        def REJECT(self):
            return self.getToken(vhdlParser.REJECT, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_delay_mechanism

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDelay_mechanism(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDelay_mechanism(self)




    def delay_mechanism(self):

        localctx = vhdlParser.Delay_mechanismContext(self, self._ctx, self.state)
        self.enterRule(localctx, 136, self.RULE_delay_mechanism)
        self._la = 0  # Token type
        try:
            self.state = 1078
            token = self._input.LA(1)
            if token == vhdlParser.TRANSPORT:
                self.enterOuterAlt(localctx, 1)
                self.state = 1072
                self.match(vhdlParser.TRANSPORT)

            elif token in [vhdlParser.INERTIAL, vhdlParser.REJECT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 1075
                _la = self._input.LA(1)
                if _la == vhdlParser.REJECT:
                    self.state = 1073
                    self.match(vhdlParser.REJECT)
                    self.state = 1074
                    self.expression()


                self.state = 1077
                self.match(vhdlParser.INERTIAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Design_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(vhdlParser.EOF, 0)

        def design_unit(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Design_unitContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Design_unitContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_design_file

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDesign_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDesign_file(self)




    def design_file(self):

        localctx = vhdlParser.Design_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 138, self.RULE_design_file)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1083
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ARCHITECTURE) | (1 << vhdlParser.CONFIGURATION) | (1 << vhdlParser.ENTITY) | (1 << vhdlParser.LIBRARY))) != 0) or _la == vhdlParser.PACKAGE or _la == vhdlParser.USE:
                self.state = 1080
                self.design_unit()
                self.state = 1085
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1086
            self.match(vhdlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Design_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def context_clause(self):
            return self.getTypedRuleContext(vhdlParser.Context_clauseContext, 0)


        def library_unit(self):
            return self.getTypedRuleContext(vhdlParser.Library_unitContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_design_unit

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDesign_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDesign_unit(self)




    def design_unit(self):

        localctx = vhdlParser.Design_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 140, self.RULE_design_unit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1088
            self.context_clause()
            self.state = 1089
            self.library_unit()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DesignatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def STRING_LITERAL(self):
            return self.getToken(vhdlParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_designator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDesignator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDesignator(self)




    def designator(self):

        localctx = vhdlParser.DesignatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 142, self.RULE_designator)
        try:
            self.state = 1093
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1091
                self.identifier()

            elif token == vhdlParser.STRING_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 1092
                self.match(vhdlParser.STRING_LITERAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DirectionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TO(self):
            return self.getToken(vhdlParser.TO, 0)

        def DOWNTO(self):
            return self.getToken(vhdlParser.DOWNTO, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_direction

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDirection(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDirection(self)




    def direction(self):

        localctx = vhdlParser.DirectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 144, self.RULE_direction)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1095
            _la = self._input.LA(1)
            if not(_la == vhdlParser.DOWNTO or _la == vhdlParser.TO):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Disconnection_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DISCONNECT(self):
            return self.getToken(vhdlParser.DISCONNECT, 0)

        def guarded_signal_specification(self):
            return self.getTypedRuleContext(vhdlParser.Guarded_signal_specificationContext, 0)


        def AFTER(self):
            return self.getToken(vhdlParser.AFTER, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_disconnection_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDisconnection_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDisconnection_specification(self)




    def disconnection_specification(self):

        localctx = vhdlParser.Disconnection_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 146, self.RULE_disconnection_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1097
            self.match(vhdlParser.DISCONNECT)
            self.state = 1098
            self.guarded_signal_specification()
            self.state = 1099
            self.match(vhdlParser.AFTER)
            self.state = 1100
            self.expression()
            self.state = 1101
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Discrete_rangeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def range(self):
            return self.getTypedRuleContext(vhdlParser.RangeContext, 0)


        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_discrete_range

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterDiscrete_range(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitDiscrete_range(self)




    def discrete_range(self):

        localctx = vhdlParser.Discrete_rangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 148, self.RULE_discrete_range)
        try:
            self.state = 1105
            la_ = self._interp.adaptivePredict(self._input, 92, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1103
                self.range()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1104
                self.subtype_indication()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Element_associationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def choices(self):
            return self.getTypedRuleContext(vhdlParser.ChoicesContext, 0)


        def ARROW(self):
            return self.getToken(vhdlParser.ARROW, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_element_association

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterElement_association(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitElement_association(self)




    def element_association(self):

        localctx = vhdlParser.Element_associationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 150, self.RULE_element_association)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1110
            la_ = self._interp.adaptivePredict(self._input, 93, self._ctx)
            if la_ == 1:
                self.state = 1107
                self.choices()
                self.state = 1108
                self.match(vhdlParser.ARROW)


            self.state = 1112
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Element_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def element_subtype_definition(self):
            return self.getTypedRuleContext(vhdlParser.Element_subtype_definitionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_element_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterElement_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitElement_declaration(self)




    def element_declaration(self):

        localctx = vhdlParser.Element_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 152, self.RULE_element_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1114
            self.identifier_list()
            self.state = 1115
            self.match(vhdlParser.COLON)
            self.state = 1116
            self.element_subtype_definition()
            self.state = 1117
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Element_subnature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_element_subnature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterElement_subnature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitElement_subnature_definition(self)




    def element_subnature_definition(self):

        localctx = vhdlParser.Element_subnature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 154, self.RULE_element_subnature_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1119
            self.subnature_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Element_subtype_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_element_subtype_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterElement_subtype_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitElement_subtype_definition(self)




    def element_subtype_definition(self):

        localctx = vhdlParser.Element_subtype_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 156, self.RULE_element_subtype_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1121
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTITY(self):
            return self.getToken(vhdlParser.ENTITY, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def CONFIGURATION(self):
            return self.getToken(vhdlParser.CONFIGURATION, 0)

        def OPEN(self):
            return self.getToken(vhdlParser.OPEN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_aspect(self)




    def entity_aspect(self):

        localctx = vhdlParser.Entity_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 158, self.RULE_entity_aspect)
        self._la = 0  # Token type
        try:
            self.state = 1134
            token = self._input.LA(1)
            if token == vhdlParser.ENTITY:
                self.enterOuterAlt(localctx, 1)
                self.state = 1123
                self.match(vhdlParser.ENTITY)
                self.state = 1124
                self.name()
                self.state = 1129
                _la = self._input.LA(1)
                if _la == vhdlParser.LPAREN:
                    self.state = 1125
                    self.match(vhdlParser.LPAREN)
                    self.state = 1126
                    self.identifier()
                    self.state = 1127
                    self.match(vhdlParser.RPAREN)



            elif token == vhdlParser.CONFIGURATION:
                self.enterOuterAlt(localctx, 2)
                self.state = 1131
                self.match(vhdlParser.CONFIGURATION)
                self.state = 1132
                self.name()

            elif token == vhdlParser.OPEN:
                self.enterOuterAlt(localctx, 3)
                self.state = 1133
                self.match(vhdlParser.OPEN)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_classContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTITY(self):
            return self.getToken(vhdlParser.ENTITY, 0)

        def ARCHITECTURE(self):
            return self.getToken(vhdlParser.ARCHITECTURE, 0)

        def CONFIGURATION(self):
            return self.getToken(vhdlParser.CONFIGURATION, 0)

        def PROCEDURE(self):
            return self.getToken(vhdlParser.PROCEDURE, 0)

        def FUNCTION(self):
            return self.getToken(vhdlParser.FUNCTION, 0)

        def PACKAGE(self):
            return self.getToken(vhdlParser.PACKAGE, 0)

        def TYPE(self):
            return self.getToken(vhdlParser.TYPE, 0)

        def SUBTYPE(self):
            return self.getToken(vhdlParser.SUBTYPE, 0)

        def CONSTANT(self):
            return self.getToken(vhdlParser.CONSTANT, 0)

        def SIGNAL(self):
            return self.getToken(vhdlParser.SIGNAL, 0)

        def VARIABLE(self):
            return self.getToken(vhdlParser.VARIABLE, 0)

        def COMPONENT(self):
            return self.getToken(vhdlParser.COMPONENT, 0)

        def LABEL(self):
            return self.getToken(vhdlParser.LABEL, 0)

        def LITERAL(self):
            return self.getToken(vhdlParser.LITERAL, 0)

        def UNITS(self):
            return self.getToken(vhdlParser.UNITS, 0)

        def GROUP(self):
            return self.getToken(vhdlParser.GROUP, 0)

        def FILE(self):
            return self.getToken(vhdlParser.FILE, 0)

        def NATURE(self):
            return self.getToken(vhdlParser.NATURE, 0)

        def SUBNATURE(self):
            return self.getToken(vhdlParser.SUBNATURE, 0)

        def QUANTITY(self):
            return self.getToken(vhdlParser.QUANTITY, 0)

        def TERMINAL(self):
            return self.getToken(vhdlParser.TERMINAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_class

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_class(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_class(self)




    def entity_class(self):

        localctx = vhdlParser.Entity_classContext(self, self._ctx, self.state)
        self.enterRule(localctx, 160, self.RULE_entity_class)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1136
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ARCHITECTURE) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONFIGURATION) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.ENTITY) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.LABEL) | (1 << vhdlParser.LITERAL) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (vhdlParser.PACKAGE - 64)) | (1 << (vhdlParser.PROCEDURE - 64)) | (1 << (vhdlParser.QUANTITY - 64)) | (1 << (vhdlParser.SIGNAL - 64)) | (1 << (vhdlParser.SUBNATURE - 64)) | (1 << (vhdlParser.SUBTYPE - 64)) | (1 << (vhdlParser.TERMINAL - 64)) | (1 << (vhdlParser.TYPE - 64)) | (1 << (vhdlParser.UNITS - 64)) | (1 << (vhdlParser.VARIABLE - 64)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_class_entryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_class(self):
            return self.getTypedRuleContext(vhdlParser.Entity_classContext, 0)


        def BOX(self):
            return self.getToken(vhdlParser.BOX, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_class_entry

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_class_entry(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_class_entry(self)




    def entity_class_entry(self):

        localctx = vhdlParser.Entity_class_entryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 162, self.RULE_entity_class_entry)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1138
            self.entity_class()
            self.state = 1140
            _la = self._input.LA(1)
            if _la == vhdlParser.BOX:
                self.state = 1139
                self.match(vhdlParser.BOX)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_class_entry_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_class_entry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Entity_class_entryContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Entity_class_entryContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_class_entry_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_class_entry_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_class_entry_list(self)




    def entity_class_entry_list(self):

        localctx = vhdlParser.Entity_class_entry_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 164, self.RULE_entity_class_entry_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1142
            self.entity_class_entry()
            self.state = 1147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1143
                self.match(vhdlParser.COMMA)
                self.state = 1144
                self.entity_class_entry()
                self.state = 1149
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTITY(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.ENTITY)
            else:
                return self.getToken(vhdlParser.ENTITY, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def entity_header(self):
            return self.getTypedRuleContext(vhdlParser.Entity_headerContext, 0)


        def entity_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Entity_declarative_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def entity_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Entity_statement_partContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_declaration(self)




    def entity_declaration(self):

        localctx = vhdlParser.Entity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 166, self.RULE_entity_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1150
            self.match(vhdlParser.ENTITY)
            self.state = 1151
            self.identifier()
            self.state = 1152
            self.match(vhdlParser.IS)
            self.state = 1153
            self.entity_header()
            self.state = 1154
            self.entity_declarative_part()
            self.state = 1157
            _la = self._input.LA(1)
            if _la == vhdlParser.BEGIN:
                self.state = 1155
                self.match(vhdlParser.BEGIN)
                self.state = 1156
                self.entity_statement_part()


            self.state = 1159
            self.match(vhdlParser.END)
            self.state = 1161
            _la = self._input.LA(1)
            if _la == vhdlParser.ENTITY:
                self.state = 1160
                self.match(vhdlParser.ENTITY)


            self.state = 1164
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1163
                self.identifier()


            self.state = 1166
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def signal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Signal_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def disconnection_specification(self):
            return self.getTypedRuleContext(vhdlParser.Disconnection_specificationContext, 0)


        def step_limit_specification(self):
            return self.getTypedRuleContext(vhdlParser.Step_limit_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def nature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Nature_declarationContext, 0)


        def subnature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_declarationContext, 0)


        def quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Quantity_declarationContext, 0)


        def terminal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Terminal_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_declarative_item(self)




    def entity_declarative_item(self):

        localctx = vhdlParser.Entity_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 168, self.RULE_entity_declarative_item)
        try:
            self.state = 1188
            la_ = self._interp.adaptivePredict(self._input, 101, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1168
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1169
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1170
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1171
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1172
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1173
                self.signal_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1174
                self.variable_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1175
                self.file_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1176
                self.alias_declaration()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1177
                self.attribute_declaration()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1178
                self.attribute_specification()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 1179
                self.disconnection_specification()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 1180
                self.step_limit_specification()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 1181
                self.use_clause()
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 1182
                self.group_template_declaration()
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 1183
                self.group_declaration()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 1184
                self.nature_declaration()
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 1185
                self.subnature_declaration()
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 1186
                self.quantity_declaration()
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 1187
                self.terminal_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Entity_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Entity_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_declarative_part(self)




    def entity_declarative_part(self):

        localctx = vhdlParser.Entity_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 170, self.RULE_entity_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.LIMIT) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.QUANTITY - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1190
                self.entity_declarative_item()
                self.state = 1195
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_designatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_tag(self):
            return self.getTypedRuleContext(vhdlParser.Entity_tagContext, 0)


        def signature(self):
            return self.getTypedRuleContext(vhdlParser.SignatureContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_designator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_designator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_designator(self)




    def entity_designator(self):

        localctx = vhdlParser.Entity_designatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 172, self.RULE_entity_designator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1196
            self.entity_tag()
            self.state = 1198
            _la = self._input.LA(1)
            if _la == vhdlParser.LBRACKET:
                self.state = 1197
                self.signature()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_headerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def generic_clause(self):
            return self.getTypedRuleContext(vhdlParser.Generic_clauseContext, 0)


        def port_clause(self):
            return self.getTypedRuleContext(vhdlParser.Port_clauseContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_header

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_header(self)




    def entity_header(self):

        localctx = vhdlParser.Entity_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 174, self.RULE_entity_header)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1201
            _la = self._input.LA(1)
            if _la == vhdlParser.GENERIC:
                self.state = 1200
                self.generic_clause()


            self.state = 1204
            _la = self._input.LA(1)
            if _la == vhdlParser.PORT:
                self.state = 1203
                self.port_clause()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_name_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_designator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Entity_designatorContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Entity_designatorContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def OTHERS(self):
            return self.getToken(vhdlParser.OTHERS, 0)

        def ALL(self):
            return self.getToken(vhdlParser.ALL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_name_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_name_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_name_list(self)




    def entity_name_list(self):

        localctx = vhdlParser.Entity_name_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 176, self.RULE_entity_name_list)
        self._la = 0  # Token type
        try:
            self.state = 1216
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.CHARACTER_LITERAL, vhdlParser.STRING_LITERAL]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1206
                self.entity_designator()
                self.state = 1211
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 1207
                    self.match(vhdlParser.COMMA)
                    self.state = 1208
                    self.entity_designator()
                    self.state = 1213
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token == vhdlParser.OTHERS:
                self.enterOuterAlt(localctx, 2)
                self.state = 1214
                self.match(vhdlParser.OTHERS)

            elif token == vhdlParser.ALL:
                self.enterOuterAlt(localctx, 3)
                self.state = 1215
                self.match(vhdlParser.ALL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_name_list(self):
            return self.getTypedRuleContext(vhdlParser.Entity_name_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def entity_class(self):
            return self.getTypedRuleContext(vhdlParser.Entity_classContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_specification(self)




    def entity_specification(self):

        localctx = vhdlParser.Entity_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 178, self.RULE_entity_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1218
            self.entity_name_list()
            self.state = 1219
            self.match(vhdlParser.COLON)
            self.state = 1220
            self.entity_class()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def concurrent_assertion_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_assertion_statementContext, 0)


        def process_statement(self):
            return self.getTypedRuleContext(vhdlParser.Process_statementContext, 0)


        def concurrent_procedure_call_statement(self):
            return self.getTypedRuleContext(vhdlParser.Concurrent_procedure_call_statementContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_statement(self)




    def entity_statement(self):

        localctx = vhdlParser.Entity_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 180, self.RULE_entity_statement)
        try:
            self.state = 1225
            la_ = self._interp.adaptivePredict(self._input, 108, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1222
                self.concurrent_assertion_statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1223
                self.process_statement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1224
                self.concurrent_procedure_call_statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Entity_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Entity_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_entity_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_statement_part(self)




    def entity_statement_part(self):

        localctx = vhdlParser.Entity_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 182, self.RULE_entity_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1230
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.ASSERT or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (vhdlParser.POSTPONED - 66)) | (1 << (vhdlParser.PROCESS - 66)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 66)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 66)))) != 0):
                self.state = 1227
                self.entity_statement()
                self.state = 1232
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Entity_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def CHARACTER_LITERAL(self):
            return self.getToken(vhdlParser.CHARACTER_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(vhdlParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_entity_tag

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEntity_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEntity_tag(self)




    def entity_tag(self):

        localctx = vhdlParser.Entity_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 184, self.RULE_entity_tag)
        try:
            self.state = 1236
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1233
                self.identifier()

            elif token == vhdlParser.CHARACTER_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 1234
                self.match(vhdlParser.CHARACTER_LITERAL)

            elif token == vhdlParser.STRING_LITERAL:
                self.enterOuterAlt(localctx, 3)
                self.state = 1235
                self.match(vhdlParser.STRING_LITERAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Enumeration_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def CHARACTER_LITERAL(self):
            return self.getToken(vhdlParser.CHARACTER_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_enumeration_literal

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEnumeration_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEnumeration_literal(self)




    def enumeration_literal(self):

        localctx = vhdlParser.Enumeration_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 186, self.RULE_enumeration_literal)
        try:
            self.state = 1240
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1238
                self.identifier()

            elif token == vhdlParser.CHARACTER_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 1239
                self.match(vhdlParser.CHARACTER_LITERAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Enumeration_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def enumeration_literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Enumeration_literalContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Enumeration_literalContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_enumeration_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterEnumeration_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitEnumeration_type_definition(self)




    def enumeration_type_definition(self):

        localctx = vhdlParser.Enumeration_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 188, self.RULE_enumeration_type_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1242
            self.match(vhdlParser.LPAREN)
            self.state = 1243
            self.enumeration_literal()
            self.state = 1248
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1244
                self.match(vhdlParser.COMMA)
                self.state = 1245
                self.enumeration_literal()
                self.state = 1250
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1251
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Exit_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXIT(self):
            return self.getToken(vhdlParser.EXIT, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_exit_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterExit_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitExit_statement(self)




    def exit_statement(self):

        localctx = vhdlParser.Exit_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 190, self.RULE_exit_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1254
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1253
                self.label_colon()


            self.state = 1256
            self.match(vhdlParser.EXIT)
            self.state = 1258
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1257
                self.identifier()


            self.state = 1262
            _la = self._input.LA(1)
            if _la == vhdlParser.WHEN:
                self.state = 1260
                self.match(vhdlParser.WHEN)
                self.state = 1261
                self.condition()


            self.state = 1264
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.RelationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.RelationContext, i)


        def logical_operator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Logical_operatorContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Logical_operatorContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitExpression(self)




    def expression(self):

        localctx = vhdlParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 192, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1266
            self.relation()
            self.state = 1272
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 116, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 1267
                    self.logical_operator()
                    self.state = 1268
                    self.relation() 
                self.state = 1274
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 116, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FactorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.PrimaryContext)
            else:
                return self.getTypedRuleContext(vhdlParser.PrimaryContext, i)


        def DOUBLESTAR(self):
            return self.getToken(vhdlParser.DOUBLESTAR, 0)

        def ABS(self):
            return self.getToken(vhdlParser.ABS, 0)

        def NOT(self):
            return self.getToken(vhdlParser.NOT, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFactor(self)




    def factor(self):

        localctx = vhdlParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 194, self.RULE_factor)
        try:
            self.state = 1284
            token = self._input.LA(1)
            if token in [vhdlParser.NEW, vhdlParser.NULL, vhdlParser.BASE_LITERAL, vhdlParser.BIT_STRING_LITERAL, vhdlParser.REAL_LITERAL, vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.CHARACTER_LITERAL, vhdlParser.STRING_LITERAL, vhdlParser.LPAREN, vhdlParser.INTEGER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1275
                self.primary()
                self.state = 1278
                la_ = self._interp.adaptivePredict(self._input, 117, self._ctx)
                if la_ == 1:
                    self.state = 1276
                    self.match(vhdlParser.DOUBLESTAR)
                    self.state = 1277
                    self.primary()



            elif token == vhdlParser.ABS:
                self.enterOuterAlt(localctx, 2)
                self.state = 1280
                self.match(vhdlParser.ABS)
                self.state = 1281
                self.primary()

            elif token == vhdlParser.NOT:
                self.enterOuterAlt(localctx, 3)
                self.state = 1282
                self.match(vhdlParser.NOT)
                self.state = 1283
                self.primary()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class File_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILE(self):
            return self.getToken(vhdlParser.FILE, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def file_open_information(self):
            return self.getTypedRuleContext(vhdlParser.File_open_informationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_file_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFile_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFile_declaration(self)




    def file_declaration(self):

        localctx = vhdlParser.File_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 196, self.RULE_file_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1286
            self.match(vhdlParser.FILE)
            self.state = 1287
            self.identifier_list()
            self.state = 1288
            self.match(vhdlParser.COLON)
            self.state = 1289
            self.subtype_indication()
            self.state = 1291
            _la = self._input.LA(1)
            if _la == vhdlParser.IS or _la == vhdlParser.OPEN:
                self.state = 1290
                self.file_open_information()


            self.state = 1293
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class File_logical_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_file_logical_name

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFile_logical_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFile_logical_name(self)




    def file_logical_name(self):

        localctx = vhdlParser.File_logical_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 198, self.RULE_file_logical_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1295
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class File_open_informationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def file_logical_name(self):
            return self.getTypedRuleContext(vhdlParser.File_logical_nameContext, 0)


        def OPEN(self):
            return self.getToken(vhdlParser.OPEN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_file_open_information

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFile_open_information(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFile_open_information(self)




    def file_open_information(self):

        localctx = vhdlParser.File_open_informationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 200, self.RULE_file_open_information)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1299
            _la = self._input.LA(1)
            if _la == vhdlParser.OPEN:
                self.state = 1297
                self.match(vhdlParser.OPEN)
                self.state = 1298
                self.expression()


            self.state = 1301
            self.match(vhdlParser.IS)
            self.state = 1302
            self.file_logical_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class File_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILE(self):
            return self.getToken(vhdlParser.FILE, 0)

        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_file_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFile_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFile_type_definition(self)




    def file_type_definition(self):

        localctx = vhdlParser.File_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 202, self.RULE_file_type_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1304
            self.match(vhdlParser.FILE)
            self.state = 1305
            self.match(vhdlParser.OF)
            self.state = 1306
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Formal_parameter_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_list(self):
            return self.getTypedRuleContext(vhdlParser.Interface_listContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_formal_parameter_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFormal_parameter_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFormal_parameter_list(self)




    def formal_parameter_list(self):

        localctx = vhdlParser.Formal_parameter_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 204, self.RULE_formal_parameter_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1308
            self.interface_list()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Formal_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def explicit_range(self):
            return self.getTypedRuleContext(vhdlParser.Explicit_rangeContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_formal_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFormal_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFormal_part(self)




    def formal_part(self):

        localctx = vhdlParser.Formal_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 206, self.RULE_formal_part)
        try:
            self.state = 1316
            la_ = self._interp.adaptivePredict(self._input, 121, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1310
                self.identifier()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1311
                self.identifier()
                self.state = 1312
                self.match(vhdlParser.LPAREN)
                self.state = 1313
                self.explicit_range()
                self.state = 1314
                self.match(vhdlParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Free_quantity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUANTITY(self):
            return self.getToken(vhdlParser.QUANTITY, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_free_quantity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFree_quantity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFree_quantity_declaration(self)




    def free_quantity_declaration(self):

        localctx = vhdlParser.Free_quantity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 208, self.RULE_free_quantity_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1318
            self.match(vhdlParser.QUANTITY)
            self.state = 1319
            self.identifier_list()
            self.state = 1320
            self.match(vhdlParser.COLON)
            self.state = 1321
            self.subtype_indication()
            self.state = 1324
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1322
                self.match(vhdlParser.VARASGN)
                self.state = 1323
                self.expression()


            self.state = 1326
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Generate_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def generation_scheme(self):
            return self.getTypedRuleContext(vhdlParser.Generation_schemeContext, 0)


        def GENERATE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.GENERATE)
            else:
                return self.getToken(vhdlParser.GENERATE, i)

        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def architecture_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Architecture_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Architecture_statementContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def block_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Block_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Block_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_generate_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGenerate_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGenerate_statement(self)




    def generate_statement(self):

        localctx = vhdlParser.Generate_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 210, self.RULE_generate_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1328
            self.label_colon()
            self.state = 1329
            self.generation_scheme()
            self.state = 1330
            self.match(vhdlParser.GENERATE)
            self.state = 1338
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.BEGIN) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FOR) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.LIMIT) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.QUANTITY - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1334
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FOR) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.LIMIT) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.QUANTITY - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                    self.state = 1331
                    self.block_declarative_item()
                    self.state = 1336
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 1337
                self.match(vhdlParser.BEGIN)


            self.state = 1343
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.IF) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (vhdlParser.POSTPONED - 66)) | (1 << (vhdlParser.PROCESS - 66)) | (1 << (vhdlParser.PROCEDURAL - 66)) | (1 << (vhdlParser.WITH - 66)) | (1 << (vhdlParser.BASE_LITERAL - 66)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 66)) | (1 << (vhdlParser.REAL_LITERAL - 66)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 66)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 66)) | (1 << (vhdlParser.CHARACTER_LITERAL - 66)) | (1 << (vhdlParser.STRING_LITERAL - 66)))) != 0) or ((((_la - 141)) & ~0x3f) == 0 and ((1 << (_la - 141)) & ((1 << (vhdlParser.LPAREN - 141)) | (1 << (vhdlParser.PLUS - 141)) | (1 << (vhdlParser.MINUS - 141)) | (1 << (vhdlParser.INTEGER - 141)))) != 0):
                self.state = 1340
                self.architecture_statement()
                self.state = 1345
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1346
            self.match(vhdlParser.END)
            self.state = 1347
            self.match(vhdlParser.GENERATE)
            self.state = 1349
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1348
                self.identifier()


            self.state = 1351
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Generation_schemeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(vhdlParser.FOR, 0)

        def parameter_specification(self):
            return self.getTypedRuleContext(vhdlParser.Parameter_specificationContext, 0)


        def IF(self):
            return self.getToken(vhdlParser.IF, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_generation_scheme

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGeneration_scheme(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGeneration_scheme(self)




    def generation_scheme(self):

        localctx = vhdlParser.Generation_schemeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 212, self.RULE_generation_scheme)
        try:
            self.state = 1357
            token = self._input.LA(1)
            if token == vhdlParser.FOR:
                self.enterOuterAlt(localctx, 1)
                self.state = 1353
                self.match(vhdlParser.FOR)
                self.state = 1354
                self.parameter_specification()

            elif token == vhdlParser.IF:
                self.enterOuterAlt(localctx, 2)
                self.state = 1355
                self.match(vhdlParser.IF)
                self.state = 1356
                self.condition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Generic_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GENERIC(self):
            return self.getToken(vhdlParser.GENERIC, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def generic_list(self):
            return self.getTypedRuleContext(vhdlParser.Generic_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_generic_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGeneric_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGeneric_clause(self)




    def generic_clause(self):

        localctx = vhdlParser.Generic_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 214, self.RULE_generic_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1359
            self.match(vhdlParser.GENERIC)
            self.state = 1360
            self.match(vhdlParser.LPAREN)
            self.state = 1361
            self.generic_list()
            self.state = 1362
            self.match(vhdlParser.RPAREN)
            self.state = 1363
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Generic_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_constant_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Interface_constant_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Interface_constant_declarationContext, i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_generic_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGeneric_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGeneric_list(self)




    def generic_list(self):

        localctx = vhdlParser.Generic_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 216, self.RULE_generic_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1365
            self.interface_constant_declaration()
            self.state = 1370
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.SEMI:
                self.state = 1366
                self.match(vhdlParser.SEMI)
                self.state = 1367
                self.interface_constant_declaration()
                self.state = 1372
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Generic_map_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GENERIC(self):
            return self.getToken(vhdlParser.GENERIC, 0)

        def MAP(self):
            return self.getToken(vhdlParser.MAP, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def association_list(self):
            return self.getTypedRuleContext(vhdlParser.Association_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_generic_map_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGeneric_map_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGeneric_map_aspect(self)




    def generic_map_aspect(self):

        localctx = vhdlParser.Generic_map_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 218, self.RULE_generic_map_aspect)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1373
            self.match(vhdlParser.GENERIC)
            self.state = 1374
            self.match(vhdlParser.MAP)
            self.state = 1375
            self.match(vhdlParser.LPAREN)
            self.state = 1376
            self.association_list()
            self.state = 1377
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Group_constituentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def CHARACTER_LITERAL(self):
            return self.getToken(vhdlParser.CHARACTER_LITERAL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_group_constituent

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGroup_constituent(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGroup_constituent(self)




    def group_constituent(self):

        localctx = vhdlParser.Group_constituentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 220, self.RULE_group_constituent)
        try:
            self.state = 1381
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1379
                self.name()

            elif token == vhdlParser.CHARACTER_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 1380
                self.match(vhdlParser.CHARACTER_LITERAL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Group_constituent_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def group_constituent(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Group_constituentContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Group_constituentContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_group_constituent_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGroup_constituent_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGroup_constituent_list(self)




    def group_constituent_list(self):

        localctx = vhdlParser.Group_constituent_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 222, self.RULE_group_constituent_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1383
            self.group_constituent()
            self.state = 1388
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1384
                self.match(vhdlParser.COMMA)
                self.state = 1385
                self.group_constituent()
                self.state = 1390
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Group_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GROUP(self):
            return self.getToken(vhdlParser.GROUP, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def group_constituent_list(self):
            return self.getTypedRuleContext(vhdlParser.Group_constituent_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_group_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGroup_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGroup_declaration(self)




    def group_declaration(self):

        localctx = vhdlParser.Group_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 224, self.RULE_group_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1391
            self.match(vhdlParser.GROUP)
            self.state = 1392
            self.label_colon()
            self.state = 1393
            self.name()
            self.state = 1394
            self.match(vhdlParser.LPAREN)
            self.state = 1395
            self.group_constituent_list()
            self.state = 1396
            self.match(vhdlParser.RPAREN)
            self.state = 1397
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Group_template_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GROUP(self):
            return self.getToken(vhdlParser.GROUP, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def entity_class_entry_list(self):
            return self.getTypedRuleContext(vhdlParser.Entity_class_entry_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_group_template_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGroup_template_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGroup_template_declaration(self)




    def group_template_declaration(self):

        localctx = vhdlParser.Group_template_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 226, self.RULE_group_template_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1399
            self.match(vhdlParser.GROUP)
            self.state = 1400
            self.identifier()
            self.state = 1401
            self.match(vhdlParser.IS)
            self.state = 1402
            self.match(vhdlParser.LPAREN)
            self.state = 1403
            self.entity_class_entry_list()
            self.state = 1404
            self.match(vhdlParser.RPAREN)
            self.state = 1405
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Guarded_signal_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signal_list(self):
            return self.getTypedRuleContext(vhdlParser.Signal_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_guarded_signal_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterGuarded_signal_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitGuarded_signal_specification(self)




    def guarded_signal_specification(self):

        localctx = vhdlParser.Guarded_signal_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 228, self.RULE_guarded_signal_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1407
            self.signal_list()
            self.state = 1408
            self.match(vhdlParser.COLON)
            self.state = 1409
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdentifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASIC_IDENTIFIER(self):
            return self.getToken(vhdlParser.BASIC_IDENTIFIER, 0)

        def EXTENDED_IDENTIFIER(self):
            return self.getToken(vhdlParser.EXTENDED_IDENTIFIER, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIdentifier(self)




    def identifier(self):

        localctx = vhdlParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 230, self.RULE_identifier)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1411
            _la = self._input.LA(1)
            if not(_la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Identifier_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_identifier_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIdentifier_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIdentifier_list(self)




    def identifier_list(self):

        localctx = vhdlParser.Identifier_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 232, self.RULE_identifier_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1413
            self.identifier()
            self.state = 1418
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1414
                self.match(vhdlParser.COMMA)
                self.state = 1415
                self.identifier()
                self.state = 1420
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class If_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.IF)
            else:
                return self.getToken(vhdlParser.IF, i)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ConditionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ConditionContext, i)


        def THEN(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.THEN)
            else:
                return self.getToken(vhdlParser.THEN, i)

        def sequence_of_statements(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Sequence_of_statementsContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Sequence_of_statementsContext, i)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def ELSIF(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.ELSIF)
            else:
                return self.getToken(vhdlParser.ELSIF, i)

        def ELSE(self):
            return self.getToken(vhdlParser.ELSE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_if_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIf_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIf_statement(self)




    def if_statement(self):

        localctx = vhdlParser.If_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 234, self.RULE_if_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1422
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1421
                self.label_colon()


            self.state = 1424
            self.match(vhdlParser.IF)
            self.state = 1425
            self.condition()
            self.state = 1426
            self.match(vhdlParser.THEN)
            self.state = 1427
            self.sequence_of_statements()
            self.state = 1435
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.ELSIF:
                self.state = 1428
                self.match(vhdlParser.ELSIF)
                self.state = 1429
                self.condition()
                self.state = 1430
                self.match(vhdlParser.THEN)
                self.state = 1431
                self.sequence_of_statements()
                self.state = 1437
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1440
            _la = self._input.LA(1)
            if _la == vhdlParser.ELSE:
                self.state = 1438
                self.match(vhdlParser.ELSE)
                self.state = 1439
                self.sequence_of_statements()


            self.state = 1442
            self.match(vhdlParser.END)
            self.state = 1443
            self.match(vhdlParser.IF)
            self.state = 1445
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1444
                self.identifier()


            self.state = 1447
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Index_constraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def discrete_range(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Discrete_rangeContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Discrete_rangeContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_index_constraint

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIndex_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIndex_constraint(self)




    def index_constraint(self):

        localctx = vhdlParser.Index_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 236, self.RULE_index_constraint)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1449
            self.match(vhdlParser.LPAREN)
            self.state = 1450
            self.discrete_range()
            self.state = 1455
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1451
                self.match(vhdlParser.COMMA)
                self.state = 1452
                self.discrete_range()
                self.state = 1457
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1458
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Index_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def discrete_range(self):
            return self.getTypedRuleContext(vhdlParser.Discrete_rangeContext, 0)


        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_index_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIndex_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIndex_specification(self)




    def index_specification(self):

        localctx = vhdlParser.Index_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 238, self.RULE_index_specification)
        try:
            self.state = 1462
            la_ = self._interp.adaptivePredict(self._input, 137, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1460
                self.discrete_range()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1461
                self.expression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Index_subtype_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def RANGE(self):
            return self.getToken(vhdlParser.RANGE, 0)

        def BOX(self):
            return self.getToken(vhdlParser.BOX, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_index_subtype_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIndex_subtype_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIndex_subtype_definition(self)




    def index_subtype_definition(self):

        localctx = vhdlParser.Index_subtype_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 240, self.RULE_index_subtype_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1464
            self.name()
            self.state = 1465
            self.match(vhdlParser.RANGE)
            self.state = 1466
            self.match(vhdlParser.BOX)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Instantiated_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def COMPONENT(self):
            return self.getToken(vhdlParser.COMPONENT, 0)

        def ENTITY(self):
            return self.getToken(vhdlParser.ENTITY, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def CONFIGURATION(self):
            return self.getToken(vhdlParser.CONFIGURATION, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_instantiated_unit

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInstantiated_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInstantiated_unit(self)




    def instantiated_unit(self):

        localctx = vhdlParser.Instantiated_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 242, self.RULE_instantiated_unit)
        self._la = 0  # Token type
        try:
            self.state = 1482
            token = self._input.LA(1)
            if token in [vhdlParser.COMPONENT, vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1469
                _la = self._input.LA(1)
                if _la == vhdlParser.COMPONENT:
                    self.state = 1468
                    self.match(vhdlParser.COMPONENT)


                self.state = 1471
                self.name()

            elif token == vhdlParser.ENTITY:
                self.enterOuterAlt(localctx, 2)
                self.state = 1472
                self.match(vhdlParser.ENTITY)
                self.state = 1473
                self.name()
                self.state = 1478
                _la = self._input.LA(1)
                if _la == vhdlParser.LPAREN:
                    self.state = 1474
                    self.match(vhdlParser.LPAREN)
                    self.state = 1475
                    self.identifier()
                    self.state = 1476
                    self.match(vhdlParser.RPAREN)



            elif token == vhdlParser.CONFIGURATION:
                self.enterOuterAlt(localctx, 3)
                self.state = 1480
                self.match(vhdlParser.CONFIGURATION)
                self.state = 1481
                self.name()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Instantiation_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def OTHERS(self):
            return self.getToken(vhdlParser.OTHERS, 0)

        def ALL(self):
            return self.getToken(vhdlParser.ALL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_instantiation_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInstantiation_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInstantiation_list(self)




    def instantiation_list(self):

        localctx = vhdlParser.Instantiation_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 244, self.RULE_instantiation_list)
        self._la = 0  # Token type
        try:
            self.state = 1494
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 1484
                self.identifier()
                self.state = 1489
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 1485
                    self.match(vhdlParser.COMMA)
                    self.state = 1486
                    self.identifier()
                    self.state = 1491
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token == vhdlParser.OTHERS:
                self.enterOuterAlt(localctx, 2)
                self.state = 1492
                self.match(vhdlParser.OTHERS)

            elif token == vhdlParser.ALL:
                self.enterOuterAlt(localctx, 3)
                self.state = 1493
                self.match(vhdlParser.ALL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_constant_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def CONSTANT(self):
            return self.getToken(vhdlParser.CONSTANT, 0)

        def IN(self):
            return self.getToken(vhdlParser.IN, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_constant_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_constant_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_constant_declaration(self)




    def interface_constant_declaration(self):

        localctx = vhdlParser.Interface_constant_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 246, self.RULE_interface_constant_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1497
            _la = self._input.LA(1)
            if _la == vhdlParser.CONSTANT:
                self.state = 1496
                self.match(vhdlParser.CONSTANT)


            self.state = 1499
            self.identifier_list()
            self.state = 1500
            self.match(vhdlParser.COLON)
            self.state = 1502
            _la = self._input.LA(1)
            if _la == vhdlParser.IN:
                self.state = 1501
                self.match(vhdlParser.IN)


            self.state = 1504
            self.subtype_indication()
            self.state = 1507
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1505
                self.match(vhdlParser.VARASGN)
                self.state = 1506
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_constant_declarationContext, 0)


        def interface_signal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_signal_declarationContext, 0)


        def interface_variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_variable_declarationContext, 0)


        def interface_file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_file_declarationContext, 0)


        def interface_terminal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_terminal_declarationContext, 0)


        def interface_quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_quantity_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_declaration(self)




    def interface_declaration(self):

        localctx = vhdlParser.Interface_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 248, self.RULE_interface_declaration)
        try:
            self.state = 1515
            la_ = self._interp.adaptivePredict(self._input, 146, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1509
                self.interface_constant_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1510
                self.interface_signal_declaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1511
                self.interface_variable_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1512
                self.interface_file_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1513
                self.interface_terminal_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1514
                self.interface_quantity_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_elementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Interface_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_element

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_element(self)




    def interface_element(self):

        localctx = vhdlParser.Interface_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 250, self.RULE_interface_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1517
            self.interface_declaration()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_file_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILE(self):
            return self.getToken(vhdlParser.FILE, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_file_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_file_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_file_declaration(self)




    def interface_file_declaration(self):

        localctx = vhdlParser.Interface_file_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 252, self.RULE_interface_file_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1519
            self.match(vhdlParser.FILE)
            self.state = 1520
            self.identifier_list()
            self.state = 1521
            self.match(vhdlParser.COLON)
            self.state = 1522
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_signal_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_signal_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Interface_signal_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Interface_signal_declarationContext, i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_interface_signal_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_signal_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_signal_list(self)




    def interface_signal_list(self):

        localctx = vhdlParser.Interface_signal_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 254, self.RULE_interface_signal_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1524
            self.interface_signal_declaration()
            self.state = 1529
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.SEMI:
                self.state = 1525
                self.match(vhdlParser.SEMI)
                self.state = 1526
                self.interface_signal_declaration()
                self.state = 1531
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_port_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_port_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Interface_port_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Interface_port_declarationContext, i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_interface_port_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_port_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_port_list(self)




    def interface_port_list(self):

        localctx = vhdlParser.Interface_port_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 256, self.RULE_interface_port_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1532
            self.interface_port_declaration()
            self.state = 1537
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.SEMI:
                self.state = 1533
                self.match(vhdlParser.SEMI)
                self.state = 1534
                self.interface_port_declaration()
                self.state = 1539
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Interface_elementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Interface_elementContext, i)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.SEMI)
            else:
                return self.getToken(vhdlParser.SEMI, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_interface_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_list(self)




    def interface_list(self):

        localctx = vhdlParser.Interface_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 258, self.RULE_interface_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1540
            self.interface_element()
            self.state = 1545
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.SEMI:
                self.state = 1541
                self.match(vhdlParser.SEMI)
                self.state = 1542
                self.interface_element()
                self.state = 1547
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_quantity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUANTITY(self):
            return self.getToken(vhdlParser.QUANTITY, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def IN(self):
            return self.getToken(vhdlParser.IN, 0)

        def OUT(self):
            return self.getToken(vhdlParser.OUT, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_interface_quantity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_quantity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_quantity_declaration(self)




    def interface_quantity_declaration(self):

        localctx = vhdlParser.Interface_quantity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 260, self.RULE_interface_quantity_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1548
            self.match(vhdlParser.QUANTITY)
            self.state = 1549
            self.identifier_list()
            self.state = 1550
            self.match(vhdlParser.COLON)
            self.state = 1552
            _la = self._input.LA(1)
            if _la == vhdlParser.IN or _la == vhdlParser.OUT:
                self.state = 1551
                _la = self._input.LA(1)
                if not(_la == vhdlParser.IN or _la == vhdlParser.OUT):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()


            self.state = 1554
            self.subtype_indication()
            self.state = 1557
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1555
                self.match(vhdlParser.VARASGN)
                self.state = 1556
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_port_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def signal_mode(self):
            return self.getTypedRuleContext(vhdlParser.Signal_modeContext, 0)


        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def BUS(self):
            return self.getToken(vhdlParser.BUS, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_port_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_port_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_port_declaration(self)




    def interface_port_declaration(self):

        localctx = vhdlParser.Interface_port_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 262, self.RULE_interface_port_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1559
            self.identifier_list()
            self.state = 1560
            self.match(vhdlParser.COLON)
            self.state = 1561
            self.signal_mode()
            self.state = 1562
            self.subtype_indication()
            self.state = 1564
            _la = self._input.LA(1)
            if _la == vhdlParser.BUS:
                self.state = 1563
                self.match(vhdlParser.BUS)


            self.state = 1568
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1566
                self.match(vhdlParser.VARASGN)
                self.state = 1567
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_signal_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIGNAL(self):
            return self.getToken(vhdlParser.SIGNAL, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def BUS(self):
            return self.getToken(vhdlParser.BUS, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_signal_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_signal_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_signal_declaration(self)




    def interface_signal_declaration(self):

        localctx = vhdlParser.Interface_signal_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 264, self.RULE_interface_signal_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1570
            self.match(vhdlParser.SIGNAL)
            self.state = 1571
            self.identifier_list()
            self.state = 1572
            self.match(vhdlParser.COLON)
            self.state = 1573
            self.subtype_indication()
            self.state = 1575
            _la = self._input.LA(1)
            if _la == vhdlParser.BUS:
                self.state = 1574
                self.match(vhdlParser.BUS)


            self.state = 1579
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1577
                self.match(vhdlParser.VARASGN)
                self.state = 1578
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_terminal_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TERMINAL(self):
            return self.getToken(vhdlParser.TERMINAL, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_terminal_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_terminal_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_terminal_declaration(self)




    def interface_terminal_declaration(self):

        localctx = vhdlParser.Interface_terminal_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 266, self.RULE_interface_terminal_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1581
            self.match(vhdlParser.TERMINAL)
            self.state = 1582
            self.identifier_list()
            self.state = 1583
            self.match(vhdlParser.COLON)
            self.state = 1584
            self.subnature_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Interface_variable_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def VARIABLE(self):
            return self.getToken(vhdlParser.VARIABLE, 0)

        def signal_mode(self):
            return self.getTypedRuleContext(vhdlParser.Signal_modeContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_interface_variable_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterInterface_variable_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitInterface_variable_declaration(self)




    def interface_variable_declaration(self):

        localctx = vhdlParser.Interface_variable_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 268, self.RULE_interface_variable_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1587
            _la = self._input.LA(1)
            if _la == vhdlParser.VARIABLE:
                self.state = 1586
                self.match(vhdlParser.VARIABLE)


            self.state = 1589
            self.identifier_list()
            self.state = 1590
            self.match(vhdlParser.COLON)
            self.state = 1592
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.BUFFER) | (1 << vhdlParser.IN) | (1 << vhdlParser.INOUT) | (1 << vhdlParser.LINKAGE) | (1 << vhdlParser.OUT))) != 0):
                self.state = 1591
                self.signal_mode()


            self.state = 1594
            self.subtype_indication()
            self.state = 1597
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 1595
                self.match(vhdlParser.VARASGN)
                self.state = 1596
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Iteration_schemeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(vhdlParser.WHILE, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def FOR(self):
            return self.getToken(vhdlParser.FOR, 0)

        def parameter_specification(self):
            return self.getTypedRuleContext(vhdlParser.Parameter_specificationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_iteration_scheme

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterIteration_scheme(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitIteration_scheme(self)




    def iteration_scheme(self):

        localctx = vhdlParser.Iteration_schemeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 270, self.RULE_iteration_scheme)
        try:
            self.state = 1603
            token = self._input.LA(1)
            if token == vhdlParser.WHILE:
                self.enterOuterAlt(localctx, 1)
                self.state = 1599
                self.match(vhdlParser.WHILE)
                self.state = 1600
                self.condition()

            elif token == vhdlParser.FOR:
                self.enterOuterAlt(localctx, 2)
                self.state = 1601
                self.match(vhdlParser.FOR)
                self.state = 1602
                self.parameter_specification()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Label_colonContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_label_colon

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLabel_colon(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLabel_colon(self)




    def label_colon(self):

        localctx = vhdlParser.Label_colonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 272, self.RULE_label_colon)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1605
            self.identifier()
            self.state = 1606
            self.match(vhdlParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Library_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LIBRARY(self):
            return self.getToken(vhdlParser.LIBRARY, 0)

        def logical_name_list(self):
            return self.getTypedRuleContext(vhdlParser.Logical_name_listContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_library_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLibrary_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLibrary_clause(self)




    def library_clause(self):

        localctx = vhdlParser.Library_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 274, self.RULE_library_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1608
            self.match(vhdlParser.LIBRARY)
            self.state = 1609
            self.logical_name_list()
            self.state = 1610
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Library_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def secondary_unit(self):
            return self.getTypedRuleContext(vhdlParser.Secondary_unitContext, 0)


        def primary_unit(self):
            return self.getTypedRuleContext(vhdlParser.Primary_unitContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_library_unit

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLibrary_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLibrary_unit(self)




    def library_unit(self):

        localctx = vhdlParser.Library_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 276, self.RULE_library_unit)
        try:
            self.state = 1614
            la_ = self._interp.adaptivePredict(self._input, 160, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1612
                self.secondary_unit()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1613
                self.primary_unit()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LiteralContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NULL(self):
            return self.getToken(vhdlParser.NULL, 0)

        def BIT_STRING_LITERAL(self):
            return self.getToken(vhdlParser.BIT_STRING_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(vhdlParser.STRING_LITERAL, 0)

        def enumeration_literal(self):
            return self.getTypedRuleContext(vhdlParser.Enumeration_literalContext, 0)


        def numeric_literal(self):
            return self.getTypedRuleContext(vhdlParser.Numeric_literalContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLiteral(self)




    def literal(self):

        localctx = vhdlParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 278, self.RULE_literal)
        try:
            self.state = 1621
            token = self._input.LA(1)
            if token == vhdlParser.NULL:
                self.enterOuterAlt(localctx, 1)
                self.state = 1616
                self.match(vhdlParser.NULL)

            elif token == vhdlParser.BIT_STRING_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 1617
                self.match(vhdlParser.BIT_STRING_LITERAL)

            elif token == vhdlParser.STRING_LITERAL:
                self.enterOuterAlt(localctx, 3)
                self.state = 1618
                self.match(vhdlParser.STRING_LITERAL)

            elif token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.CHARACTER_LITERAL]:
                self.enterOuterAlt(localctx, 4)
                self.state = 1619
                self.enumeration_literal()

            elif token in [vhdlParser.BASE_LITERAL, vhdlParser.REAL_LITERAL, vhdlParser.INTEGER]:
                self.enterOuterAlt(localctx, 5)
                self.state = 1620
                self.numeric_literal()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Logical_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_logical_name

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLogical_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLogical_name(self)




    def logical_name(self):

        localctx = vhdlParser.Logical_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 280, self.RULE_logical_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1623
            self.identifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Logical_name_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logical_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Logical_nameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Logical_nameContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_logical_name_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLogical_name_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLogical_name_list(self)




    def logical_name_list(self):

        localctx = vhdlParser.Logical_name_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 282, self.RULE_logical_name_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1625
            self.logical_name()
            self.state = 1630
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1626
                self.match(vhdlParser.COMMA)
                self.state = 1627
                self.logical_name()
                self.state = 1632
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Logical_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(vhdlParser.AND, 0)

        def OR(self):
            return self.getToken(vhdlParser.OR, 0)

        def NAND(self):
            return self.getToken(vhdlParser.NAND, 0)

        def NOR(self):
            return self.getToken(vhdlParser.NOR, 0)

        def XOR(self):
            return self.getToken(vhdlParser.XOR, 0)

        def XNOR(self):
            return self.getToken(vhdlParser.XNOR, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_logical_operator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLogical_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLogical_operator(self)




    def logical_operator(self):

        localctx = vhdlParser.Logical_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 284, self.RULE_logical_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1633
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.AND) | (1 << vhdlParser.NAND) | (1 << vhdlParser.NOR) | (1 << vhdlParser.OR))) != 0) or _la == vhdlParser.XNOR or _la == vhdlParser.XOR):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Loop_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LOOP(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.LOOP)
            else:
                return self.getToken(vhdlParser.LOOP, i)

        def sequence_of_statements(self):
            return self.getTypedRuleContext(vhdlParser.Sequence_of_statementsContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def iteration_scheme(self):
            return self.getTypedRuleContext(vhdlParser.Iteration_schemeContext, 0)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_loop_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterLoop_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitLoop_statement(self)




    def loop_statement(self):

        localctx = vhdlParser.Loop_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 286, self.RULE_loop_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1636
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1635
                self.label_colon()


            self.state = 1639
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR or _la == vhdlParser.WHILE:
                self.state = 1638
                self.iteration_scheme()


            self.state = 1641
            self.match(vhdlParser.LOOP)
            self.state = 1642
            self.sequence_of_statements()
            self.state = 1643
            self.match(vhdlParser.END)
            self.state = 1644
            self.match(vhdlParser.LOOP)
            self.state = 1646
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1645
                self.identifier()


            self.state = 1648
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Signal_modeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IN(self):
            return self.getToken(vhdlParser.IN, 0)

        def OUT(self):
            return self.getToken(vhdlParser.OUT, 0)

        def INOUT(self):
            return self.getToken(vhdlParser.INOUT, 0)

        def BUFFER(self):
            return self.getToken(vhdlParser.BUFFER, 0)

        def LINKAGE(self):
            return self.getToken(vhdlParser.LINKAGE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_signal_mode

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignal_mode(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignal_mode(self)




    def signal_mode(self):

        localctx = vhdlParser.Signal_modeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 288, self.RULE_signal_mode)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1650
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.BUFFER) | (1 << vhdlParser.IN) | (1 << vhdlParser.INOUT) | (1 << vhdlParser.LINKAGE) | (1 << vhdlParser.OUT))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Multiplying_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MUL(self):
            return self.getToken(vhdlParser.MUL, 0)

        def DIV(self):
            return self.getToken(vhdlParser.DIV, 0)

        def MOD(self):
            return self.getToken(vhdlParser.MOD, 0)

        def REM(self):
            return self.getToken(vhdlParser.REM, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_multiplying_operator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterMultiplying_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitMultiplying_operator(self)




    def multiplying_operator(self):

        localctx = vhdlParser.Multiplying_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 290, self.RULE_multiplying_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1652
            _la = self._input.LA(1)
            if not(_la == vhdlParser.MOD or _la == vhdlParser.REM or _la == vhdlParser.MUL or _la == vhdlParser.DIV):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selected_name(self):
            return self.getTypedRuleContext(vhdlParser.Selected_nameContext, 0)


        def name_part(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Name_partContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Name_partContext, i)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.DOT)
            else:
                return self.getToken(vhdlParser.DOT, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitName(self)




    def name(self):

        localctx = vhdlParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 292, self.RULE_name)
        try:
            self.state = 1663
            la_ = self._interp.adaptivePredict(self._input, 167, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1654
                self.selected_name()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1655
                self.name_part()
                self.state = 1660
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 166, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1656
                        self.match(vhdlParser.DOT)
                        self.state = 1657
                        self.name_part() 
                    self.state = 1662
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 166, self._ctx)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Name_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selected_name(self):
            return self.getTypedRuleContext(vhdlParser.Selected_nameContext, 0)


        def name_attribute_part(self):
            return self.getTypedRuleContext(vhdlParser.Name_attribute_partContext, 0)


        def name_function_call_or_indexed_part(self):
            return self.getTypedRuleContext(vhdlParser.Name_function_call_or_indexed_partContext, 0)


        def name_slice_part(self):
            return self.getTypedRuleContext(vhdlParser.Name_slice_partContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_name_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterName_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitName_part(self)




    def name_part(self):

        localctx = vhdlParser.Name_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 294, self.RULE_name_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1665
            self.selected_name()
            self.state = 1669
            la_ = self._interp.adaptivePredict(self._input, 168, self._ctx)
            if la_ == 1:
                self.state = 1666
                self.name_attribute_part()

            elif la_ == 2:
                self.state = 1667
                self.name_function_call_or_indexed_part()

            elif la_ == 3:
                self.state = 1668
                self.name_slice_part()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Name_attribute_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def APOSTROPHE(self):
            return self.getToken(vhdlParser.APOSTROPHE, 0)

        def attribute_designator(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_designatorContext, 0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ExpressionContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_name_attribute_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterName_attribute_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitName_attribute_part(self)




    def name_attribute_part(self):

        localctx = vhdlParser.Name_attribute_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 296, self.RULE_name_attribute_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1671
            self.match(vhdlParser.APOSTROPHE)
            self.state = 1672
            self.attribute_designator()
            self.state = 1681
            la_ = self._interp.adaptivePredict(self._input, 170, self._ctx)
            if la_ == 1:
                self.state = 1673
                self.expression()
                self.state = 1678
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 169, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 1674
                        self.match(vhdlParser.COMMA)
                        self.state = 1675
                        self.expression() 
                    self.state = 1680
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 169, self._ctx)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Name_function_call_or_indexed_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def actual_parameter_part(self):
            return self.getTypedRuleContext(vhdlParser.Actual_parameter_partContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_name_function_call_or_indexed_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterName_function_call_or_indexed_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitName_function_call_or_indexed_part(self)




    def name_function_call_or_indexed_part(self):

        localctx = vhdlParser.Name_function_call_or_indexed_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 298, self.RULE_name_function_call_or_indexed_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1683
            self.match(vhdlParser.LPAREN)
            self.state = 1685
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL) | (1 << vhdlParser.OPEN))) != 0) or ((((_la - 112)) & ~0x3f) == 0 and ((1 << (_la - 112)) & ((1 << (vhdlParser.BASE_LITERAL - 112)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 112)) | (1 << (vhdlParser.REAL_LITERAL - 112)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 112)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 112)) | (1 << (vhdlParser.CHARACTER_LITERAL - 112)) | (1 << (vhdlParser.STRING_LITERAL - 112)) | (1 << (vhdlParser.LPAREN - 112)) | (1 << (vhdlParser.PLUS - 112)) | (1 << (vhdlParser.MINUS - 112)) | (1 << (vhdlParser.INTEGER - 112)))) != 0):
                self.state = 1684
                self.actual_parameter_part()


            self.state = 1687
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Name_slice_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def explicit_range(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Explicit_rangeContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Explicit_rangeContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_name_slice_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterName_slice_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitName_slice_part(self)




    def name_slice_part(self):

        localctx = vhdlParser.Name_slice_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 300, self.RULE_name_slice_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1689
            self.match(vhdlParser.LPAREN)
            self.state = 1690
            self.explicit_range()
            self.state = 1695
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 1691
                self.match(vhdlParser.COMMA)
                self.state = 1692
                self.explicit_range()
                self.state = 1697
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1698
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Selected_nameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.DOT)
            else:
                return self.getToken(vhdlParser.DOT, i)

        def suffix(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.SuffixContext)
            else:
                return self.getTypedRuleContext(vhdlParser.SuffixContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_selected_name

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSelected_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSelected_name(self)




    def selected_name(self):

        localctx = vhdlParser.Selected_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 302, self.RULE_selected_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1700
            self.identifier()
            self.state = 1705
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 173, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 1701
                    self.match(vhdlParser.DOT)
                    self.state = 1702
                    self.suffix() 
                self.state = 1707
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 173, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Nature_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NATURE(self):
            return self.getToken(vhdlParser.NATURE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Nature_definitionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_nature_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterNature_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitNature_declaration(self)




    def nature_declaration(self):

        localctx = vhdlParser.Nature_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 304, self.RULE_nature_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1708
            self.match(vhdlParser.NATURE)
            self.state = 1709
            self.identifier()
            self.state = 1710
            self.match(vhdlParser.IS)
            self.state = 1711
            self.nature_definition()
            self.state = 1712
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def scalar_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Scalar_nature_definitionContext, 0)


        def composite_nature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Composite_nature_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterNature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitNature_definition(self)




    def nature_definition(self):

        localctx = vhdlParser.Nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 306, self.RULE_nature_definition)
        try:
            self.state = 1716
            token = self._input.LA(1)
            if token in (vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER):
                self.enterOuterAlt(localctx, 1)
                self.state = 1714
                self.scalar_nature_definition()

            elif token in (vhdlParser.ARRAY, vhdlParser.RECORD):
                self.enterOuterAlt(localctx, 2)
                self.state = 1715
                self.composite_nature_definition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Nature_element_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def element_subnature_definition(self):
            return self.getTypedRuleContext(vhdlParser.Element_subnature_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_nature_element_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterNature_element_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitNature_element_declaration(self)




    def nature_element_declaration(self):

        localctx = vhdlParser.Nature_element_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 308, self.RULE_nature_element_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1718
            self.identifier_list()
            self.state = 1719
            self.match(vhdlParser.COLON)
            self.state = 1720
            self.element_subnature_definition()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Next_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEXT(self):
            return self.getToken(vhdlParser.NEXT, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def condition(self):
            return self.getTypedRuleContext(vhdlParser.ConditionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_next_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterNext_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitNext_statement(self)




    def next_statement(self):

        localctx = vhdlParser.Next_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 310, self.RULE_next_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1723
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1722
                self.label_colon()


            self.state = 1725
            self.match(vhdlParser.NEXT)
            self.state = 1727
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1726
                self.identifier()


            self.state = 1731
            _la = self._input.LA(1)
            if _la == vhdlParser.WHEN:
                self.state = 1729
                self.match(vhdlParser.WHEN)
                self.state = 1730
                self.condition()


            self.state = 1733
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Numeric_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def abstract_literal(self):
            return self.getTypedRuleContext(vhdlParser.Abstract_literalContext, 0)


        def physical_literal(self):
            return self.getTypedRuleContext(vhdlParser.Physical_literalContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_numeric_literal

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterNumeric_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitNumeric_literal(self)




    def numeric_literal(self):

        localctx = vhdlParser.Numeric_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 312, self.RULE_numeric_literal)
        try:
            self.state = 1737
            la_ = self._interp.adaptivePredict(self._input, 178, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1735
                self.abstract_literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1736
                self.physical_literal()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Object_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def signal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Signal_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def terminal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Terminal_declarationContext, 0)


        def quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Quantity_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_object_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterObject_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitObject_declaration(self)




    def object_declaration(self):

        localctx = vhdlParser.Object_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 314, self.RULE_object_declaration)
        try:
            self.state = 1745
            token = self._input.LA(1)
            if token in (vhdlParser.CONSTANT,):
                self.enterOuterAlt(localctx, 1)
                self.state = 1739
                self.constant_declaration()

            elif token in (vhdlParser.SIGNAL,):
                self.enterOuterAlt(localctx, 2)
                self.state = 1740
                self.signal_declaration()

            elif token in (vhdlParser.SHARED, vhdlParser.VARIABLE):
                self.enterOuterAlt(localctx, 3)
                self.state = 1741
                self.variable_declaration()

            elif token in (vhdlParser.FILE,):
                self.enterOuterAlt(localctx, 4)
                self.state = 1742
                self.file_declaration()

            elif token in (vhdlParser.TERMINAL,):
                self.enterOuterAlt(localctx, 5)
                self.state = 1743
                self.terminal_declaration()

            elif token in (vhdlParser.QUANTITY,):
                self.enterOuterAlt(localctx, 6)
                self.state = 1744
                self.quantity_declaration()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GUARDED(self):
            return self.getToken(vhdlParser.GUARDED, 0)

        def delay_mechanism(self):
            return self.getTypedRuleContext(vhdlParser.Delay_mechanismContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_opts

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterOpts(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitOpts(self)




    def opts(self):

        localctx = vhdlParser.OptsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 316, self.RULE_opts)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1748
            _la = self._input.LA(1)
            if _la == vhdlParser.GUARDED:
                self.state = 1747
                self.match(vhdlParser.GUARDED)


            self.state = 1751
            _la = self._input.LA(1)
            if ((((_la - 39)) & ~0x3f) == 0 and ((1 << (_la - 39)) & ((1 << (vhdlParser.INERTIAL - 39)) | (1 << (vhdlParser.REJECT - 39)) | (1 << (vhdlParser.TRANSPORT - 39)))) != 0):
                self.state = 1750
                self.delay_mechanism()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_bodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PACKAGE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.PACKAGE)
            else:
                return self.getToken(vhdlParser.PACKAGE, i)

        def BODY(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.BODY)
            else:
                return self.getToken(vhdlParser.BODY, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def package_body_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Package_body_declarative_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_package_body

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_body(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_body(self)




    def package_body(self):

        localctx = vhdlParser.Package_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 318, self.RULE_package_body)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1753
            self.match(vhdlParser.PACKAGE)
            self.state = 1754
            self.match(vhdlParser.BODY)
            self.state = 1755
            self.identifier()
            self.state = 1756
            self.match(vhdlParser.IS)
            self.state = 1757
            self.package_body_declarative_part()
            self.state = 1758
            self.match(vhdlParser.END)
            self.state = 1761
            _la = self._input.LA(1)
            if _la == vhdlParser.PACKAGE:
                self.state = 1759
                self.match(vhdlParser.PACKAGE)
                self.state = 1760
                self.match(vhdlParser.BODY)


            self.state = 1764
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1763
                self.identifier()


            self.state = 1766
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_body_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_package_body_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_body_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_body_declarative_item(self)




    def package_body_declarative_item(self):

        localctx = vhdlParser.Package_body_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 320, self.RULE_package_body_declarative_item)
        try:
            self.state = 1779
            la_ = self._interp.adaptivePredict(self._input, 184, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1768
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1769
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1770
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1771
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1772
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1773
                self.variable_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1774
                self.file_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1775
                self.alias_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1776
                self.use_clause()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1777
                self.group_template_declaration()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1778
                self.group_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_body_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def package_body_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Package_body_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Package_body_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_package_body_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_body_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_body_declarative_part(self)




    def package_body_declarative_part(self):

        localctx = vhdlParser.Package_body_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 322, self.RULE_package_body_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1784
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1781
                self.package_body_declarative_item()
                self.state = 1786
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PACKAGE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.PACKAGE)
            else:
                return self.getToken(vhdlParser.PACKAGE, i)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(vhdlParser.IdentifierContext, i)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def package_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Package_declarative_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_package_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_declaration(self)




    def package_declaration(self):

        localctx = vhdlParser.Package_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 324, self.RULE_package_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1787
            self.match(vhdlParser.PACKAGE)
            self.state = 1788
            self.identifier()
            self.state = 1789
            self.match(vhdlParser.IS)
            self.state = 1790
            self.package_declarative_part()
            self.state = 1791
            self.match(vhdlParser.END)
            self.state = 1793
            _la = self._input.LA(1)
            if _la == vhdlParser.PACKAGE:
                self.state = 1792
                self.match(vhdlParser.PACKAGE)


            self.state = 1796
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1795
                self.identifier()


            self.state = 1798
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def signal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Signal_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def component_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Component_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def disconnection_specification(self):
            return self.getTypedRuleContext(vhdlParser.Disconnection_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def nature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Nature_declarationContext, 0)


        def subnature_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_declarationContext, 0)


        def terminal_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Terminal_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_package_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_declarative_item(self)




    def package_declarative_item(self):

        localctx = vhdlParser.Package_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 326, self.RULE_package_declarative_item)
        try:
            self.state = 1818
            la_ = self._interp.adaptivePredict(self._input, 188, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1800
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1801
                self.type_declaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1802
                self.subtype_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1803
                self.constant_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1804
                self.signal_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1805
                self.variable_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1806
                self.file_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1807
                self.alias_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1808
                self.component_declaration()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1809
                self.attribute_declaration()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1810
                self.attribute_specification()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 1811
                self.disconnection_specification()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 1812
                self.use_clause()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 1813
                self.group_template_declaration()
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 1814
                self.group_declaration()
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 1815
                self.nature_declaration()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 1816
                self.subnature_declaration()
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 1817
                self.terminal_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Package_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def package_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Package_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Package_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_package_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPackage_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPackage_declarative_part(self)




    def package_declarative_part(self):

        localctx = vhdlParser.Package_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 328, self.RULE_package_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1823
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.COMPONENT) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.DISCONNECT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE) | (1 << vhdlParser.NATURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SIGNAL - 68)) | (1 << (vhdlParser.SUBNATURE - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TERMINAL - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1820
                self.package_declarative_item()
                self.state = 1825
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Parameter_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def IN(self):
            return self.getToken(vhdlParser.IN, 0)

        def discrete_range(self):
            return self.getTypedRuleContext(vhdlParser.Discrete_rangeContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_parameter_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterParameter_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitParameter_specification(self)




    def parameter_specification(self):

        localctx = vhdlParser.Parameter_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 330, self.RULE_parameter_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1826
            self.identifier()
            self.state = 1827
            self.match(vhdlParser.IN)
            self.state = 1828
            self.discrete_range()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Physical_literalContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def abstract_literal(self):
            return self.getTypedRuleContext(vhdlParser.Abstract_literalContext, 0)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_physical_literal

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPhysical_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPhysical_literal(self)




    def physical_literal(self):

        localctx = vhdlParser.Physical_literalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 332, self.RULE_physical_literal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1830
            self.abstract_literal()

            self.state = 1831
            self.identifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Physical_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def range_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Range_constraintContext, 0)


        def UNITS(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.UNITS)
            else:
                return self.getToken(vhdlParser.UNITS, i)

        def base_unit_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Base_unit_declarationContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def secondary_unit_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Secondary_unit_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Secondary_unit_declarationContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_physical_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPhysical_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPhysical_type_definition(self)




    def physical_type_definition(self):

        localctx = vhdlParser.Physical_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 334, self.RULE_physical_type_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1833
            self.range_constraint()
            self.state = 1834
            self.match(vhdlParser.UNITS)
            self.state = 1835
            self.base_unit_declaration()
            self.state = 1839
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1836
                self.secondary_unit_declaration()
                self.state = 1841
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 1842
            self.match(vhdlParser.END)
            self.state = 1843
            self.match(vhdlParser.UNITS)
            self.state = 1845
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1844
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Port_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PORT(self):
            return self.getToken(vhdlParser.PORT, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def port_list(self):
            return self.getTypedRuleContext(vhdlParser.Port_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_port_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPort_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPort_clause(self)




    def port_clause(self):

        localctx = vhdlParser.Port_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 336, self.RULE_port_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1847
            self.match(vhdlParser.PORT)
            self.state = 1848
            self.match(vhdlParser.LPAREN)
            self.state = 1849
            self.port_list()
            self.state = 1850
            self.match(vhdlParser.RPAREN)
            self.state = 1851
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Port_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def interface_port_list(self):
            return self.getTypedRuleContext(vhdlParser.Interface_port_listContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_port_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPort_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPort_list(self)




    def port_list(self):

        localctx = vhdlParser.Port_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 338, self.RULE_port_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1853
            self.interface_port_list()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Port_map_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PORT(self):
            return self.getToken(vhdlParser.PORT, 0)

        def MAP(self):
            return self.getToken(vhdlParser.MAP, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def association_list(self):
            return self.getTypedRuleContext(vhdlParser.Association_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_port_map_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPort_map_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPort_map_aspect(self)




    def port_map_aspect(self):

        localctx = vhdlParser.Port_map_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 340, self.RULE_port_map_aspect)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1855
            self.match(vhdlParser.PORT)
            self.state = 1856
            self.match(vhdlParser.MAP)
            self.state = 1857
            self.match(vhdlParser.LPAREN)
            self.state = 1858
            self.association_list()
            self.state = 1859
            self.match(vhdlParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PrimaryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(vhdlParser.LiteralContext, 0)


        def qualified_expression(self):
            return self.getTypedRuleContext(vhdlParser.Qualified_expressionContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def allocator(self):
            return self.getTypedRuleContext(vhdlParser.AllocatorContext, 0)


        def aggregate(self):
            return self.getTypedRuleContext(vhdlParser.AggregateContext, 0)


        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_primary

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPrimary(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPrimary(self)




    def primary(self):

        localctx = vhdlParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 342, self.RULE_primary)
        try:
            self.state = 1870
            la_ = self._interp.adaptivePredict(self._input, 192, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1861
                self.literal()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1862
                self.qualified_expression()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1863
                self.match(vhdlParser.LPAREN)
                self.state = 1864
                self.expression()
                self.state = 1865
                self.match(vhdlParser.RPAREN)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1867
                self.allocator()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1868
                self.aggregate()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1869
                self.name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Primary_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def entity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Entity_declarationContext, 0)


        def configuration_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Configuration_declarationContext, 0)


        def package_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Package_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_primary_unit

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterPrimary_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitPrimary_unit(self)




    def primary_unit(self):

        localctx = vhdlParser.Primary_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 344, self.RULE_primary_unit)
        try:
            self.state = 1875
            token = self._input.LA(1)
            if token in (vhdlParser.ENTITY,):
                self.enterOuterAlt(localctx, 1)
                self.state = 1872
                self.entity_declaration()

            elif token in (vhdlParser.CONFIGURATION,):
                self.enterOuterAlt(localctx, 2)
                self.state = 1873
                self.configuration_declaration()

            elif token in (vhdlParser.PACKAGE,):
                self.enterOuterAlt(localctx, 3)
                self.state = 1874
                self.package_declaration()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedural_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_procedural_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedural_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedural_declarative_item(self)




    def procedural_declarative_item(self):

        localctx = vhdlParser.Procedural_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 346, self.RULE_procedural_declarative_item)
        try:
            self.state = 1889
            la_ = self._interp.adaptivePredict(self._input, 194, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1877
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1878
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1879
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1880
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1881
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1882
                self.variable_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1883
                self.alias_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1884
                self.attribute_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1885
                self.attribute_specification()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1886
                self.use_clause()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1887
                self.group_template_declaration()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 1888
                self.group_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedural_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procedural_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Procedural_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Procedural_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_procedural_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedural_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedural_declarative_part(self)




    def procedural_declarative_part(self):

        localctx = vhdlParser.Procedural_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 348, self.RULE_procedural_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1894
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1891
                self.procedural_declarative_item()
                self.state = 1896
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedural_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sequential_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Sequential_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Sequential_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_procedural_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedural_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedural_statement_part(self)




    def procedural_statement_part(self):

        localctx = vhdlParser.Procedural_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 350, self.RULE_procedural_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1900
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.EXIT) | (1 << vhdlParser.FOR) | (1 << vhdlParser.IF) | (1 << vhdlParser.LOOP) | (1 << vhdlParser.NEXT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & ((1 << (vhdlParser.REPORT - 79)) | (1 << (vhdlParser.RETURN - 79)) | (1 << (vhdlParser.WAIT - 79)) | (1 << (vhdlParser.WHILE - 79)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 79)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 79)) | (1 << (vhdlParser.LPAREN - 79)))) != 0):
                self.state = 1897
                self.sequential_statement()
                self.state = 1902
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedure_callContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selected_name(self):
            return self.getTypedRuleContext(vhdlParser.Selected_nameContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def actual_parameter_part(self):
            return self.getTypedRuleContext(vhdlParser.Actual_parameter_partContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_procedure_call

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedure_call(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedure_call(self)




    def procedure_call(self):

        localctx = vhdlParser.Procedure_callContext(self, self._ctx, self.state)
        self.enterRule(localctx, 352, self.RULE_procedure_call)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1903
            self.selected_name()
            self.state = 1908
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 1904
                self.match(vhdlParser.LPAREN)
                self.state = 1905
                self.actual_parameter_part()
                self.state = 1906
                self.match(vhdlParser.RPAREN)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedure_call_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procedure_call(self):
            return self.getTypedRuleContext(vhdlParser.Procedure_callContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_procedure_call_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedure_call_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedure_call_statement(self)




    def procedure_call_statement(self):

        localctx = vhdlParser.Procedure_call_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 354, self.RULE_procedure_call_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1911
            la_ = self._interp.adaptivePredict(self._input, 198, self._ctx)
            if la_ == 1:
                self.state = 1910
                self.label_colon()


            self.state = 1913
            self.procedure_call()
            self.state = 1914
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Process_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_process_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcess_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcess_declarative_item(self)




    def process_declarative_item(self):

        localctx = vhdlParser.Process_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 356, self.RULE_process_declarative_item)
        try:
            self.state = 1929
            la_ = self._interp.adaptivePredict(self._input, 199, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1916
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1917
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1918
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 1919
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 1920
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 1921
                self.variable_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 1922
                self.file_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 1923
                self.alias_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 1924
                self.attribute_declaration()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 1925
                self.attribute_specification()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 1926
                self.use_clause()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 1927
                self.group_template_declaration()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 1928
                self.group_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Process_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def process_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Process_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Process_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_process_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcess_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcess_declarative_part(self)




    def process_declarative_part(self):

        localctx = vhdlParser.Process_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 358, self.RULE_process_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1934
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 1931
                self.process_declarative_item()
                self.state = 1936
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Process_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCESS(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.PROCESS)
            else:
                return self.getToken(vhdlParser.PROCESS, i)

        def process_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Process_declarative_partContext, 0)


        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def process_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Process_statement_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def POSTPONED(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.POSTPONED)
            else:
                return self.getToken(vhdlParser.POSTPONED, i)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def sensitivity_list(self):
            return self.getTypedRuleContext(vhdlParser.Sensitivity_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_process_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcess_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcess_statement(self)




    def process_statement(self):

        localctx = vhdlParser.Process_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 360, self.RULE_process_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1938
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1937
                self.label_colon()


            self.state = 1941
            _la = self._input.LA(1)
            if _la == vhdlParser.POSTPONED:
                self.state = 1940
                self.match(vhdlParser.POSTPONED)


            self.state = 1943
            self.match(vhdlParser.PROCESS)
            self.state = 1948
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 1944
                self.match(vhdlParser.LPAREN)
                self.state = 1945
                self.sensitivity_list()
                self.state = 1946
                self.match(vhdlParser.RPAREN)


            self.state = 1951
            _la = self._input.LA(1)
            if _la == vhdlParser.IS:
                self.state = 1950
                self.match(vhdlParser.IS)


            self.state = 1953
            self.process_declarative_part()
            self.state = 1954
            self.match(vhdlParser.BEGIN)
            self.state = 1955
            self.process_statement_part()
            self.state = 1956
            self.match(vhdlParser.END)
            self.state = 1958
            _la = self._input.LA(1)
            if _la == vhdlParser.POSTPONED:
                self.state = 1957
                self.match(vhdlParser.POSTPONED)


            self.state = 1960
            self.match(vhdlParser.PROCESS)
            self.state = 1962
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 1961
                self.identifier()


            self.state = 1964
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Process_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sequential_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Sequential_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Sequential_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_process_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcess_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcess_statement_part(self)




    def process_statement_part(self):

        localctx = vhdlParser.Process_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 362, self.RULE_process_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1969
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.EXIT) | (1 << vhdlParser.FOR) | (1 << vhdlParser.IF) | (1 << vhdlParser.LOOP) | (1 << vhdlParser.NEXT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & ((1 << (vhdlParser.REPORT - 79)) | (1 << (vhdlParser.RETURN - 79)) | (1 << (vhdlParser.WAIT - 79)) | (1 << (vhdlParser.WHILE - 79)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 79)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 79)) | (1 << (vhdlParser.LPAREN - 79)))) != 0):
                self.state = 1966
                self.sequential_statement()
                self.state = 1971
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Qualified_expressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def APOSTROPHE(self):
            return self.getToken(vhdlParser.APOSTROPHE, 0)

        def aggregate(self):
            return self.getTypedRuleContext(vhdlParser.AggregateContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_qualified_expression

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterQualified_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitQualified_expression(self)




    def qualified_expression(self):

        localctx = vhdlParser.Qualified_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 364, self.RULE_qualified_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1972
            self.subtype_indication()
            self.state = 1973
            self.match(vhdlParser.APOSTROPHE)
            self.state = 1979
            la_ = self._interp.adaptivePredict(self._input, 208, self._ctx)
            if la_ == 1:
                self.state = 1974
                self.aggregate()
                pass

            elif la_ == 2:
                self.state = 1975
                self.match(vhdlParser.LPAREN)
                self.state = 1976
                self.expression()
                self.state = 1977
                self.match(vhdlParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Quantity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def free_quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Free_quantity_declarationContext, 0)


        def branch_quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Branch_quantity_declarationContext, 0)


        def source_quantity_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Source_quantity_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_quantity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterQuantity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitQuantity_declaration(self)




    def quantity_declaration(self):

        localctx = vhdlParser.Quantity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 366, self.RULE_quantity_declaration)
        try:
            self.state = 1984
            la_ = self._interp.adaptivePredict(self._input, 209, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 1981
                self.free_quantity_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 1982
                self.branch_quantity_declaration()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 1983
                self.source_quantity_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Quantity_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def OTHERS(self):
            return self.getToken(vhdlParser.OTHERS, 0)

        def ALL(self):
            return self.getToken(vhdlParser.ALL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_quantity_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterQuantity_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitQuantity_list(self)




    def quantity_list(self):

        localctx = vhdlParser.Quantity_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 368, self.RULE_quantity_list)
        self._la = 0  # Token type
        try:
            self.state = 1996
            token = self._input.LA(1)
            if token in (vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER,):
                self.enterOuterAlt(localctx, 1)
                self.state = 1986
                self.name()
                self.state = 1991
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 1987
                    self.match(vhdlParser.COMMA)
                    self.state = 1988
                    self.name()
                    self.state = 1993
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in (vhdlParser.OTHERS, ):
                self.enterOuterAlt(localctx, 2)
                self.state = 1994
                self.match(vhdlParser.OTHERS)

            elif token == vhdlParser.ALL:
                self.enterOuterAlt(localctx, 3)
                self.state = 1995
                self.match(vhdlParser.ALL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Quantity_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def quantity_list(self):
            return self.getTypedRuleContext(vhdlParser.Quantity_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_quantity_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterQuantity_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitQuantity_specification(self)




    def quantity_specification(self):

        localctx = vhdlParser.Quantity_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 370, self.RULE_quantity_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 1998
            self.quantity_list()
            self.state = 1999
            self.match(vhdlParser.COLON)
            self.state = 2000
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RangeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def explicit_range(self):
            return self.getTypedRuleContext(vhdlParser.Explicit_rangeContext, 0)


        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_range

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRange(self)




    def range(self):

        localctx = vhdlParser.RangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 372, self.RULE_range)
        try:
            self.state = 2004
            la_ = self._interp.adaptivePredict(self._input, 212, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2002
                self.explicit_range()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2003
                self.name()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Explicit_rangeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simple_expressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simple_expressionContext, i)


        def direction(self):
            return self.getTypedRuleContext(vhdlParser.DirectionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_explicit_range

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterExplicit_range(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitExplicit_range(self)




    def explicit_range(self):

        localctx = vhdlParser.Explicit_rangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 374, self.RULE_explicit_range)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2006
            self.simple_expression()
            self.state = 2007
            self.direction()
            self.state = 2008
            self.simple_expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Range_constraintContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RANGE(self):
            return self.getToken(vhdlParser.RANGE, 0)

        def range(self):
            return self.getTypedRuleContext(vhdlParser.RangeContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_range_constraint

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRange_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRange_constraint(self)




    def range_constraint(self):

        localctx = vhdlParser.Range_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 376, self.RULE_range_constraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2010
            self.match(vhdlParser.RANGE)
            self.state = 2011
            self.range()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Record_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RECORD(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.RECORD)
            else:
                return self.getToken(vhdlParser.RECORD, i)

        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def nature_element_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Nature_element_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Nature_element_declarationContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_record_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRecord_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRecord_nature_definition(self)




    def record_nature_definition(self):

        localctx = vhdlParser.Record_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 378, self.RULE_record_nature_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2013
            self.match(vhdlParser.RECORD)
            self.state = 2015 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 2014
                self.nature_element_declaration()
                self.state = 2017 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER):
                    break

            self.state = 2019
            self.match(vhdlParser.END)
            self.state = 2020
            self.match(vhdlParser.RECORD)
            self.state = 2022
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2021
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Record_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RECORD(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.RECORD)
            else:
                return self.getToken(vhdlParser.RECORD, i)

        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def element_declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Element_declarationContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Element_declarationContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_record_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRecord_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRecord_type_definition(self)




    def record_type_definition(self):

        localctx = vhdlParser.Record_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 380, self.RULE_record_type_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2024
            self.match(vhdlParser.RECORD)
            self.state = 2026 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 2025
                self.element_declaration()
                self.state = 2028 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER):
                    break

            self.state = 2030
            self.match(vhdlParser.END)
            self.state = 2031
            self.match(vhdlParser.RECORD)
            self.state = 2033
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2032
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RelationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def shift_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Shift_expressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Shift_expressionContext, i)


        def relational_operator(self):
            return self.getTypedRuleContext(vhdlParser.Relational_operatorContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRelation(self)




    def relation(self):

        localctx = vhdlParser.RelationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 382, self.RULE_relation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2035
            self.shift_expression()
            self.state = 2039
            la_ = self._interp.adaptivePredict(self._input, 217, self._ctx)
            if la_ == 1:
                self.state = 2036
                self.relational_operator()
                self.state = 2037
                self.shift_expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Relational_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(vhdlParser.EQ, 0)

        def NEQ(self):
            return self.getToken(vhdlParser.NEQ, 0)

        def LOWERTHAN(self):
            return self.getToken(vhdlParser.LOWERTHAN, 0)

        def LE(self):
            return self.getToken(vhdlParser.LE, 0)

        def GREATERTHAN(self):
            return self.getToken(vhdlParser.GREATERTHAN, 0)

        def GE(self):
            return self.getToken(vhdlParser.GE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_relational_operator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterRelational_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitRelational_operator(self)




    def relational_operator(self):

        localctx = vhdlParser.Relational_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 384, self.RULE_relational_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2041
            _la = self._input.LA(1)
            if not(((((_la - 131)) & ~0x3f) == 0 and ((1 << (_la - 131)) & ((1 << (vhdlParser.LE - 131)) | (1 << (vhdlParser.GE - 131)) | (1 << (vhdlParser.NEQ - 131)) | (1 << (vhdlParser.LOWERTHAN - 131)) | (1 << (vhdlParser.GREATERTHAN - 131)) | (1 << (vhdlParser.EQ - 131)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Report_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPORT(self):
            return self.getToken(vhdlParser.REPORT, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ExpressionContext, i)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def SEVERITY(self):
            return self.getToken(vhdlParser.SEVERITY, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_report_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterReport_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitReport_statement(self)




    def report_statement(self):

        localctx = vhdlParser.Report_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 386, self.RULE_report_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2044
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2043
                self.label_colon()


            self.state = 2046
            self.match(vhdlParser.REPORT)
            self.state = 2047
            self.expression()
            self.state = 2050
            _la = self._input.LA(1)
            if _la == vhdlParser.SEVERITY:
                self.state = 2048
                self.match(vhdlParser.SEVERITY)
                self.state = 2049
                self.expression()


            self.state = 2052
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Return_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(vhdlParser.RETURN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_return_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterReturn_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitReturn_statement(self)




    def return_statement(self):

        localctx = vhdlParser.Return_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 388, self.RULE_return_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2055
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2054
                self.label_colon()


            self.state = 2057
            self.match(vhdlParser.RETURN)
            self.state = 2059
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 112)) & ~0x3f) == 0 and ((1 << (_la - 112)) & ((1 << (vhdlParser.BASE_LITERAL - 112)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 112)) | (1 << (vhdlParser.REAL_LITERAL - 112)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 112)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 112)) | (1 << (vhdlParser.CHARACTER_LITERAL - 112)) | (1 << (vhdlParser.STRING_LITERAL - 112)) | (1 << (vhdlParser.LPAREN - 112)) | (1 << (vhdlParser.PLUS - 112)) | (1 << (vhdlParser.MINUS - 112)) | (1 << (vhdlParser.INTEGER - 112)))) != 0):
                self.state = 2058
                self.expression()


            self.state = 2061
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Scalar_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def ACROSS(self):
            return self.getToken(vhdlParser.ACROSS, 0)

        def THROUGH(self):
            return self.getToken(vhdlParser.THROUGH, 0)

        def REFERENCE(self):
            return self.getToken(vhdlParser.REFERENCE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_scalar_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterScalar_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitScalar_nature_definition(self)




    def scalar_nature_definition(self):

        localctx = vhdlParser.Scalar_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 390, self.RULE_scalar_nature_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2063
            self.name()
            self.state = 2064
            self.match(vhdlParser.ACROSS)
            self.state = 2065
            self.name()
            self.state = 2066
            self.match(vhdlParser.THROUGH)
            self.state = 2067
            self.name()
            self.state = 2068
            self.match(vhdlParser.REFERENCE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Scalar_type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def physical_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Physical_type_definitionContext, 0)


        def enumeration_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Enumeration_type_definitionContext, 0)


        def range_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Range_constraintContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_scalar_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterScalar_type_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitScalar_type_definition(self)




    def scalar_type_definition(self):

        localctx = vhdlParser.Scalar_type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 392, self.RULE_scalar_type_definition)
        try:
            self.state = 2073
            la_ = self._interp.adaptivePredict(self._input, 222, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2070
                self.physical_type_definition()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2071
                self.enumeration_type_definition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2072
                self.range_constraint()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Secondary_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def architecture_body(self):
            return self.getTypedRuleContext(vhdlParser.Architecture_bodyContext, 0)


        def package_body(self):
            return self.getTypedRuleContext(vhdlParser.Package_bodyContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_secondary_unit

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSecondary_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSecondary_unit(self)




    def secondary_unit(self):

        localctx = vhdlParser.Secondary_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 394, self.RULE_secondary_unit)
        try:
            self.state = 2077
            token = self._input.LA(1)
            if token == vhdlParser.ARCHITECTURE:
                self.enterOuterAlt(localctx, 1)
                self.state = 2075
                self.architecture_body()

            elif token == vhdlParser.PACKAGE:
                self.enterOuterAlt(localctx, 2)
                self.state = 2076
                self.package_body()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Secondary_unit_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def EQ(self):
            return self.getToken(vhdlParser.EQ, 0)

        def physical_literal(self):
            return self.getTypedRuleContext(vhdlParser.Physical_literalContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_secondary_unit_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSecondary_unit_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSecondary_unit_declaration(self)




    def secondary_unit_declaration(self):

        localctx = vhdlParser.Secondary_unit_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 396, self.RULE_secondary_unit_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2079
            self.identifier()
            self.state = 2080
            self.match(vhdlParser.EQ)
            self.state = 2081
            self.physical_literal()
            self.state = 2082
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Selected_signal_assignmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WITH(self):
            return self.getToken(vhdlParser.WITH, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def SELECT(self):
            return self.getToken(vhdlParser.SELECT, 0)

        def target(self):
            return self.getTypedRuleContext(vhdlParser.TargetContext, 0)


        def LE(self):
            return self.getToken(vhdlParser.LE, 0)

        def opts(self):
            return self.getTypedRuleContext(vhdlParser.OptsContext, 0)


        def selected_waveforms(self):
            return self.getTypedRuleContext(vhdlParser.Selected_waveformsContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_selected_signal_assignment

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSelected_signal_assignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSelected_signal_assignment(self)




    def selected_signal_assignment(self):

        localctx = vhdlParser.Selected_signal_assignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 398, self.RULE_selected_signal_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2084
            self.match(vhdlParser.WITH)
            self.state = 2085
            self.expression()
            self.state = 2086
            self.match(vhdlParser.SELECT)
            self.state = 2087
            self.target()
            self.state = 2088
            self.match(vhdlParser.LE)
            self.state = 2089
            self.opts()
            self.state = 2090
            self.selected_waveforms()
            self.state = 2091
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Selected_waveformsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def waveform(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.WaveformContext)
            else:
                return self.getTypedRuleContext(vhdlParser.WaveformContext, i)


        def WHEN(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.WHEN)
            else:
                return self.getToken(vhdlParser.WHEN, i)

        def choices(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ChoicesContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ChoicesContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_selected_waveforms

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSelected_waveforms(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSelected_waveforms(self)




    def selected_waveforms(self):

        localctx = vhdlParser.Selected_waveformsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 400, self.RULE_selected_waveforms)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2093
            self.waveform()
            self.state = 2094
            self.match(vhdlParser.WHEN)
            self.state = 2095
            self.choices()
            self.state = 2103
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 2096
                self.match(vhdlParser.COMMA)
                self.state = 2097
                self.waveform()
                self.state = 2098
                self.match(vhdlParser.WHEN)
                self.state = 2099
                self.choices()
                self.state = 2105
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Sensitivity_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ON(self):
            return self.getToken(vhdlParser.ON, 0)

        def sensitivity_list(self):
            return self.getTypedRuleContext(vhdlParser.Sensitivity_listContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_sensitivity_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSensitivity_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSensitivity_clause(self)




    def sensitivity_clause(self):

        localctx = vhdlParser.Sensitivity_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 402, self.RULE_sensitivity_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2106
            self.match(vhdlParser.ON)
            self.state = 2107
            self.sensitivity_list()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Sensitivity_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_sensitivity_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSensitivity_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSensitivity_list(self)




    def sensitivity_list(self):

        localctx = vhdlParser.Sensitivity_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 404, self.RULE_sensitivity_list)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2109
            self.name()
            self.state = 2114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 2110
                self.match(vhdlParser.COMMA)
                self.state = 2111
                self.name()
                self.state = 2116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Sequence_of_statementsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sequential_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Sequential_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Sequential_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_sequence_of_statements

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSequence_of_statements(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSequence_of_statements(self)




    def sequence_of_statements(self):

        localctx = vhdlParser.Sequence_of_statementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 406, self.RULE_sequence_of_statements)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.EXIT) | (1 << vhdlParser.FOR) | (1 << vhdlParser.IF) | (1 << vhdlParser.LOOP) | (1 << vhdlParser.NEXT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & ((1 << (vhdlParser.REPORT - 79)) | (1 << (vhdlParser.RETURN - 79)) | (1 << (vhdlParser.WAIT - 79)) | (1 << (vhdlParser.WHILE - 79)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 79)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 79)) | (1 << (vhdlParser.LPAREN - 79)))) != 0):
                self.state = 2117
                self.sequential_statement()
                self.state = 2122
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Sequential_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def wait_statement(self):
            return self.getTypedRuleContext(vhdlParser.Wait_statementContext, 0)


        def assertion_statement(self):
            return self.getTypedRuleContext(vhdlParser.Assertion_statementContext, 0)


        def report_statement(self):
            return self.getTypedRuleContext(vhdlParser.Report_statementContext, 0)


        def signal_assignment_statement(self):
            return self.getTypedRuleContext(vhdlParser.Signal_assignment_statementContext, 0)


        def variable_assignment_statement(self):
            return self.getTypedRuleContext(vhdlParser.Variable_assignment_statementContext, 0)


        def if_statement(self):
            return self.getTypedRuleContext(vhdlParser.If_statementContext, 0)


        def case_statement(self):
            return self.getTypedRuleContext(vhdlParser.Case_statementContext, 0)


        def loop_statement(self):
            return self.getTypedRuleContext(vhdlParser.Loop_statementContext, 0)


        def next_statement(self):
            return self.getTypedRuleContext(vhdlParser.Next_statementContext, 0)


        def exit_statement(self):
            return self.getTypedRuleContext(vhdlParser.Exit_statementContext, 0)


        def return_statement(self):
            return self.getTypedRuleContext(vhdlParser.Return_statementContext, 0)


        def NULL(self):
            return self.getToken(vhdlParser.NULL, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def break_statement(self):
            return self.getTypedRuleContext(vhdlParser.Break_statementContext, 0)


        def procedure_call_statement(self):
            return self.getTypedRuleContext(vhdlParser.Procedure_call_statementContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_sequential_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSequential_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSequential_statement(self)




    def sequential_statement(self):

        localctx = vhdlParser.Sequential_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 408, self.RULE_sequential_statement)
        self._la = 0  # Token type
        try:
            self.state = 2141
            la_ = self._interp.adaptivePredict(self._input, 228, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2123
                self.wait_statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2124
                self.assertion_statement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2125
                self.report_statement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 2126
                self.signal_assignment_statement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 2127
                self.variable_assignment_statement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 2128
                self.if_statement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 2129
                self.case_statement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 2130
                self.loop_statement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 2131
                self.next_statement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 2132
                self.exit_statement()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 2133
                self.return_statement()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 2135
                _la = self._input.LA(1)
                if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                    self.state = 2134
                    self.label_colon()


                self.state = 2137
                self.match(vhdlParser.NULL)
                self.state = 2138
                self.match(vhdlParser.SEMI)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 2139
                self.break_statement()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 2140
                self.procedure_call_statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Shift_expressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simple_expressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simple_expressionContext, i)


        def shift_operator(self):
            return self.getTypedRuleContext(vhdlParser.Shift_operatorContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_shift_expression

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterShift_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitShift_expression(self)




    def shift_expression(self):

        localctx = vhdlParser.Shift_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 410, self.RULE_shift_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2143
            self.simple_expression()
            self.state = 2147
            la_ = self._interp.adaptivePredict(self._input, 229, self._ctx)
            if la_ == 1:
                self.state = 2144
                self.shift_operator()
                self.state = 2145
                self.simple_expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Shift_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLL(self):
            return self.getToken(vhdlParser.SLL, 0)

        def SRL(self):
            return self.getToken(vhdlParser.SRL, 0)

        def SLA(self):
            return self.getToken(vhdlParser.SLA, 0)

        def SRA(self):
            return self.getToken(vhdlParser.SRA, 0)

        def ROL(self):
            return self.getToken(vhdlParser.ROL, 0)

        def ROR(self):
            return self.getToken(vhdlParser.ROR, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_shift_operator

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterShift_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitShift_operator(self)




    def shift_operator(self):

        localctx = vhdlParser.Shift_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 412, self.RULE_shift_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2149
            _la = self._input.LA(1)
            if not(((((_la - 81)) & ~0x3f) == 0 and ((1 << (_la - 81)) & ((1 << (vhdlParser.ROL - 81)) | (1 << (vhdlParser.ROR - 81)) | (1 << (vhdlParser.SLA - 81)) | (1 << (vhdlParser.SLL - 81)) | (1 << (vhdlParser.SRA - 81)) | (1 << (vhdlParser.SRL - 81)))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Signal_assignment_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(vhdlParser.TargetContext, 0)


        def LE(self):
            return self.getToken(vhdlParser.LE, 0)

        def waveform(self):
            return self.getTypedRuleContext(vhdlParser.WaveformContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def delay_mechanism(self):
            return self.getTypedRuleContext(vhdlParser.Delay_mechanismContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_signal_assignment_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignal_assignment_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignal_assignment_statement(self)




    def signal_assignment_statement(self):

        localctx = vhdlParser.Signal_assignment_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 414, self.RULE_signal_assignment_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2152
            la_ = self._interp.adaptivePredict(self._input, 230, self._ctx)
            if la_ == 1:
                self.state = 2151
                self.label_colon()


            self.state = 2154
            self.target()
            self.state = 2155
            self.match(vhdlParser.LE)
            self.state = 2157
            _la = self._input.LA(1)
            if ((((_la - 39)) & ~0x3f) == 0 and ((1 << (_la - 39)) & ((1 << (vhdlParser.INERTIAL - 39)) | (1 << (vhdlParser.REJECT - 39)) | (1 << (vhdlParser.TRANSPORT - 39)))) != 0):
                self.state = 2156
                self.delay_mechanism()


            self.state = 2159
            self.waveform()
            self.state = 2160
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Signal_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIGNAL(self):
            return self.getToken(vhdlParser.SIGNAL, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def signal_kind(self):
            return self.getTypedRuleContext(vhdlParser.Signal_kindContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_signal_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignal_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignal_declaration(self)




    def signal_declaration(self):

        localctx = vhdlParser.Signal_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 416, self.RULE_signal_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2162
            self.match(vhdlParser.SIGNAL)
            self.state = 2163
            self.identifier_list()
            self.state = 2164
            self.match(vhdlParser.COLON)
            self.state = 2165
            self.subtype_indication()
            self.state = 2167
            _la = self._input.LA(1)
            if _la == vhdlParser.BUS or _la == vhdlParser.REGISTER:
                self.state = 2166
                self.signal_kind()


            self.state = 2171
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 2169
                self.match(vhdlParser.VARASGN)
                self.state = 2170
                self.expression()


            self.state = 2173
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Signal_kindContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGISTER(self):
            return self.getToken(vhdlParser.REGISTER, 0)

        def BUS(self):
            return self.getToken(vhdlParser.BUS, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_signal_kind

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignal_kind(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignal_kind(self)




    def signal_kind(self):

        localctx = vhdlParser.Signal_kindContext(self, self._ctx, self.state)
        self.enterRule(localctx, 418, self.RULE_signal_kind)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2175
            _la = self._input.LA(1)
            if not(_la == vhdlParser.BUS or _la == vhdlParser.REGISTER):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Signal_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def OTHERS(self):
            return self.getToken(vhdlParser.OTHERS, 0)

        def ALL(self):
            return self.getToken(vhdlParser.ALL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_signal_list

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignal_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignal_list(self)




    def signal_list(self):

        localctx = vhdlParser.Signal_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 420, self.RULE_signal_list)
        self._la = 0  # Token type
        try:
            self.state = 2187
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2177
                self.name()
                self.state = 2182
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 2178
                    self.match(vhdlParser.COMMA)
                    self.state = 2179
                    self.name()
                    self.state = 2184
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token == vhdlParser.OTHERS:
                self.enterOuterAlt(localctx, 2)
                self.state = 2185
                self.match(vhdlParser.OTHERS)

            elif token == vhdlParser.ALL:
                self.enterOuterAlt(localctx, 3)
                self.state = 2186
                self.match(vhdlParser.ALL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SignatureContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACKET(self):
            return self.getToken(vhdlParser.LBRACKET, 0)

        def RBRACKET(self):
            return self.getToken(vhdlParser.RBRACKET, 0)

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def RETURN(self):
            return self.getToken(vhdlParser.RETURN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_signature

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSignature(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSignature(self)




    def signature(self):

        localctx = vhdlParser.SignatureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 422, self.RULE_signature)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2189
            self.match(vhdlParser.LBRACKET)
            self.state = 2198
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2190
                self.name()
                self.state = 2195
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 2191
                    self.match(vhdlParser.COMMA)
                    self.state = 2192
                    self.name()
                    self.state = 2197
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 2202
            _la = self._input.LA(1)
            if _la == vhdlParser.RETURN:
                self.state = 2200
                self.match(vhdlParser.RETURN)
                self.state = 2201
                self.name()


            self.state = 2204
            self.match(vhdlParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_expressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.TermContext)
            else:
                return self.getTypedRuleContext(vhdlParser.TermContext, i)


        def adding_operator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Adding_operatorContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Adding_operatorContext, i)


        def PLUS(self):
            return self.getToken(vhdlParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(vhdlParser.MINUS, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_simple_expression

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimple_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimple_expression(self)




    def simple_expression(self):

        localctx = vhdlParser.Simple_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 424, self.RULE_simple_expression)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2207
            _la = self._input.LA(1)
            if _la == vhdlParser.PLUS or _la == vhdlParser.MINUS:
                self.state = 2206
                _la = self._input.LA(1)
                if not(_la == vhdlParser.PLUS or _la == vhdlParser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()


            self.state = 2209
            self.term()
            self.state = 2215
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 240, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 2210
                    self.adding_operator()
                    self.state = 2211
                    self.term() 
                self.state = 2217
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 240, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_simultaneous_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simple_expressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simple_expressionContext, i)


        def ASSIGN(self):
            return self.getToken(vhdlParser.ASSIGN, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def tolerance_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Tolerance_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simple_simultaneous_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimple_simultaneous_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimple_simultaneous_statement(self)




    def simple_simultaneous_statement(self):

        localctx = vhdlParser.Simple_simultaneous_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 426, self.RULE_simple_simultaneous_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2219
            la_ = self._interp.adaptivePredict(self._input, 241, self._ctx)
            if la_ == 1:
                self.state = 2218
                self.label_colon()


            self.state = 2221
            self.simple_expression()
            self.state = 2222
            self.match(vhdlParser.ASSIGN)
            self.state = 2223
            self.simple_expression()
            self.state = 2225
            _la = self._input.LA(1)
            if _la == vhdlParser.TOLERANCE:
                self.state = 2224
                self.tolerance_aspect()


            self.state = 2227
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_alternativeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHEN(self):
            return self.getToken(vhdlParser.WHEN, 0)

        def choices(self):
            return self.getTypedRuleContext(vhdlParser.ChoicesContext, 0)


        def ARROW(self):
            return self.getToken(vhdlParser.ARROW, 0)

        def simultaneous_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Simultaneous_statement_partContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_alternative

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_alternative(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_alternative(self)




    def simultaneous_alternative(self):

        localctx = vhdlParser.Simultaneous_alternativeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 428, self.RULE_simultaneous_alternative)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2229
            self.match(vhdlParser.WHEN)
            self.state = 2230
            self.choices()
            self.state = 2231
            self.match(vhdlParser.ARROW)
            self.state = 2232
            self.simultaneous_statement_part()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_case_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CASE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.CASE)
            else:
                return self.getToken(vhdlParser.CASE, i)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def USE(self):
            return self.getToken(vhdlParser.USE, 0)

        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def simultaneous_alternative(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simultaneous_alternativeContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simultaneous_alternativeContext, i)


        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_case_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_case_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_case_statement(self)




    def simultaneous_case_statement(self):

        localctx = vhdlParser.Simultaneous_case_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 430, self.RULE_simultaneous_case_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2235
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2234
                self.label_colon()


            self.state = 2237
            self.match(vhdlParser.CASE)
            self.state = 2238
            self.expression()
            self.state = 2239
            self.match(vhdlParser.USE)
            self.state = 2241 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 2240
                self.simultaneous_alternative()
                self.state = 2243 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la == vhdlParser.WHEN):
                    break

            self.state = 2245
            self.match(vhdlParser.END)
            self.state = 2246
            self.match(vhdlParser.CASE)
            self.state = 2248
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2247
                self.identifier()


            self.state = 2250
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_if_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(vhdlParser.IF, 0)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ConditionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ConditionContext, i)


        def USE(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.USE)
            else:
                return self.getToken(vhdlParser.USE, i)

        def simultaneous_statement_part(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simultaneous_statement_partContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simultaneous_statement_partContext, i)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def ELSIF(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.ELSIF)
            else:
                return self.getToken(vhdlParser.ELSIF, i)

        def ELSE(self):
            return self.getToken(vhdlParser.ELSE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_if_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_if_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_if_statement(self)




    def simultaneous_if_statement(self):

        localctx = vhdlParser.Simultaneous_if_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 432, self.RULE_simultaneous_if_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2253
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2252
                self.label_colon()


            self.state = 2255
            self.match(vhdlParser.IF)
            self.state = 2256
            self.condition()
            self.state = 2257
            self.match(vhdlParser.USE)
            self.state = 2258
            self.simultaneous_statement_part()
            self.state = 2266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.ELSIF:
                self.state = 2259
                self.match(vhdlParser.ELSIF)
                self.state = 2260
                self.condition()
                self.state = 2261
                self.match(vhdlParser.USE)
                self.state = 2262
                self.simultaneous_statement_part()
                self.state = 2268
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2271
            _la = self._input.LA(1)
            if _la == vhdlParser.ELSE:
                self.state = 2269
                self.match(vhdlParser.ELSE)
                self.state = 2270
                self.simultaneous_statement_part()


            self.state = 2273
            self.match(vhdlParser.END)
            self.state = 2274
            self.match(vhdlParser.USE)
            self.state = 2276
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2275
                self.identifier()


            self.state = 2278
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_procedural_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCEDURAL(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.PROCEDURAL)
            else:
                return self.getToken(vhdlParser.PROCEDURAL, i)

        def procedural_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Procedural_declarative_partContext, 0)


        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def procedural_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Procedural_statement_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_procedural_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_procedural_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_procedural_statement(self)




    def simultaneous_procedural_statement(self):

        localctx = vhdlParser.Simultaneous_procedural_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 434, self.RULE_simultaneous_procedural_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2281
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2280
                self.label_colon()


            self.state = 2283
            self.match(vhdlParser.PROCEDURAL)
            self.state = 2285
            _la = self._input.LA(1)
            if _la == vhdlParser.IS:
                self.state = 2284
                self.match(vhdlParser.IS)


            self.state = 2287
            self.procedural_declarative_part()
            self.state = 2288
            self.match(vhdlParser.BEGIN)
            self.state = 2289
            self.procedural_statement_part()
            self.state = 2290
            self.match(vhdlParser.END)
            self.state = 2291
            self.match(vhdlParser.PROCEDURAL)
            self.state = 2293
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2292
                self.identifier()


            self.state = 2295
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_simultaneous_statement(self):
            return self.getTypedRuleContext(vhdlParser.Simple_simultaneous_statementContext, 0)


        def simultaneous_if_statement(self):
            return self.getTypedRuleContext(vhdlParser.Simultaneous_if_statementContext, 0)


        def simultaneous_case_statement(self):
            return self.getTypedRuleContext(vhdlParser.Simultaneous_case_statementContext, 0)


        def simultaneous_procedural_statement(self):
            return self.getTypedRuleContext(vhdlParser.Simultaneous_procedural_statementContext, 0)


        def NULL(self):
            return self.getToken(vhdlParser.NULL, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_statement(self)




    def simultaneous_statement(self):

        localctx = vhdlParser.Simultaneous_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 436, self.RULE_simultaneous_statement)
        self._la = 0  # Token type
        try:
            self.state = 2306
            la_ = self._interp.adaptivePredict(self._input, 254, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2297
                self.simple_simultaneous_statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2298
                self.simultaneous_if_statement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2299
                self.simultaneous_case_statement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 2300
                self.simultaneous_procedural_statement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 2302
                _la = self._input.LA(1)
                if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                    self.state = 2301
                    self.label_colon()


                self.state = 2304
                self.match(vhdlParser.NULL)
                self.state = 2305
                self.match(vhdlParser.SEMI)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simultaneous_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simultaneous_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simultaneous_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simultaneous_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_simultaneous_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSimultaneous_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSimultaneous_statement_part(self)




    def simultaneous_statement_part(self):

        localctx = vhdlParser.Simultaneous_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 438, self.RULE_simultaneous_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2311
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ABS) | (1 << vhdlParser.CASE) | (1 << vhdlParser.IF) | (1 << vhdlParser.NEW) | (1 << vhdlParser.NOT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (vhdlParser.PROCEDURAL - 69)) | (1 << (vhdlParser.BASE_LITERAL - 69)) | (1 << (vhdlParser.BIT_STRING_LITERAL - 69)) | (1 << (vhdlParser.REAL_LITERAL - 69)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 69)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 69)) | (1 << (vhdlParser.CHARACTER_LITERAL - 69)) | (1 << (vhdlParser.STRING_LITERAL - 69)))) != 0) or ((((_la - 141)) & ~0x3f) == 0 and ((1 << (_la - 141)) & ((1 << (vhdlParser.LPAREN - 141)) | (1 << (vhdlParser.PLUS - 141)) | (1 << (vhdlParser.MINUS - 141)) | (1 << (vhdlParser.INTEGER - 141)))) != 0):
                self.state = 2308
                self.simultaneous_statement()
                self.state = 2313
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Source_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPECTRUM(self):
            return self.getToken(vhdlParser.SPECTRUM, 0)

        def simple_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Simple_expressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Simple_expressionContext, i)


        def COMMA(self):
            return self.getToken(vhdlParser.COMMA, 0)

        def NOISE(self):
            return self.getToken(vhdlParser.NOISE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_source_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSource_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSource_aspect(self)




    def source_aspect(self):

        localctx = vhdlParser.Source_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 440, self.RULE_source_aspect)
        try:
            self.state = 2321
            token = self._input.LA(1)
            if token == vhdlParser.SPECTRUM:
                self.enterOuterAlt(localctx, 1)
                self.state = 2314
                self.match(vhdlParser.SPECTRUM)
                self.state = 2315
                self.simple_expression()
                self.state = 2316
                self.match(vhdlParser.COMMA)
                self.state = 2317
                self.simple_expression()

            elif token == vhdlParser.NOISE:
                self.enterOuterAlt(localctx, 2)
                self.state = 2319
                self.match(vhdlParser.NOISE)
                self.state = 2320
                self.simple_expression()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Source_quantity_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUANTITY(self):
            return self.getToken(vhdlParser.QUANTITY, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def source_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Source_aspectContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_source_quantity_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSource_quantity_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSource_quantity_declaration(self)




    def source_quantity_declaration(self):

        localctx = vhdlParser.Source_quantity_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 442, self.RULE_source_quantity_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2323
            self.match(vhdlParser.QUANTITY)
            self.state = 2324
            self.identifier_list()
            self.state = 2325
            self.match(vhdlParser.COLON)
            self.state = 2326
            self.subtype_indication()
            self.state = 2327
            self.source_aspect()
            self.state = 2328
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Step_limit_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LIMIT(self):
            return self.getToken(vhdlParser.LIMIT, 0)

        def quantity_specification(self):
            return self.getTypedRuleContext(vhdlParser.Quantity_specificationContext, 0)


        def WITH(self):
            return self.getToken(vhdlParser.WITH, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_step_limit_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterStep_limit_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitStep_limit_specification(self)




    def step_limit_specification(self):

        localctx = vhdlParser.Step_limit_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 444, self.RULE_step_limit_specification)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2330
            self.match(vhdlParser.LIMIT)
            self.state = 2331
            self.quantity_specification()
            self.state = 2332
            self.match(vhdlParser.WITH)
            self.state = 2333
            self.expression()
            self.state = 2334
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subnature_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SUBNATURE(self):
            return self.getToken(vhdlParser.SUBNATURE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_subnature_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubnature_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubnature_declaration(self)




    def subnature_declaration(self):

        localctx = vhdlParser.Subnature_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 446, self.RULE_subnature_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2336
            self.match(vhdlParser.SUBNATURE)
            self.state = 2337
            self.identifier()
            self.state = 2338
            self.match(vhdlParser.IS)
            self.state = 2339
            self.subnature_indication()
            self.state = 2340
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subnature_indicationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def index_constraint(self):
            return self.getTypedRuleContext(vhdlParser.Index_constraintContext, 0)


        def TOLERANCE(self):
            return self.getToken(vhdlParser.TOLERANCE, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ExpressionContext, i)


        def ACROSS(self):
            return self.getToken(vhdlParser.ACROSS, 0)

        def THROUGH(self):
            return self.getToken(vhdlParser.THROUGH, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_subnature_indication

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubnature_indication(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubnature_indication(self)




    def subnature_indication(self):

        localctx = vhdlParser.Subnature_indicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 448, self.RULE_subnature_indication)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2342
            self.name()
            self.state = 2344
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 2343
                self.index_constraint()


            self.state = 2352
            _la = self._input.LA(1)
            if _la == vhdlParser.TOLERANCE:
                self.state = 2346
                self.match(vhdlParser.TOLERANCE)
                self.state = 2347
                self.expression()
                self.state = 2348
                self.match(vhdlParser.ACROSS)
                self.state = 2349
                self.expression()
                self.state = 2350
                self.match(vhdlParser.THROUGH)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_bodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_specification(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_specificationContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def subprogram_declarative_part(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarative_partContext, 0)


        def BEGIN(self):
            return self.getToken(vhdlParser.BEGIN, 0)

        def subprogram_statement_part(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_statement_partContext, 0)


        def END(self):
            return self.getToken(vhdlParser.END, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def subprogram_kind(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_kindContext, 0)


        def designator(self):
            return self.getTypedRuleContext(vhdlParser.DesignatorContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_body

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_body(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_body(self)




    def subprogram_body(self):

        localctx = vhdlParser.Subprogram_bodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 450, self.RULE_subprogram_body)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2354
            self.subprogram_specification()
            self.state = 2355
            self.match(vhdlParser.IS)
            self.state = 2356
            self.subprogram_declarative_part()
            self.state = 2357
            self.match(vhdlParser.BEGIN)
            self.state = 2358
            self.subprogram_statement_part()
            self.state = 2359
            self.match(vhdlParser.END)
            self.state = 2361
            _la = self._input.LA(1)
            if _la == vhdlParser.FUNCTION or _la == vhdlParser.PROCEDURE:
                self.state = 2360
                self.subprogram_kind()


            self.state = 2364
            _la = self._input.LA(1)
            if ((((_la - 118)) & ~0x3f) == 0 and ((1 << (_la - 118)) & ((1 << (vhdlParser.BASIC_IDENTIFIER - 118)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 118)) | (1 << (vhdlParser.STRING_LITERAL - 118)))) != 0):
                self.state = 2363
                self.designator()


            self.state = 2366
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_specification(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_specificationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_declaration(self)




    def subprogram_declaration(self):

        localctx = vhdlParser.Subprogram_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 452, self.RULE_subprogram_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2368
            self.subprogram_specification()
            self.state = 2369
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_declarative_itemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_declarationContext, 0)


        def subprogram_body(self):
            return self.getTypedRuleContext(vhdlParser.Subprogram_bodyContext, 0)


        def type_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Type_declarationContext, 0)


        def subtype_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_declarationContext, 0)


        def constant_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Constant_declarationContext, 0)


        def variable_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Variable_declarationContext, 0)


        def file_declaration(self):
            return self.getTypedRuleContext(vhdlParser.File_declarationContext, 0)


        def alias_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Alias_declarationContext, 0)


        def attribute_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_declarationContext, 0)


        def attribute_specification(self):
            return self.getTypedRuleContext(vhdlParser.Attribute_specificationContext, 0)


        def use_clause(self):
            return self.getTypedRuleContext(vhdlParser.Use_clauseContext, 0)


        def group_template_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_template_declarationContext, 0)


        def group_declaration(self):
            return self.getTypedRuleContext(vhdlParser.Group_declarationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_declarative_item

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_declarative_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_declarative_item(self)




    def subprogram_declarative_item(self):

        localctx = vhdlParser.Subprogram_declarative_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 454, self.RULE_subprogram_declarative_item)
        try:
            self.state = 2384
            la_ = self._interp.adaptivePredict(self._input, 261, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 2371
                self.subprogram_declaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 2372
                self.subprogram_body()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 2373
                self.type_declaration()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 2374
                self.subtype_declaration()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 2375
                self.constant_declaration()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 2376
                self.variable_declaration()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 2377
                self.file_declaration()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 2378
                self.alias_declaration()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 2379
                self.attribute_declaration()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 2380
                self.attribute_specification()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 2381
                self.use_clause()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 2382
                self.group_template_declaration()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 2383
                self.group_declaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_declarative_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def subprogram_declarative_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Subprogram_declarative_itemContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Subprogram_declarative_itemContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_declarative_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_declarative_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_declarative_part(self)




    def subprogram_declarative_part(self):

        localctx = vhdlParser.Subprogram_declarative_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 456, self.RULE_subprogram_declarative_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2389
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ALIAS) | (1 << vhdlParser.ATTRIBUTE) | (1 << vhdlParser.CONSTANT) | (1 << vhdlParser.FILE) | (1 << vhdlParser.FUNCTION) | (1 << vhdlParser.GROUP) | (1 << vhdlParser.IMPURE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (vhdlParser.PROCEDURE - 68)) | (1 << (vhdlParser.PURE - 68)) | (1 << (vhdlParser.SHARED - 68)) | (1 << (vhdlParser.SUBTYPE - 68)) | (1 << (vhdlParser.TYPE - 68)) | (1 << (vhdlParser.USE - 68)) | (1 << (vhdlParser.VARIABLE - 68)))) != 0):
                self.state = 2386
                self.subprogram_declarative_item()
                self.state = 2391
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_kindContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCEDURE(self):
            return self.getToken(vhdlParser.PROCEDURE, 0)

        def FUNCTION(self):
            return self.getToken(vhdlParser.FUNCTION, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_kind

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_kind(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_kind(self)




    def subprogram_kind(self):

        localctx = vhdlParser.Subprogram_kindContext(self, self._ctx, self.state)
        self.enterRule(localctx, 458, self.RULE_subprogram_kind)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2392
            _la = self._input.LA(1)
            if not(_la == vhdlParser.FUNCTION or _la == vhdlParser.PROCEDURE):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def procedure_specification(self):
            return self.getTypedRuleContext(vhdlParser.Procedure_specificationContext, 0)


        def function_specification(self):
            return self.getTypedRuleContext(vhdlParser.Function_specificationContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_specification(self)




    def subprogram_specification(self):

        localctx = vhdlParser.Subprogram_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 460, self.RULE_subprogram_specification)
        try:
            self.state = 2396
            token = self._input.LA(1)
            if token == vhdlParser.PROCEDURE:
                self.enterOuterAlt(localctx, 1)
                self.state = 2394
                self.procedure_specification()

            elif token in [vhdlParser.FUNCTION, vhdlParser.IMPURE, vhdlParser.PURE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2395
                self.function_specification()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Procedure_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROCEDURE(self):
            return self.getToken(vhdlParser.PROCEDURE, 0)

        def designator(self):
            return self.getTypedRuleContext(vhdlParser.DesignatorContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def formal_parameter_list(self):
            return self.getTypedRuleContext(vhdlParser.Formal_parameter_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_procedure_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterProcedure_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitProcedure_specification(self)




    def procedure_specification(self):

        localctx = vhdlParser.Procedure_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 462, self.RULE_procedure_specification)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2398
            self.match(vhdlParser.PROCEDURE)
            self.state = 2399
            self.designator()
            self.state = 2404
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 2400
                self.match(vhdlParser.LPAREN)
                self.state = 2401
                self.formal_parameter_list()
                self.state = 2402
                self.match(vhdlParser.RPAREN)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_specificationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION(self):
            return self.getToken(vhdlParser.FUNCTION, 0)

        def designator(self):
            return self.getTypedRuleContext(vhdlParser.DesignatorContext, 0)


        def RETURN(self):
            return self.getToken(vhdlParser.RETURN, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def formal_parameter_list(self):
            return self.getTypedRuleContext(vhdlParser.Formal_parameter_listContext, 0)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def PURE(self):
            return self.getToken(vhdlParser.PURE, 0)

        def IMPURE(self):
            return self.getToken(vhdlParser.IMPURE, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_function_specification

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterFunction_specification(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitFunction_specification(self)




    def function_specification(self):

        localctx = vhdlParser.Function_specificationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 464, self.RULE_function_specification)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2407
            _la = self._input.LA(1)
            if _la == vhdlParser.IMPURE or _la == vhdlParser.PURE:
                self.state = 2406
                _la = self._input.LA(1)
                if not(_la == vhdlParser.IMPURE or _la == vhdlParser.PURE):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()


            self.state = 2409
            self.match(vhdlParser.FUNCTION)
            self.state = 2410
            self.designator()
            self.state = 2415
            _la = self._input.LA(1)
            if _la == vhdlParser.LPAREN:
                self.state = 2411
                self.match(vhdlParser.LPAREN)
                self.state = 2412
                self.formal_parameter_list()
                self.state = 2413
                self.match(vhdlParser.RPAREN)


            self.state = 2417
            self.match(vhdlParser.RETURN)
            self.state = 2418
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subprogram_statement_partContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def sequential_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Sequential_statementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Sequential_statementContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_subprogram_statement_part

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubprogram_statement_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubprogram_statement_part(self)




    def subprogram_statement_part(self):

        localctx = vhdlParser.Subprogram_statement_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 466, self.RULE_subprogram_statement_part)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2423
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << vhdlParser.ASSERT) | (1 << vhdlParser.BREAK) | (1 << vhdlParser.CASE) | (1 << vhdlParser.EXIT) | (1 << vhdlParser.FOR) | (1 << vhdlParser.IF) | (1 << vhdlParser.LOOP) | (1 << vhdlParser.NEXT) | (1 << vhdlParser.NULL))) != 0) or ((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & ((1 << (vhdlParser.REPORT - 79)) | (1 << (vhdlParser.RETURN - 79)) | (1 << (vhdlParser.WAIT - 79)) | (1 << (vhdlParser.WHILE - 79)) | (1 << (vhdlParser.BASIC_IDENTIFIER - 79)) | (1 << (vhdlParser.EXTENDED_IDENTIFIER - 79)) | (1 << (vhdlParser.LPAREN - 79)))) != 0):
                self.state = 2420
                self.sequential_statement()
                self.state = 2425
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subtype_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SUBTYPE(self):
            return self.getToken(vhdlParser.SUBTYPE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_subtype_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubtype_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubtype_declaration(self)




    def subtype_declaration(self):

        localctx = vhdlParser.Subtype_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 468, self.RULE_subtype_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2426
            self.match(vhdlParser.SUBTYPE)
            self.state = 2427
            self.identifier()
            self.state = 2428
            self.match(vhdlParser.IS)
            self.state = 2429
            self.subtype_indication()
            self.state = 2430
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Subtype_indicationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selected_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Selected_nameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Selected_nameContext, i)


        def constraint(self):
            return self.getTypedRuleContext(vhdlParser.ConstraintContext, 0)


        def tolerance_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Tolerance_aspectContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_subtype_indication

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSubtype_indication(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSubtype_indication(self)




    def subtype_indication(self):

        localctx = vhdlParser.Subtype_indicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 470, self.RULE_subtype_indication)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2432
            self.selected_name()
            self.state = 2434
            la_ = self._interp.adaptivePredict(self._input, 268, self._ctx)
            if la_ == 1:
                self.state = 2433
                self.selected_name()


            self.state = 2437
            la_ = self._interp.adaptivePredict(self._input, 269, self._ctx)
            if la_ == 1:
                self.state = 2436
                self.constraint()


            self.state = 2440
            la_ = self._interp.adaptivePredict(self._input, 270, self._ctx)
            if la_ == 1:
                self.state = 2439
                self.tolerance_aspect()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SuffixContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def CHARACTER_LITERAL(self):
            return self.getToken(vhdlParser.CHARACTER_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(vhdlParser.STRING_LITERAL, 0)

        def ALL(self):
            return self.getToken(vhdlParser.ALL, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_suffix

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterSuffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitSuffix(self)




    def suffix(self):

        localctx = vhdlParser.SuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 472, self.RULE_suffix)
        try:
            self.state = 2446
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2442
                self.identifier()

            elif token == vhdlParser.CHARACTER_LITERAL:
                self.enterOuterAlt(localctx, 2)
                self.state = 2443
                self.match(vhdlParser.CHARACTER_LITERAL)

            elif token == vhdlParser.STRING_LITERAL:
                self.enterOuterAlt(localctx, 3)
                self.state = 2444
                self.match(vhdlParser.STRING_LITERAL)

            elif token == vhdlParser.ALL:
                self.enterOuterAlt(localctx, 4)
                self.state = 2445
                self.match(vhdlParser.ALL)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TargetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(vhdlParser.NameContext, 0)


        def aggregate(self):
            return self.getTypedRuleContext(vhdlParser.AggregateContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_target

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTarget(self)




    def target(self):

        localctx = vhdlParser.TargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 474, self.RULE_target)
        try:
            self.state = 2450
            token = self._input.LA(1)
            if token in [vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2448
                self.name()

            elif token == vhdlParser.LPAREN:
                self.enterOuterAlt(localctx, 2)
                self.state = 2449
                self.aggregate()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.FactorContext)
            else:
                return self.getTypedRuleContext(vhdlParser.FactorContext, i)


        def multiplying_operator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Multiplying_operatorContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Multiplying_operatorContext, i)


        def getRuleIndex(self):
            return vhdlParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTerm(self)




    def term(self):

        localctx = vhdlParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 476, self.RULE_term)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2452
            self.factor()
            self.state = 2458
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 273, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 2453
                    self.multiplying_operator()
                    self.state = 2454
                    self.factor() 
                self.state = 2460
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 273, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Terminal_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.NameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.NameContext, i)


        def TO(self):
            return self.getToken(vhdlParser.TO, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_terminal_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTerminal_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTerminal_aspect(self)




    def terminal_aspect(self):

        localctx = vhdlParser.Terminal_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 478, self.RULE_terminal_aspect)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2461
            self.name()
            self.state = 2464
            _la = self._input.LA(1)
            if _la == vhdlParser.TO:
                self.state = 2462
                self.match(vhdlParser.TO)
                self.state = 2463
                self.name()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Terminal_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TERMINAL(self):
            return self.getToken(vhdlParser.TERMINAL, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_terminal_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTerminal_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTerminal_declaration(self)




    def terminal_declaration(self):

        localctx = vhdlParser.Terminal_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 480, self.RULE_terminal_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2466
            self.match(vhdlParser.TERMINAL)
            self.state = 2467
            self.identifier_list()
            self.state = 2468
            self.match(vhdlParser.COLON)
            self.state = 2469
            self.subnature_indication()
            self.state = 2470
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Through_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def THROUGH(self):
            return self.getToken(vhdlParser.THROUGH, 0)

        def tolerance_aspect(self):
            return self.getTypedRuleContext(vhdlParser.Tolerance_aspectContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_through_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterThrough_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitThrough_aspect(self)




    def through_aspect(self):

        localctx = vhdlParser.Through_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 482, self.RULE_through_aspect)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2472
            self.identifier_list()
            self.state = 2474
            _la = self._input.LA(1)
            if _la == vhdlParser.TOLERANCE:
                self.state = 2473
                self.tolerance_aspect()


            self.state = 2478
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 2476
                self.match(vhdlParser.VARASGN)
                self.state = 2477
                self.expression()


            self.state = 2480
            self.match(vhdlParser.THROUGH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Timeout_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(vhdlParser.FOR, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_timeout_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTimeout_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTimeout_clause(self)




    def timeout_clause(self):

        localctx = vhdlParser.Timeout_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 484, self.RULE_timeout_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2482
            self.match(vhdlParser.FOR)
            self.state = 2483
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Tolerance_aspectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOLERANCE(self):
            return self.getToken(vhdlParser.TOLERANCE, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_tolerance_aspect

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterTolerance_aspect(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitTolerance_aspect(self)




    def tolerance_aspect(self):

        localctx = vhdlParser.Tolerance_aspectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 486, self.RULE_tolerance_aspect)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2485
            self.match(vhdlParser.TOLERANCE)
            self.state = 2486
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Type_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TYPE(self):
            return self.getToken(vhdlParser.TYPE, 0)

        def identifier(self):
            return self.getTypedRuleContext(vhdlParser.IdentifierContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def IS(self):
            return self.getToken(vhdlParser.IS, 0)

        def type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Type_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_type_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterType_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitType_declaration(self)




    def type_declaration(self):

        localctx = vhdlParser.Type_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 488, self.RULE_type_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2488
            self.match(vhdlParser.TYPE)
            self.state = 2489
            self.identifier()
            self.state = 2492
            _la = self._input.LA(1)
            if _la == vhdlParser.IS:
                self.state = 2490
                self.match(vhdlParser.IS)
                self.state = 2491
                self.type_definition()


            self.state = 2494
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Type_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def scalar_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Scalar_type_definitionContext, 0)


        def composite_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Composite_type_definitionContext, 0)


        def access_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.Access_type_definitionContext, 0)


        def file_type_definition(self):
            return self.getTypedRuleContext(vhdlParser.File_type_definitionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_type_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterType_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitType_definition(self)




    def type_definition(self):

        localctx = vhdlParser.Type_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 490, self.RULE_type_definition)
        try:
            self.state = 2500
            token = self._input.LA(1)
            if token in [vhdlParser.RANGE, vhdlParser.LPAREN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2496
                self.scalar_type_definition()

            elif token in [vhdlParser.ARRAY, vhdlParser.RECORD]:
                self.enterOuterAlt(localctx, 2)
                self.state = 2497
                self.composite_type_definition()

            elif token == vhdlParser.ACCESS:
                self.enterOuterAlt(localctx, 3)
                self.state = 2498
                self.access_type_definition()

            elif token == vhdlParser.FILE:
                self.enterOuterAlt(localctx, 4)
                self.state = 2499
                self.file_type_definition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Unconstrained_array_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARRAY(self):
            return self.getToken(vhdlParser.ARRAY, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def index_subtype_definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Index_subtype_definitionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Index_subtype_definitionContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_unconstrained_array_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterUnconstrained_array_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitUnconstrained_array_definition(self)




    def unconstrained_array_definition(self):

        localctx = vhdlParser.Unconstrained_array_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 492, self.RULE_unconstrained_array_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2502
            self.match(vhdlParser.ARRAY)
            self.state = 2503
            self.match(vhdlParser.LPAREN)
            self.state = 2504
            self.index_subtype_definition()
            self.state = 2509
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 2505
                self.match(vhdlParser.COMMA)
                self.state = 2506
                self.index_subtype_definition()
                self.state = 2511
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2512
            self.match(vhdlParser.RPAREN)
            self.state = 2513
            self.match(vhdlParser.OF)
            self.state = 2514
            self.subtype_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Unconstrained_nature_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARRAY(self):
            return self.getToken(vhdlParser.ARRAY, 0)

        def LPAREN(self):
            return self.getToken(vhdlParser.LPAREN, 0)

        def index_subtype_definition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Index_subtype_definitionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Index_subtype_definitionContext, i)


        def RPAREN(self):
            return self.getToken(vhdlParser.RPAREN, 0)

        def OF(self):
            return self.getToken(vhdlParser.OF, 0)

        def subnature_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subnature_indicationContext, 0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_unconstrained_nature_definition

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterUnconstrained_nature_definition(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitUnconstrained_nature_definition(self)




    def unconstrained_nature_definition(self):

        localctx = vhdlParser.Unconstrained_nature_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 494, self.RULE_unconstrained_nature_definition)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2516
            self.match(vhdlParser.ARRAY)
            self.state = 2517
            self.match(vhdlParser.LPAREN)
            self.state = 2518
            self.index_subtype_definition()
            self.state = 2523
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 2519
                self.match(vhdlParser.COMMA)
                self.state = 2520
                self.index_subtype_definition()
                self.state = 2525
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2526
            self.match(vhdlParser.RPAREN)
            self.state = 2527
            self.match(vhdlParser.OF)
            self.state = 2528
            self.subnature_indication()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Use_clauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE(self):
            return self.getToken(vhdlParser.USE, 0)

        def selected_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Selected_nameContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Selected_nameContext, i)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def getRuleIndex(self):
            return vhdlParser.RULE_use_clause

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterUse_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitUse_clause(self)




    def use_clause(self):

        localctx = vhdlParser.Use_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 496, self.RULE_use_clause)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2530
            self.match(vhdlParser.USE)
            self.state = 2531
            self.selected_name()
            self.state = 2536
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == vhdlParser.COMMA:
                self.state = 2532
                self.match(vhdlParser.COMMA)
                self.state = 2533
                self.selected_name()
                self.state = 2538
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 2539
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Variable_assignment_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(vhdlParser.TargetContext, 0)


        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_variable_assignment_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterVariable_assignment_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitVariable_assignment_statement(self)




    def variable_assignment_statement(self):

        localctx = vhdlParser.Variable_assignment_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 498, self.RULE_variable_assignment_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2542
            la_ = self._interp.adaptivePredict(self._input, 282, self._ctx)
            if la_ == 1:
                self.state = 2541
                self.label_colon()


            self.state = 2544
            self.target()
            self.state = 2545
            self.match(vhdlParser.VARASGN)
            self.state = 2546
            self.expression()
            self.state = 2547
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Variable_declarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE(self):
            return self.getToken(vhdlParser.VARIABLE, 0)

        def identifier_list(self):
            return self.getTypedRuleContext(vhdlParser.Identifier_listContext, 0)


        def COLON(self):
            return self.getToken(vhdlParser.COLON, 0)

        def subtype_indication(self):
            return self.getTypedRuleContext(vhdlParser.Subtype_indicationContext, 0)


        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def SHARED(self):
            return self.getToken(vhdlParser.SHARED, 0)

        def VARASGN(self):
            return self.getToken(vhdlParser.VARASGN, 0)

        def expression(self):
            return self.getTypedRuleContext(vhdlParser.ExpressionContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_variable_declaration

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterVariable_declaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitVariable_declaration(self)




    def variable_declaration(self):

        localctx = vhdlParser.Variable_declarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 500, self.RULE_variable_declaration)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2550
            _la = self._input.LA(1)
            if _la == vhdlParser.SHARED:
                self.state = 2549
                self.match(vhdlParser.SHARED)


            self.state = 2552
            self.match(vhdlParser.VARIABLE)
            self.state = 2553
            self.identifier_list()
            self.state = 2554
            self.match(vhdlParser.COLON)
            self.state = 2555
            self.subtype_indication()
            self.state = 2558
            _la = self._input.LA(1)
            if _la == vhdlParser.VARASGN:
                self.state = 2556
                self.match(vhdlParser.VARASGN)
                self.state = 2557
                self.expression()


            self.state = 2560
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Wait_statementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WAIT(self):
            return self.getToken(vhdlParser.WAIT, 0)

        def SEMI(self):
            return self.getToken(vhdlParser.SEMI, 0)

        def label_colon(self):
            return self.getTypedRuleContext(vhdlParser.Label_colonContext, 0)


        def sensitivity_clause(self):
            return self.getTypedRuleContext(vhdlParser.Sensitivity_clauseContext, 0)


        def condition_clause(self):
            return self.getTypedRuleContext(vhdlParser.Condition_clauseContext, 0)


        def timeout_clause(self):
            return self.getTypedRuleContext(vhdlParser.Timeout_clauseContext, 0)


        def getRuleIndex(self):
            return vhdlParser.RULE_wait_statement

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterWait_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitWait_statement(self)




    def wait_statement(self):

        localctx = vhdlParser.Wait_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 502, self.RULE_wait_statement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2563
            _la = self._input.LA(1)
            if _la == vhdlParser.BASIC_IDENTIFIER or _la == vhdlParser.EXTENDED_IDENTIFIER:
                self.state = 2562
                self.label_colon()


            self.state = 2565
            self.match(vhdlParser.WAIT)
            self.state = 2567
            _la = self._input.LA(1)
            if _la == vhdlParser.ON:
                self.state = 2566
                self.sensitivity_clause()


            self.state = 2570
            _la = self._input.LA(1)
            if _la == vhdlParser.UNTIL:
                self.state = 2569
                self.condition_clause()


            self.state = 2573
            _la = self._input.LA(1)
            if _la == vhdlParser.FOR:
                self.state = 2572
                self.timeout_clause()


            self.state = 2575
            self.match(vhdlParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class WaveformContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def waveform_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.Waveform_elementContext)
            else:
                return self.getTypedRuleContext(vhdlParser.Waveform_elementContext, i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(vhdlParser.COMMA)
            else:
                return self.getToken(vhdlParser.COMMA, i)

        def UNAFFECTED(self):
            return self.getToken(vhdlParser.UNAFFECTED, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_waveform

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterWaveform(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitWaveform(self)




    def waveform(self):

        localctx = vhdlParser.WaveformContext(self, self._ctx, self.state)
        self.enterRule(localctx, 504, self.RULE_waveform)
        self._la = 0  # Token type
        try:
            self.state = 2586
            token = self._input.LA(1)
            if token in [vhdlParser.ABS, vhdlParser.NEW, vhdlParser.NOT, vhdlParser.NULL, vhdlParser.BASE_LITERAL, vhdlParser.BIT_STRING_LITERAL, vhdlParser.REAL_LITERAL, vhdlParser.BASIC_IDENTIFIER, vhdlParser.EXTENDED_IDENTIFIER, vhdlParser.CHARACTER_LITERAL, vhdlParser.STRING_LITERAL, vhdlParser.LPAREN, vhdlParser.PLUS, vhdlParser.MINUS, vhdlParser.INTEGER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 2577
                self.waveform_element()
                self.state = 2582
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == vhdlParser.COMMA:
                    self.state = 2578
                    self.match(vhdlParser.COMMA)
                    self.state = 2579
                    self.waveform_element()
                    self.state = 2584
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token == vhdlParser.UNAFFECTED:
                self.enterOuterAlt(localctx, 2)
                self.state = 2585
                self.match(vhdlParser.UNAFFECTED)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Waveform_elementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(vhdlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(vhdlParser.ExpressionContext, i)


        def AFTER(self):
            return self.getToken(vhdlParser.AFTER, 0)

        def getRuleIndex(self):
            return vhdlParser.RULE_waveform_element

        def enterRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.enterWaveform_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance(listener, vhdlListener):
                listener.exitWaveform_element(self)




    def waveform_element(self):

        localctx = vhdlParser.Waveform_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 506, self.RULE_waveform_element)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2588
            self.expression()
            self.state = 2591
            _la = self._input.LA(1)
            if _la == vhdlParser.AFTER:
                self.state = 2589
                self.match(vhdlParser.AFTER)
                self.state = 2590
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




