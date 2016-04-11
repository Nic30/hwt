
class DuplicitValueExc(Exception):
    pass

class NoValueExc(Exception):
    pass

def distinctBy(iterable, fn):
    s = set()
    for i in iterable:
        r = fn(i)
        if r not in s:
            s.add(fn(i))
            yield  i

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
    if not found:
        raise NoValueExc()    
    return ret

def arr_any(iterable, fn):
    for i in where(iterable, fn):
        return True
    return False

def where(iterable, fn):
    for i in iterable:
        if fn(i):
            yield i
            
def last_iter(it):
    # Ensure it's an iterator and get the first field
    it = iter(it)
    prev = next(it)
    for item in it:
        # Lag by one item so I know I'm not at the end
        yield False, prev
        prev = item
    # Last item
    yield True, prev

def extendLen(arr, newLen, useValue=None):
    lenNow = len(arr)
    toAdd = newLen - lenNow
    assert(toAdd > 0)
    arr.extend([useValue for _ in range(toAdd)])
    
    
