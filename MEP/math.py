# -*- coding: utf-8 -*-


import cmath
import math
import random
from string import ascii_lowercase as letters
from typing import Any, Callable

from .production import *

from.formula import Formula, unlock, relock


class Constructor:

    @classmethod
    def _args_type_check(cls, args):
        num_count = formula_count = production_count = 0
        for arg in args:
            if not isinstance(arg, (Formula, Production)):
                num_count += 1
            elif isinstance(arg, Formula):
                formula_count += 1
            elif isinstance(arg, Production):
                production_count += 1

        if num_count == len(args):
            return 'allnum'
        elif production_count and formula_count:
            raise TypeError('unsupported operand type(s) for this math functions: Formula and Production')
        elif production_count:
            return 'prod'
        elif formula_count:
            return 'form'

    @classmethod
    def _construct_production(cls, func, args, name):
        funcs, trees, args_ = {}, {}, set()
        unlock(*args)
        for index, arg in enumerate(args):
            if isinstance(arg, Production):
                funcs[index] = arg._func
                trees[index] = arg._tree
                args_ = args_ | arg._args
        relock(*args)

        return Production(lambda kwargs: func(
            *[(funcs[index](kwargs) if isinstance(arg, Production) else arg) for index, arg in enumerate(args)]),
            dict((('S', name),) + tuple(
                [(letters[index], trees[index] if isinstance(arg, Production) else arg)
                 for index, arg in enumerate(args)])), 
            args_)

    @classmethod
    def _construct_formula(cls, args, wrapper):
        productions = {}
        unlock(*args)
        for index, arg in enumerate(args):
            if isinstance(arg, Formula):
                productions[index] = arg._formula._production
        relock(*args)

        production = wrapper(*[(productions[index] if isinstance(arg, Formula) else arg) for index, arg in enumerate(args)])
        return Formula(production)

    @classmethod
    def newfunc(cls, func: Callable, name: str):
        def wrapper(*args: Production | Formula | Any):
            match cls._args_type_check(args):
                case 'allnum':
                    return func(*args)
                case 'prod':
                    return cls._construct_production(func, args, name)
                case 'form':
                    return cls._construct_formula(args, wrapper)
        return wrapper

class Utils:

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
    def branch(cls, *args):
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
            'newfunc': Constructor.newfunc, 
            'func': func, 
            'name': name})

    # basic
    root = Constructor.newfunc(lambda x, y: x ** (1 / y), 'root')
    sqrt = Constructor.newfunc(cmath.sqrt, 'sqrt')
    cbrt = Constructor.newfunc(lambda x: x ** (1 / 3), 'cbrt')
    log = Constructor.newfunc(cmath.log, 'log')
    fact = Constructor.newfunc(Utils.factorial, 'fact')

    # numtype
    int = Constructor.newfunc(int, 'int')
    float = Constructor.newfunc(float, 'float')

    # permutation combinations
    comb = Constructor.newfunc(math.comb, 'comb')
    perm = Constructor.newfunc(math.perm, 'perm')

    # lcg anf gcd
    lcm = Constructor.newfunc(math.lcm, 'lcg')
    gcd = Constructor.newfunc(math.gcd, 'gcd')

    # trigonometry
    sin = Constructor.newfunc(cmath.sin, 'sin')
    cos = Constructor.newfunc(cmath.cos, 'cos')
    tan = Constructor.newfunc(cmath.tan, 'tan')
    asin = Constructor.newfunc(cmath.asin, 'asin')
    acos = Constructor.newfunc(cmath.acos, 'acos')
    atan = Constructor.newfunc(cmath.atan, 'atan')
    dist = Constructor.newfunc(Utils.dist, 'dist')
    hypot = Constructor.newfunc(lambda *args: cmath.sqrt(sum((x ** 2 for x in args))), 'hypot')

    # angle
    radtodeg = Constructor.newfunc(lambda x: cmath.pi / 180 * x, 'rtd')
    gradtodeg = Constructor.newfunc(lambda x: x * 400 / 360, 'gtd')
    degtorad = Constructor.newfunc(lambda x: 180 / cmath.pi * x, 'dtr')
    gradtorad = Constructor.newfunc(lambda x: 240 / cmath.pi * x, 'gtr')
    degtograd = Constructor.newfunc(lambda x: x * 360 / 400, 'dtg')
    radtograd = Constructor.newfunc(lambda x: cmath.pi / 240 * x, 'rtd')

    # hyperbolic
    sinh = Constructor.newfunc(cmath.sinh, 'sinh')
    cosh = Constructor.newfunc(cmath.cosh, 'cosh')
    tanh = Constructor.newfunc(cmath.tanh, 'tanh')
    asinh = Constructor.newfunc(cmath.asinh, 'asinh')
    acosh = Constructor.newfunc(cmath.acosh, 'acosh')
    atanh = Constructor.newfunc(cmath.atanh, 'atanh')

    # random
    rand = Constructor.newfunc(random.randint, 'rand')
    choose = Constructor.newfunc(lambda *args: random.choice(args), 'choose')
    wchoose = Constructor.newfunc(Utils.wchoose, 'wchoose')

    # complex
    complex = Constructor.newfunc(complex, 'complex')
    real = Constructor.newfunc(lambda x: x.real, 'real')
    imag = Constructor.newfunc(lambda x: x.imag, 'imag')
    conjugate = Constructor.newfunc(lambda x: x.conjugate(), 'conjugate')
    phase = Constructor.newfunc(cmath.phase, 'phase')
    modulus = Constructor.newfunc(lambda x: cmath.polar(x)[0], 'modulus')
    rect = Constructor.newfunc(cmath.rect, 'rect')

    # logic
    bool = Constructor.newfunc(bool, 'bool')
    logicand = Constructor.newfunc(lambda *args: all(map(bool, args)), 'and')
    logicor = Constructor.newfunc(lambda *args: any(map(bool, args)), 'or')
    logicnot = Constructor.newfunc(lambda x: not bool(x), 'not')
    logicxor = Constructor.newfunc(lambda x, y: (not (bool(x) and bool(y))) and (bool(x) or bool(y)), 'xor')
    branch = Constructor.newfunc(Utils.branch, 'branch')
