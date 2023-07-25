# -*- coding: utf-8 -*-


import cmath
import math
import random
from string import ascii_lowercase as letters
from typing import Any, Callable

from MEP.production import *


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

class Helper:

    @classmethod
    def factorial(cls, x):
        result = 1
        if x == 1:
            return result
        for i in range(2, x + 1):
            result *= i
        return result

    @classmethod
    def dist(cls, *args):
        if len(*args) % 2 != 0:
            raise ValueError('bad value was given')
        mid = len(args) // 2
        p = zip(args[:mid], args[mid:])
        return (sum((abs(x - y) ** 2 for x, y in p))) ** 0.5
    
    @classmethod
    def wchoose(cls, *args):
        if len(*args) % 2 != 0:
            raise ValueError('bad value was given')
        values, weights = [], []
        for k, v in enumerate(args):
            if k % 2 == 0:
                values.append(v)
            else:
                weights.append(v)
        return random.choices(values, weights)[0]
    
    @classmethod
    def conditions(cls, *args):
        if len(args) % 2 != 1:
            raise ValueError('bad value was given')
        for index, item in enumerate(args):
            if index % 2 == 1 and bool(item):
                return args[index - 1]
        return args[-1]

class Math:

    @classmethod
    def define(cls, func, name):
        exec(f'cls.{name} = newfunc(func, name)', {
            'cls': cls, 
            'newfunc': newfunc, 
            'func': func, 
            'name': name})

    # basic
    root = newfunc(lambda x, y: x ** (1 / y), 'root')
    sqrt = newfunc(cmath.sqrt, 'sqrt')
    cbrt = newfunc(lambda x: x ** (1 / 3), 'cbrt')
    log = newfunc(cmath.log, 'log')
    fact = newfunc(Helper.factorial, 'fact')

    # numtype
    int = newfunc(int, 'int')
    float = newfunc(float, 'float')

    # permutation combinations
    comb = newfunc(math.comb, 'comb')
    perm = newfunc(math.perm, 'perm')

    # lcg anf gcd
    lcm = newfunc(math.lcm, 'lcg')
    gcd = newfunc(math.gcd, 'gcd')

    # trigonometry
    sin = newfunc(cmath.sin, 'sin')
    cos = newfunc(cmath.cos, 'cos')
    tan = newfunc(cmath.tan, 'tan')
    asin = newfunc(cmath.asin, 'asin')
    acos = newfunc(cmath.acos, 'acos')
    atan = newfunc(cmath.atan, 'atan')
    dist = newfunc(Helper.dist, 'dist')
    hypot = newfunc(lambda *args: cmath.sqrt(sum((x ** 2 for x in args))), 'hypot')

    # angle
    radtodeg = newfunc(lambda x: cmath.pi / 180 * x, 'rtd')
    gradtodeg = newfunc(lambda x: x * 400 / 360, 'gtd')
    degtorad = newfunc(lambda x: 180 / cmath.pi * x, 'dtr')
    gradtorad = newfunc(lambda x: 240 / cmath.pi * x, 'gtr')
    degtograd = newfunc(lambda x: x * 360 / 400, 'dtg')
    radtograd = newfunc(lambda x: cmath.pi / 240 * x, 'rtd')

    # hyperbolic
    sinh = newfunc(cmath.sinh, 'sinh')
    cosh = newfunc(cmath.cosh, 'cosh')
    tanh = newfunc(cmath.tanh, 'tanh')
    asinh = newfunc(cmath.asinh, 'asinh')
    acosh = newfunc(cmath.acosh, 'acosh')
    atanh = newfunc(cmath.atanh, 'atanh')

    # random
    rand = newfunc(random.randint, 'rand')
    choose = newfunc(lambda *args: random.choice(args), 'choose')
    wchoose = newfunc(Helper.wchoose, 'wchoose')

    # complex
    complex = newfunc(complex, 'complex')
    real = newfunc(lambda x: x.real, 'real')
    imag = newfunc(lambda x: x.imag, 'imag')
    conjugate = newfunc(lambda x: x.conjugate(), 'conjugate')
    phase = newfunc(cmath.phase, 'phase')
    modulus = newfunc(lambda x: cmath.polar(x)[0], 'modulus')
    rect = newfunc(cmath.rect, 'rect')

    # logic
    bool = newfunc(bool, 'bool')
    logicand = newfunc(lambda *args: all(map(bool, args)), 'and')
    logicor = newfunc(lambda *args: any(map(bool, args)), 'or')
    logicnot = newfunc(lambda x: not bool(x), 'not')
    logicxor = newfunc(lambda x, y: (not (bool(x) and bool(y))) and (bool(x) or bool(y)), 'xor')
    conditions = newfunc(Helper.conditions, 'if')
