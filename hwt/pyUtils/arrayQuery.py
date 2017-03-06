# select = map, groupBy = itertools.groupby

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
    for _ in where(iterable, fn):
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
    assert toAdd > 0
    arr.extend([useValue for _ in range(toAdd)])
    
    
def indexUsigIs(iterable, item):
    i = 0
    for v in iterable:
        if v is item:
            return i
        i += 1


def groupedby(collection, fn):
    """
    This function does not needs initial sorting like itertools.groupby
    @attention: Order of pairs is not deterministic.
    """
    d = {}
    for item in collection:
        k = fn(item)
        try:
            arr = d[k] 
        except KeyError:
            arr = []
            d[k] = arr
        arr.append(item)
    
    yield from d.items()

def split(arr, size):
    arr = list(arr)
    while len(arr) > size:
        pice = arr[:size]
        yield pice
        arr = arr[size:]
    yield arr