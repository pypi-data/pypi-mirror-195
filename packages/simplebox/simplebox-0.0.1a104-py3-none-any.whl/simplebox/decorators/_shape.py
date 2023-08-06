#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cProfile import Profile
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Tuple, Callable

from ..decorators._process import _do

_sort_stats = ('calls', 'cumulative', 'cumtime', 'file', 'filename', 'module', 'ncalls', 'pcalls', 'line', 'name',
               'nfl', 'stdname', 'time', 'tottime')


def shaper(sort_stats: str = "stdname", save_file: str = None):
    """
    Performs profiling of the specified function
    :param save_file: Save the analysis to a file
    :param sort_stats: This method modifies the Stats object by sorting it according to the supplied criteria.
    The argument can be either a string or a SortKey enum identifying the basis of a sort (example: 'time', 'name',
    SortKey.TIME or SortKey.NAME). The SortKey enums argument have advantage over the string argument in that it is
    more robust and less error prone.

    When more than one key is provided, then additional keys are used as secondary criteria when there is equality in
    all keys selected before them. For example, sort_stats(SortKey.NAME, SortKey.FILE) will sort all the entries
    according to their function name, and resolve all ties (identical function names) by sorting by file name.

    For the string argument, abbreviations can be used for any key names, as long as the abbreviation is unambiguous.

    The following are the valid string and sort stats:
        'calls'         ->          number of calls
        'cumulative'    ->          cumulative time
        'cumtime'       ->          cumulative time
        'file'          ->          file name
        'filename'      ->          file name
        'module'        ->          file name
        'ncalls'        ->          number of calls
        'pcalls'        ->          raw call count
        'line'          ->          line number
        'name'          ->          function name
        'nfl'           ->          name/file/line
        'stdname'       ->          standard name
        'time'          ->          internal time
        'tottime'       ->          internal time

    usage:
        def add(x, y):
            time.sleep(1)
            value = x + y
            return value


        def sub(x, y):
            time.sleep(1.5)
            value = x - y
            return value


        class TestProfile:

            @shaper()
            def calc(self, x, y):
                time.sleep(1)
                add_result = add(x, y)
                sub_result = sub(x, y)
                print(f"{x} add {y} result is: {add_result}")
                print(f"{x} sub {y} result is: {sub_result}")
                return x+y


        if __name__ == '__main__':
            result = TestProfile().calc(1, 2)
            assert result == 3

    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"sort_stats": sort_stats, "save_file": save_file, "stacklevel": 7}
            return _do(func=func, decorator_name=shaper.__name__, args=args, kwargs=kwargs, opts=opts)
        return __wrapper
    return __inner


def __do_shaper(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None) -> Any:
    sort_stat = opts.get("sort_stats")
    save_file = opts.get("save_file")
    args_ = () if args is None else args
    kwargs_ = {} if kwargs is None else kwargs
    with Profile() as pr:
        result = pr.runcall(func, *args_, **kwargs_)
        if sort_stat in _sort_stats:
            pr.print_stats(sort_stat)
        else:
            pr.print_stats('stdname')
        if save_file:
            if not Path(save_file).exists():
                raise ValueError(f"'{save_file}' is not exists.")
            pr.dump_stats(save_file)
    return result


__all__ = [shaper]
