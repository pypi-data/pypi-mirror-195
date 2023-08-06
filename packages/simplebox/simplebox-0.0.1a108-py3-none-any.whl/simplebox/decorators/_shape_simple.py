#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import timeit
from functools import wraps
from typing import Any, Dict, Tuple, Callable

import psutil

from ..decorators._process import _do

_sort_stats = ('calls', 'cumulative', 'cumtime', 'file', 'filename', 'module', 'ncalls', 'pcalls', 'line', 'name',
               'nfl', 'stdname', 'time', 'tottime')


def shaper_simple():
    """
    Performs profiling of the specified function(only memory and time, cpu).
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"stacklevel": 7}
            return _do(func=func, decorator_name=shaper_simple.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper
    return __inner


def __do_shaper_simple(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None) -> Any:
    args_ = () if args is None else args
    kwargs_ = {} if kwargs is None else kwargs
    start = timeit.default_timer()
    try:
        return func(*args_, **kwargs_)
    finally:
        pid = os.getpid()
        process = psutil.Process(pid)
        mm_info = process.memory_full_info()
        cpu_info = process.cpu_times()
        name = func.__qualname__
        memory = mm_info.uss / 1024 / 1024
        end = timeit.default_timer()
        print(f"run '{name}' simple info, memory used: {memory:.4f} MB, time used: {(end - start):.4f} second, "
              f"cpu user: {cpu_info.user:.4f}, cpu system: {cpu_info.system:.4f}, "
              f"cpu child user: {cpu_info.children_user:.4f}, cpu child system: {cpu_info.children_system:.4f}")


__all__ = [shaper_simple]
