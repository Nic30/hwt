
class DuplicitValueExc(Exception):
    pass

def first(iterable, fn):
    for i in iterable:
        if fn(i):
            return i

def single(iterable, fn):
    found = False
    ret = None
    
    for i in iterable:
        if fn(i):
            if found:
                raise DuplicitValueExc(i)
            found = True
            ret = i
        
    return ret

def where(iterable, fn):
    for i in iterable:
        if fn(i):
            yield i