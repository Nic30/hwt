import re
from io import StringIO
from models import entityReg, architectureReg, Entity, Architecture
from enum import Enum


regex_isChar = re.compile("[a-zA-Z]|_")

vhdl_keywords_str = ['architecture', 'begin', 'component', 'downto', 'else', 'elsif', 'end', 'entity', 'generate', 'if', 'is', 'port', 'then', 'to']


class vhdl_kw(Enum):
    k_architecture =0
    k_begin  =1
    k_component =2
    k_downto =3
    k_else = 4
    k_elsif =5
    k_end  = 6
    k_entity =7
    k_generate = 8
    k_if = 9
    k_is = 10
    k_port = 11
    k_then = 12
    k_to = 13
    
    
class VHDL_lex():
    def __init__(self,s):
        s = re.sub( "--[^\n]*", "", s)
        tmp = StringIO()
        for ch in s:
            if regex_isChar.match(ch):
                tmp.write(ch)
            else:
                v = tmp.getvalue().lower()
                if v != "":
                    if v in vhdl_keywords_str:
                        print( "keyw: " + v )
                    else:
                        print(v)
                    tmp = StringIO()
            
    #@staticmethod
    #def splitOn(splitedLine, splitingReg):
    #    """splitingReg should be ("replacestr", re.compile("searchParent")) """
    #    for s in splitedLine:
    #        for item in splitingReg[1].sub("\n"+splitingReg[0]+"\n",s).split("\n"):
    #            yield item
    #
    #splits = [("(" ,re.compile("\(")),
    #          (")",re.compile("\)")),
    #          ("is", re.compile("(?<!\w)is(?!\w)", re.IGNORECASE)),
    #          ("then", re.compile("(?<!\w)then(?!\w)", re.IGNORECASE)),
    #          ("begin", re.compile("(?<!\w)begin(?!\w)", re.IGNORECASE)),
    #          ("generate", re.compile("(?<!\w)generate(?!\w)", re.IGNORECASE)),
    #          ("elsif", re.compile("(?<!\w)elsif(?!\w)", re.IGNORECASE))]
    #generateFix = re.compile("end generate", re.IGNORECASE)
        
    
    
if __name__ == "__main__":
    with open("test.vhd") as f:
        l = VHDL_lex(f.read())   
        #sourceFile= VHDL_withoutComments(f.read())
        #for line in sourceFile:
        #    mE = entityReg.match(line)
        #    mA = architectureReg.match(line)
        #    if mE :
        #        e = Entity(mE.group(1), sourceFile, None)
        #    if mA:
        #        a = Architecture(mA.group(1), mA.group(2), sourceFile, None)
        #for p in e.port:
        #    print(p)
