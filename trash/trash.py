def incrIndent(tokens, indent):
    tmp = []
    indentStr = "    "
    end = (0, 0)
    start = (0, 0)
    tmp.append(tokenize.TokenInfo(tokenize.ENCODING, 'utf-8', start, end, ''))
    for _ in range(indent):
        # type string start end line
        tmp.append(tokenize.TokenInfo(token.INDENT, indentStr, start, end, indentStr))
    for t in tokens:
        if t.type == tokenize.ENCODING:
            pass
        if t[0] == token.INDENT:
            i = t.string
            for _ in range(indent):
                i += indentStr
            t = t._replace(string=i)
        tmp.append(t)
    tmp = tokens
    tmp = tokensNormalize(tokens)
    return tmp

def tokensNormalize(tokens):
    posY = 1
    posX = 0
    line = ""
    indentStrLen = 4
    indent = 0
    tmp = []
    tmp.append(tokenize.TokenInfo(tokenize.ENCODING, 'utf-8', (0, 0), (0, 0), ""))
    tmp.append(tokenize.TokenInfo(tokenize.NL, '\n', (posY, 0), (posY, 1), "\n"))
    posY += 1

    for t in tokens:
        start = (posY, posX)
        if t.type == tokenize.ENCODING:
            continue
        elif t.type == token.NEWLINE or t.type == tokenize.NL:
            if len(tmp) == 2 :
                continue  # trim newlines at start of code
            end = (posY, posX + 1)
            tmp.append(tokenize.TokenInfo(t.type, t.string, start, end, line))
            posY += 1
            posX = indent * indentStrLen
        else:
            if t.type == tokenize.INDENT:
                indent += 1
                posX = indent * indentStrLen
            elif t.type == tokenize.DEDENT:
                indent -= 1
                posX = indent * indentStrLen
            else:
                width = len(t.string) 
                posX += width
            end = (posY, posX)
            tmp.append(tokenize.TokenInfo(t.type, t.string, start, end, line))
            # posX +=1
    for orig, norm in zip(tokens, tmp):
        if not orig.type == norm.type:
            raise Exception() 
        # if not orig.start[0] == norm.start[0]:
        #    raise Exception() 
        # if not orig.start[1] == norm.start[1]:
        #    raise Exception() 
        # #assert orig.line == norm.line
    return tmp        
            
    
def joinTokens(tokensA, tokensB):
    s0 = tokenize.untokenize(tokensA)
    s1 = tokenize.untokenize(tokensB)
    if type(s0) == str:
        s0 = s0.encode()
    if type(s1) == str:
        s1 = s1.encode()
    tokens = list(tokenize.tokenize(io.BytesIO(s0 + s1).readline))
    return tokens