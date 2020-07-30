# select = map, groupBy = itertools.groupby
from itertools import zip_longest
from math import inf
from types import GeneratorType


class DuplicitValueExc(Exception):
    """
    Exception which means that there are multiple items which this query
    selected but it should return only one
    """


class NoValueExc(Exception):
    """
    Exception which means that query did not selected any item
    """


def distinctBy(iterable, fn):
    """
    uniq operation with key selector
    """
    s = set()
    for i in iterable:
        r = fn(i)
        if r not in s:
            s.add(r)
            yield i


def single(iterable, fn):
    """
    Get value from iterable where fn(item) and check
    if there is not fn(other item)

    :raise DuplicitValueExc: when there are multiple items satisfying fn()
    :raise NoValueExc: when no value satisfying fn(item) found
    """
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
    """
    :return: True if fn(item) for any item else False
    """
    for item in iterable:
        if fn(item):
            return True
    return False


def arr_all(iterable, fn):
    """
    :return: True if fn(item) for all items in interable or iterable
        is empty else False
    """
    for item in iterable:
        if not fn(item):
            return False
    return True


def take(iterrable, howMay):
    """
    :return: generator of first n items from iterrable
    """
    assert howMay >= 0

    if not howMay:
        return

    last = howMay - 1
    for i, item in enumerate(iterrable):
        yield item
        if i == last:
            return


def where(iterable, fn):
    """
    :return: generator of items from iterable where fn(item)
    """
    for i in iterable:
        if fn(i):
            yield i


def iter_with_last(iterable):
    """
    :return: generator of tuples (isLastFlag, item)
    """
    # Ensure it's an iterator and get the first field
    iterable = iter(iterable)
    try:
        prev = next(iterable)
    except StopIteration:
        return
    for item in iterable:
        # Lag by one item so I know I'm not at the end
        yield False, prev
        prev = item
    # Last item
    yield True, prev


def groupedby(collection, fn):
    """
    same like itertools.groupby

    :note: This function does not needs initial sorting like itertools.groupby

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


def flatten(iterables, level=inf):
    """
    Flatten nested lists, tuples, generators and maps

    :param level: maximum depth of flattening
    """
    if level >= 0 and isinstance(iterables, (list, tuple, GeneratorType,
                                             map, zip)):
        level -= 1
        for i in iterables:
            yield from flatten(i, level=level)
    else:
        yield iterables


def grouper(n, iterable, padvalue=None):
    """grouper(3, 'abcdefg', 'x') -->
       ('a','b','c'), ('d','e','f'), ('g','x','x')
    """
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def areSetsIntersets(setA, setB):
    """
    Check if intersection of sets is not empty
    """
    return any(x in setA for x in setB)


def balanced_reduce(arr, opFn):
    while len(arr) > 1:
        nextArr = []
        for a, b in grouper(2, arr):
            nextArr.append(opFn(a, b))
        arr = nextArr

    return arr[0]
