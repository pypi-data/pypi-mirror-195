#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import deque, defaultdict
from functools import reduce
from itertools import *
from math import fsum
from secrets import choice
from typing import Iterable, Callable, Dict, List, Iterator

from ..collection._streamable import Streamable, _default_call_return_true, _default_call_return_intact
from ..exceptions import raise_exception
from ..generic import T, R, K, V
from ..util import Optionals

__all__ = ['Stream']


class Stream(Streamable[T]):
    """

    """

    def __init__(self, iterable: Iterable[T]):
        """
        Initialization by Stream.of() or Stream.of_item()
        """
        self.__type = type(iterable)
        if not issubclass(self.__type, Iterable):
            raise TypeError(f"Exception 'iterable' object, got a {self.__type.__name__}")
        self.__data: Iterator = iter(iterable)
        self.__size = None

    @staticmethod
    def of(*args) -> 'Stream[T]':
        return Stream(args)

    @staticmethod
    def of_item(iterable: Iterable[T]) -> 'Stream[T]':
        return Stream(iterable)

    def __iter__(self):
        return self.__data

    def __length(self):
        cnt = count()
        deque(zip(self, cnt), 0)
        return next(cnt)

    def __next__(self):
        return next(self.__data)

    # intermediate operation
    def filter(self, predicate: Callable[[T], bool] = _default_call_return_true) -> 'Stream[T]':
        return Stream.of_item((element for element in self if predicate(element)))

    def filter_else_raise(self, predicate: Callable[[T], bool],
                          exception: Callable[[T], BaseException]) -> 'Streamable[T]':
        for element in self:
            if predicate(element):
                yield element
            else:
                raise_exception(exception(element))

    def distinct(self) -> 'Stream[T]':
        return Stream.of_item(_distinct(self.__data))

    def map(self, predicate: Callable[[T], R] = _default_call_return_intact) -> 'Stream[R]':
        return Stream.of_item(predicate(element) for element in self)

    def flat(self, predicate: Callable[[T], R] = _default_call_return_intact) -> 'Stream[T]':

        def __flattening(iterable):
            if not issubclass(type(iterable), Iterable):
                yield predicate(iterable)
            else:
                for element in iterable:
                    yield from __flattening(element)

        return Stream.of_item(__flattening(self))

    def flat_map(self, predicate: Callable[[T], R] = _default_call_return_intact) -> 'Stream[R]':
        return Stream.of_item(predicate(element) for element in chain.from_iterable(self))

    def limit(self, maxSize: int = 0) -> 'Stream[T]':
        return Stream.of_item(islice(self, 0, maxSize))

    def peek(self, action: Callable[[T], None]) -> 'Stream[T]':
        for element in self:
            action(element)
            yield
        return self

    def skip(self, index: int = 0) -> 'Stream[T]':
        return Stream.of_item(islice(self, index, None))

    def sorted(self, comparator: Callable[[T], T] = _default_call_return_intact, reverse: bool = False) -> 'Stream[T]':
        return Stream.of_item(sorted(self.__data, key=comparator, reverse=reverse))

    def dropwhile(self, predicate: Callable[[T], bool] = _default_call_return_true) -> 'Stream[T]':
        return Stream.of_item(dropwhile(predicate, self))

    def takewhile(self, predicate: Callable[[T], bool] = _default_call_return_true) -> 'Stream[T]':
        return Stream.of_item(takewhile(predicate, self))

    def intersection(self, iterable: Iterable[T]) -> 'Stream[T]':
        # return Stream.of_item(set(self).intersection(iterable))
        return Stream.of_item(_intersection(self, iterable))

    def union(self, iterable: Iterable[T]) -> 'Stream[T]':
        # return Stream.of_item(set(self).union(iterable))
        return Stream.of_item(_union(self, iterable))

    def difference(self, iterable: Iterable[T]) -> 'Stream[T]':
        # return Stream.of_item(set(self).difference(iterable))
        return Stream.of_item(_difference(self, iterable))

    def symmetric_difference(self, iterable: Iterable[T]) -> 'Stream[T]':
        # return Stream.of_item(set(self).symmetric_difference(iterable))
        return Stream.of_item(_symmetric_difference(self, iterable))

    # terminal operations
    def count(self, predicate: Callable[[T], bool] = _default_call_return_true) -> int:
        return self.__length()

    def reduce(self, accumulator: Callable[[T, T], T], initializer: T = None) -> Optionals[T]:
        if initializer:
            return Optionals.of_none_able(reduce(accumulator, self, initializer))
        else:
            return Optionals.of_none_able(reduce(accumulator, self))

    def forEach(self, action: Callable[[T], None]) -> None:
        for element in self:
            action(element)

    def min(self, comparator: Callable[[T], T] = _default_call_return_intact, default: T = None) -> Optionals[T]:
        result = min(self, key=comparator)
        return Optionals.of_none_able(result if result is None else default)

    def max(self, comparator: Callable[[T], T] = _default_call_return_intact, default: T = None) -> Optionals[R]:
        result = max(self, key=comparator)
        return Optionals.of_none_able(result if result else default)

    def any_match(self, predicate: Callable[[T], bool] = _default_call_return_true) -> bool:
        return any(map(predicate, self))

    def all_match(self, predicate: Callable[[T], bool] = _default_call_return_true) -> bool:
        return all(map(predicate, self))

    def none_match(self, predicate: Callable[[T], bool] = _default_call_return_true) -> bool:
        return not self.any_match(predicate)

    def find_first(self) -> Optionals[T]:
        result = list(self)
        return Optionals.of_none_able(result[0] if result else None)

    def find_any(self) -> Optionals[T]:

        return Optionals.of_none_able(choice(list(self.__data)))

    def group(self, predicate: Callable[[T], R] = _default_call_return_intact,
              collector: Callable[[Iterable[T]], Iterable[T]] = list, overwrite: bool = True) -> Dict[K, Iterable[T]]:
        group_map = defaultdict(collector)
        for key, group in groupby(self, key=predicate):
            if overwrite:
                group_map[key] = collector(group)
            else:
                continue

        return group_map

    def to_dict(self, k: Callable[[T], K], v: Callable[[T], V], overwrite: bool = True) -> Dict[K, V]:
        tmp = {}
        for i in self:
            key = k(i)
            value = v(i)
            if overwrite:
                tmp[key] = value
            else:
                if key not in tmp:
                    tmp[key] = value
        return tmp

    def to_list(self) -> List[T]:
        return list(self.__data)

    def collect(self, collector: Callable[[Iterable[T]], Iterable[T]]) -> Iterable[T]:
        return collector(self.__data)

    def sum(self, start: int = 0) -> int or float:
        return sum(self, start=start)

    def fsum(self):
        return fsum(self)

    def isdisjoint(self, iterable: Iterable[T]) -> bool:
        return set(self).isdisjoint(set(iterable))

    def issubset(self, iterable: Iterable[T]) -> bool:
        return set(self).issubset(iterable)

    def issuperset(self, iterable: Iterable[T]) -> bool:
        return set(self).issuperset(iterable)

    def partition(self, size: int = 1, collector: Callable[[Iterable[T]], Iterable[T]] = list) -> 'List[Iterable[T]]':
        if size <= 0:
            length = 1
        else:
            length = size
        p_iterable = list()
        p_iterable_append = p_iterable.append
        while True:
            s_iterable = collector(islice(self, length))
            if s_iterable:
                p_iterable_append(s_iterable)
            else:
                break
        return p_iterable


class _distinct:
    def __init__(self, iterable: Iterable):
        self.__data: Iterator = iter(set(iter(iterable)))

    def __iter__(self):
        return self.__data

    def __next__(self):
        return next(self.__data)


class _intersection:
    def __init__(self, left: Iterable, right: Iterable):
        self.__data: Iterator = iter(set(iter(left)).intersection(set(iter(right))))

    def __iter__(self):
        return self.__data

    def __next__(self):
        return next(self.__data)


class _union:
    def __init__(self, left: Iterable, right: Iterable):
        self.__data: Iterator = iter(set(iter(left)).union(set(iter(right))))

    def __iter__(self):
        return self.__data

    def __next__(self):
        return next(self.__data)


class _difference:
    def __init__(self, left: Iterable, right: Iterable):
        self.__data: Iterator = iter(set(iter(left)).difference(set(iter(right))))

    def __iter__(self):
        return self.__data

    def __next__(self):
        return next(self.__data)


class _symmetric_difference:
    def __init__(self, left: Iterable, right: Iterable):
        self.__data: Iterator = iter(set(iter(left)).symmetric_difference(set(iter(right))))

    def __iter__(self):
        return self.__data

    def __next__(self):
        return next(self.__data)
