

def for_parentBlock(iterator, func):
    lp_cnt = 1
    rp_cnt = 0
    tmp = next(iterator)
    if tmp.type != 'LPAREN':
        raise Exception("for_parentBlock expected LPAREN recieved %s" % tmp.type)
    
    for o in iterator:
        if o.type == 'LPAREN':
            lp_cnt += 1
        if o.type == 'RPAREN':
            rp_cnt += 1
        if  lp_cnt == rp_cnt:
            return
        func(iterator, o)
