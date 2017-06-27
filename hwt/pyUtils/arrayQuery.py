# select = map, groupBy = itertools.groupby
from types import GeneratorType
from itertools import zip_longest
from math import inf


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
            yield i


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


def arr_all(iterable, fn):
    """
    returns True if fn(item) for all items in interable or iterable is empty else False
    """
    for item in iterable:
        if not fn(item):
            return False
    return True


def where(iterable, fn):
    """
    Select items from iterable where fn(item)
    """
    for i in iterable:
        if fn(i):
            yield i


def iter_with_last(iterable):
    """
    Iterate iterable and yield tuples (isLastFlag, item)
    """
    # Ensure it's an iterator and get the first field
    iterable = iter(iterable)
    prev = next(iterable)
    for item in iterable:
        # Lag by one item so I know I'm not at the end
        yield False, prev
        prev = item
    # Last item
    yield True, prev


def extendLen(arr, newLen, useValue=None):
    """
    Extend size of arr to newLen and use padding value specified by useValue
    """
    lenNow = len(arr)
    toAdd = newLen - lenNow
    assert toAdd > 0
    arr.extend([useValue for _ in range(toAdd)])


def groupedby(collection, fn):
    """
    This function does not needs initial sorting like itertools.groupby

    :attention: Order of pairs is not deterministic.
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
    """
    split arr on smaller arrays of size
    """
    arr = list(arr)
    while len(arr) > size:
        pice = arr[:size]
        yield pice
        arr = arr[size:]
    yield arr


def flatten(iterables, level=inf):
    """
    Flatten nested lists, tuples, generators and maps

    :param level: maximum depth of flattening
    """
    if level >= 0 and isinstance(iterables, (list, tuple, GeneratorType, map, zip)):
        level -= 1
        for i in iterables:
            yield from flatten(i, level=level)
    else:
        yield iterables


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)
