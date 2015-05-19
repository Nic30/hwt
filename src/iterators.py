import re

def forBracketBlock(fileReader, startCnt=0):
    for i in  forBlock(fileReader, "(", ")", startCnt):
        yield i

def forBlock(fileReader, startTag, endTag, startCnt=0):
    sCnt = startCnt
    eCnt = 0
    
    while sCnt != eCnt or sCnt == startCnt:
        line = next(fileReader)
        sCnt += line.count(startTag)
        eCnt += line.count(endTag) 
        yield line

def countStartTagsWithEnd(line):
    keywordsWithEnd = ["is", "loop", "generate", "then" ]
    cnt = 0
    for k in keywordsWithEnd:
        m = re.match("(?<!\w)%s(?!\w)" % (k), line, re.IGNORECASE)
        if m:
            cnt +=1
    return cnt

def forVhdlBlock(fileReader, startCnt):
    sCnt = startCnt
    eCnt = 0
    endMatch = re.compile("(?<!\w)(END|ELSIF)(?!\w)", re.IGNORECASE)
    while  eCnt < sCnt or sCnt == startCnt:
        line = next(fileReader)
        sCnt += countStartTagsWithEnd(line)
        if endMatch.match(line):
            eCnt += 1
            if eCnt >= sCnt:
                break;
        yield line


#pathTree ={
#           "PackageDef" : "PACKAGE _name_ IS _body_ END;",
#           "FuncDef": "FUNCTION _name_ (_params_) RETURN _type_;",
#           "ComponentDef" : "COMPONENT _name_ IS _body_ END;",
#           "Generic": "GENERIC ( _genericRecs_ );",
#           "Port" : "PORT ( _portRecs_  );",
#           "Package": "PACKAGE BODY _name_ IS _body_ END;",
#           "Function" : "FUNCTION _name_ ( _params_ ) RETURN _type_ IS _head_ BEGIN _body_ END;",
#           "Case" : "CASE _var_ IS _body_ END;",
#           "If" : "IF _condition_ THEN _body_ END;",
#           "Architecture" : "ARCHITECTURE _name_ OF _parentname_ IS _head_ BEGIN _body_ END;",
#           "Process" : "PROCESS (_sensivitilist_) BEGIN _body_ END;",
#           "For" : "FOR _var_ IN _var_ TO _var_ LOOP _body_ END;",
#           "EntityDef" : "ENTITY _name_ IS _body_ END;",
#           "GenerateIf" : "IF _condition_ GENERATE _body_ END;",
#           "GenerateFor" : "FOR _var_ IN _var_ TO _var_ GENERATE _body_ END;"
#           
#           
#        }