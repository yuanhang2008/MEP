# -*- coding: utf-8 -*-


import math
from string import ascii_lowercase as letters
from typing import Any, Callable

from .production import *


def newfunc(func: Callable, name: str):
    def wrapper(*args: Production | Any):
        funcs = {}
        trees = {}
        args_ = set()
        unlock(*args)
        for arg in args:
            if isinstance(arg, Production):
                funcs[arg] = arg._func
                trees[arg] = arg._tree
                args_ = args_ | arg._args
        relock(*args)

        if not any([isinstance(arg, Production) for arg in args]):
            return func(*args)
        return Production(lambda kwargs: func(
            *[(funcs[arg](kwargs) if isinstance(arg, Production) else arg) for arg in args]),
            dict((('S', name),) + tuple(
                [(letters[index], trees[arg] if isinstance(arg, Production) else arg)
                 for index, arg in enumerate(args)])),
            args_)

    return wrapper

def root(x, y=2):
    if y == 0:
        return 1
    if y == 1:
        return x
    if x >= 0 and y == 2:
        return math.sqrt(x)
    return x ** (1 / y)

class Math:

    abs = newfunc(math.fabs, 'abs')
    root = newfunc(root, 'root')
    round = newfunc(round, 'round')
    ceil = newfunc(math.ceil, 'ceil')
    floor = newfunc(math.floor, 'floor')
    int = newfunc(int, 'int')
    sqrt = newfunc(root, 'sqrt')
    factorial = newfunc(math.factorial, 'factorial')
