# -*- coding: utf-8 -*-


import math
import random
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

def dist(*args):
    if len(args) % 2 != 0:
        raise ValueError('bad arguments was given')
    pos1, pos2 = args[:int(len(args) / 2)], args[int(len(args) / 2):]
    return math.dist(pos1, pos2)

def choice(*args):
    if len(args) == 1:
        return args[0]
    return random.choice(args)

def randweight(*args):
    if len(args) % 2 != 0:
        raise ValueError('bad arguments was given')
    if len(args) == 2:
        return args[0]
    values = []
    weights = []
    for index, item in enumerate(args):
        if index % 2 == 0:
            values.append(item)
        else:
            weights.append(item)
    return random.choices(values, weights)[0]

def conditions(*args):
    if len(args) % 2 == 0:
        raise ValueError('bad arguments was given')
    for index, item in enumerate(args[:-1]):
        if index % 2 == 0 and bool(args[index + 1]):
            return item
    return args[-1]

class Math:

    # basic
    abs = newfunc(math.fabs, 'abs')
    factorial = newfunc(math.factorial, 'factorial')
    root = newfunc(root, 'root')
    sqrt = newfunc(root, 'sqrt')
    log = newfunc(math.log, 'log')
    comb = newfunc(math.comb, 'comb')
    perm = newfunc(math.perm, 'perm')
    gcd = newfunc(math.gcd, 'gcd')
    lcm = newfunc(math.lcm, 'lcm')

    # round
    round = newfunc(round, 'round')
    ceil = newfunc(math.ceil, 'ceil')
    floor = newfunc(math.floor, 'floor')
    int = newfunc(int, 'int')

    # trigonometry
    sin = newfunc(math.sin, 'sin')
    cos = newfunc(math.cos, 'cos')
    tan = newfunc(math.tan, 'tan')
    asin = newfunc(math.asin, 'asin')
    acos = newfunc(math.acos, 'acos')
    atan = newfunc(math.atan, 'atan')
    dist = newfunc(dist, 'dist')
    hypot = newfunc(math.hypot, 'hypot')

    # angle
    degrees = newfunc(math.degrees, 'degrees')
    radians = newfunc(math.radians, 'radians')

    # hyperbolic
    sinh = newfunc(math.sinh, 'sinh')
    cosh = newfunc(math.cosh, 'cosh')
    tanh = newfunc(math.tanh, 'tanh')
    asinh = newfunc(math.asinh, 'asinh')
    acosh = newfunc(math.acosh, 'acosh')
    atanh = newfunc(math.atanh, 'atanh')

    # random
    rand = newfunc(random.randint, 'random')
    choose = newfunc(choice, 'choose')
    randweight = newfunc(randweight, 'randweight')

    # logic
    bool = newfunc(bool, 'bool')
    logicnot = newfunc(lambda x: not x, 'not')
    logicand = newfunc(lambda x, y: (bool(x) and bool(y)), 'and')
    logicor = newfunc(lambda x, y: (bool(x) or bool(y)), 'or')
    logicxor = newfunc(lambda x, y: ((not (bool(x) and bool(y))) and (bool(x) or bool(y))), 'xor')
    condition = newfunc(lambda x, y, z: x if bool(z) else y, 'if')
    conditions = newfunc(conditions, 'ifs')