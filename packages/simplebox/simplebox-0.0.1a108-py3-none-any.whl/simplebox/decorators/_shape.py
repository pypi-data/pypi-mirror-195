#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import tempfile
import timeit
from cProfile import Profile
from functools import wraps
from pathlib import Path
from pstats import Stats
from typing import Any, Dict, Tuple, Callable

import psutil
from flameprof import render, get_out, DEFAULT_FORMAT, DEFAULT_THRESHOLD, DEFAULT_WIDTH, DEFAULT_ROW_HEIGHT, \
    DEFAULT_FONT_SIZE, DEFAULT_LOG_MULT

from ..decorators._process import _do

_sort_stats = ('calls', 'cumulative', 'cumtime', 'file', 'filename', 'module', 'ncalls', 'pcalls', 'line', 'name',
               'nfl', 'stdname', 'time', 'tottime')


def shaper(sort_stats: str = "stdname", dump_stats: Path or str = None, flame_graphs: Path or str = None):
    """
    Performs profiling of the specified function
    :param flame_graphs: save the flame graphs. suffix must be .svg.
    :param dump_stats: Save the analysis to a file. suffix must be .prof.
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
            opts = {"sort_stats": sort_stats, "dump_stats": dump_stats, "flame_graphs": flame_graphs, "stacklevel": 7}
            return _do(func=func, decorator_name=shaper.__name__, args=args, kwargs=kwargs, opts=opts)
        return __wrapper
    return __inner


def __do_shaper(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None) -> Any:
    sort_stat = opts.get("sort_stats")
    dump_stats = opts.get("dump_stats")
    flame_graphs = opts.get("flame_graphs")

    if sort_stat and sort_stat not in _sort_stats:
        raise ValueError(f"Excepted sort stats kind in '{_sort_stats}', got a '{sort_stat}'")

    if dump_stats:
        suffix = Path(dump_stats).suffix
        if suffix != ".prof":
            raise TypeError(f"profile suffix error: excepted is '.prof', got a '{suffix}'")
    if flame_graphs:
        suffix = Path(flame_graphs).suffix
        if suffix != ".svg":
            raise TypeError(f"flame graphs file suffix error: excepted suffix is '.svg', got a '{suffix}'")

    args_ = () if args is None else args
    kwargs_ = {} if kwargs is None else kwargs
    with Profile() as pr:
        start = timeit.default_timer()
        result = pr.runcall(func, *args_, **kwargs_)
        if sort_stat in _sort_stats:
            __print(pr, sort_stat, start)
        else:
            __print(pr, "stdname", start)
        if dump_stats:
            pr.dump_stats(dump_stats)
            print(f"\n>>>profile stats<<< path: {dump_stats}")
        if flame_graphs:
            if dump_stats:
                __gen_flame_graphs(dump_stats, flame_graphs)
            else:
                with tempfile.NamedTemporaryFile(suffix=".prof", delete=False) as fp:
                    tm_file = fp.name
                    pr.dump_stats(fp.name)
                    __gen_flame_graphs(fp.name, flame_graphs)
                p = Path(tm_file)
                if p.exists():
                    p.unlink()
            print(f"\n>>>flame graphs<<< path: {flame_graphs}")
    return result


def __gen_flame_graphs(stats_file, flame_graphs):
    s = Stats(stats_file)
    render(s.stats, get_out(str(flame_graphs)), DEFAULT_FORMAT, DEFAULT_THRESHOLD / 100,
           DEFAULT_WIDTH, DEFAULT_ROW_HEIGHT, DEFAULT_FONT_SIZE, DEFAULT_LOG_MULT)


def __print(pr, sort_stat, start):
    pid = os.getpid()
    process = psutil.Process(pid)
    mm_info = process.memory_full_info()
    cpu_info = process.cpu_times()
    memory = mm_info.uss / 1024 / 1024
    end = timeit.default_timer()
    pr.print_stats(sort_stat)
    print(f"    memory used: {memory:.4f} MB, time used: {(end - start):.4f} second, "
          f"cpu user: {cpu_info.user:.4f}, cpu system: {cpu_info.system:.4f}, "
          f"cpu child user: {cpu_info.children_user:.4f}, cpu child system: {cpu_info.children_system:.4f}")


__all__ = [shaper]
