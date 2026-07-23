# select = map, groupBy = itertools.groupby
from collections import deque
from itertools import zip_longest
from math import inf
from types import GeneratorType
from typing import Sequence, Generator, Callable, TypeVar

from hdlConvertorAst.to.hdlUtils import iter_with_last
from hwt.constants import NOT_SPECIFIED


class DuplicitValueExc(Exception):
    """
    Exception which means that there are multiple items which this query
    selected but it should return only one
    """


class NoValueExc(Exception):
    """
    Exception which means that query did not selected any item
    """


_singleT = TypeVar("T")


def single(iterable: Sequence[_singleT], fn: Callable[[_singleT], bool]) -> _singleT:
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


_arr_anyT = TypeVar("T")


def arr_any(iterable: Sequence[_arr_anyT], fn: Callable[[_arr_anyT], bool]) -> bool:
    """
    :return: True if fn(item) for any item else False
    """
    for item in iterable:
        if fn(item):
            return True
    return False


_arr_allT = TypeVar("T")


def arr_all(iterable: Sequence[_arr_allT], fn: Callable[[_arr_allT], bool]) -> bool:
    """
    :return: True if fn(item) for all items in interable or iterable
        is empty else False
    """
    for item in iterable:
        if not fn(item):
            return False
    return True


_takeT = TypeVar("T")


def take(iterrable:Sequence[_takeT], howMay:int) -> Generator[_takeT, None, None]:
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


_whereT = TypeVar("T")


def where(iterable: Sequence[_whereT], fn: Callable[[_whereT], bool]) -> Generator[_whereT, None, None]:
    """
    :return: generator of items from iterable where fn(item)
    """
    for i in iterable:
        if fn(i):
            yield i


_groupedbyKeyT = TypeVar("Key")
_groupedbyValueT = TypeVar("Val")


def groupedby(collection: Sequence[_groupedbyValueT], fn: Callable[[_groupedbyValueT], _groupedbyKeyT])\
    ->dict[_groupedbyKeyT, list[_groupedbyValueT]]:
    """
    same like itertools.groupby

    :note: This function does not needs initial sorting like itertools.groupby

    :attention: Order of pairs is not deterministic.
    """
    d:dict[_groupedbyKeyT, list[_groupedbyValueT]] = {}
    for item in collection:
        k = fn(item)
        try:
            arr = d[k]
        except KeyError:
            arr:list[_groupedbyValueT] = []
            d[k] = arr
        arr.append(item)

    yield from d.items()


def flatten(iterables, level=inf):
    """
    Flatten nested lists, tuples, generators and maps

    :param level: maximum depth of flattening
    """
    if level >= 0 and isinstance(iterables, (list, tuple, GeneratorType,
                                             map, zip, set, deque)):
        level -= 1
        for i in iterables:
            yield from flatten(i, level=level)
    else:
        yield iterables


_grouperT = TypeVar("T")


def grouper(n: int, iterable: Sequence[_grouperT], padvalue=None) -> Sequence[tuple[_grouperT, ...]]:
    """grouper(3, 'abcdefg', 'x') -->
       ('a','b','c'), ('d','e','f'), ('g','x','x')
    """
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def areSetsIntersets(setA: set, setB: set):
    """
    Check if intersection of sets is not empty
    """
    return any(x in setA for x in setB)


_balanced_reduceT = TypeVar("T")


def balanced_reduce(arr: Sequence[_balanced_reduceT],
                    opFn: Callable[[_balanced_reduceT, _balanced_reduceT], _balanced_reduceT])\
                    ->_balanced_reduceT:
    """
    Construct balaned binary tree given array of items and binary operator opFn
    """
    while len(arr) > 1:
        nextArr = []
        for a, b in grouper(2, arr, NOT_SPECIFIED):
            if b is NOT_SPECIFIED:
                # if number of items was odd we have 1 leftover
                nextArr.append(a)
            else:
                nextArr.append(opFn(a, b))
        arr = nextArr

    return arr[0]


_iter_with_lookaheadT = TypeVar("T")


def iter_with_lookahead(it: Sequence[_iter_with_lookaheadT], padValue=None)\
    ->tuple[_iter_with_lookaheadT, _iter_with_lookaheadT]:
    """
    iterate all items with lookahead to next item, for last item the nextitem=padValue
    """
    # Ensure it's an iterator and get the first field
    it = iter(it)
    try:
        prev = next(it)
    except StopIteration:
        # completly empty sequence
        return

    for item in it:
        # Lag by one item so I know I'm not at the end
        yield prev, item
        prev = item

    # Last item
    yield prev, padValue

    
