# -*- coding: utf-8 -*-


import cmath
import math
import random
from string import ascii_lowercase as letters
from typing import Any, Callable
from enum import Enum

from .production import *

from .formula import Formula, unlock, relock


NumericValue = int | float | complex | bool

class _ArgsType(Enum):
    ALLNUM = 'allnum'
    PRODUCTION = 'production'
    FORMULA = 'formula'

class _Constructor:

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
            return _ArgsType.ALLNUM
        elif production_count and formula_count:
            raise TypeError('unsupported operand type(s) for this math functions: Formula and Production')
        elif production_count:
            return _ArgsType.PRODUCTION
        elif formula_count:
            return _ArgsType.FORMULA

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
    def _func_construct_wrapper(cls, func: Callable, name: str):
        def wrapper(*args: Production | Formula | Any):
            match cls._args_type_check(args):
                case _ArgsType.ALLNUM:
                    return func(*args)
                case _ArgsType.PRODUCTION:
                    return cls._construct_production(func, args, name)
                case _ArgsType.FORMULA:
                    return cls._construct_formula(args, wrapper)
        return wrapper

class _NewMathFunction:

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
    '''
    A set of functions that Provides additional arithmetic functions.
    '''

    @classmethod
    def define(cls, func, name):
        '''
        Define a new math function.

        Args:
            func (Callable): the core of new function.
            name (str): the name of new function.
        '''
        exec(f'cls.{name} = newfunc(func, name)', {
            'cls': cls, 
            'newfunc': _Constructor._func_construct_wrapper, 
            'func': func, 
            'name': name})

    # basic
    to_int: Formula | Production = _Constructor._func_construct_wrapper(int, 'int')
    to_float = _Constructor._func_construct_wrapper(float, 'float')
    root = _Constructor._func_construct_wrapper(lambda x, y: x ** (1 / y), 'root')
    sqrt = _Constructor._func_construct_wrapper(cmath.sqrt, 'sqrt')
    cbrt = _Constructor._func_construct_wrapper(lambda x: x ** (1 / 3), 'cbrt')
    log = _Constructor._func_construct_wrapper(cmath.log, 'log')
    fact = _Constructor._func_construct_wrapper(_NewMathFunction.factorial, 'fact')

    # permutation combinations
    comb = _Constructor._func_construct_wrapper(math.comb, 'comb')
    perm = _Constructor._func_construct_wrapper(math.perm, 'perm')

    # lcg and gcd
    lcm = _Constructor._func_construct_wrapper(math.lcm, 'lcg')
    gcd = _Constructor._func_construct_wrapper(math.gcd, 'gcd')

    # trigonometry
    sin = _Constructor._func_construct_wrapper(cmath.sin, 'sin')
    cos = _Constructor._func_construct_wrapper(cmath.cos, 'cos')
    tan = _Constructor._func_construct_wrapper(cmath.tan, 'tan')
    asin = _Constructor._func_construct_wrapper(cmath.asin, 'asin')
    acos = _Constructor._func_construct_wrapper(cmath.acos, 'acos')
    atan = _Constructor._func_construct_wrapper(cmath.atan, 'atan')
    dist = _Constructor._func_construct_wrapper(_NewMathFunction.dist, 'dist')
    hypot = _Constructor._func_construct_wrapper(lambda *args: cmath.sqrt(sum((x ** 2 for x in args))), 'hypot')

    # angle
    radtodeg = _Constructor._func_construct_wrapper(lambda x: cmath.pi / 180 * x, 'rtd')
    gradtodeg = _Constructor._func_construct_wrapper(lambda x: x * 400 / 360, 'gtd')
    degtorad = _Constructor._func_construct_wrapper(lambda x: 180 / cmath.pi * x, 'dtr')
    gradtorad = _Constructor._func_construct_wrapper(lambda x: 240 / cmath.pi * x, 'gtr')
    degtograd = _Constructor._func_construct_wrapper(lambda x: x * 360 / 400, 'dtg')
    radtograd = _Constructor._func_construct_wrapper(lambda x: cmath.pi / 240 * x, 'rtd')

    # hyperbolic
    sinh = _Constructor._func_construct_wrapper(cmath.sinh, 'sinh')
    cosh = _Constructor._func_construct_wrapper(cmath.cosh, 'cosh')
    tanh = _Constructor._func_construct_wrapper(cmath.tanh, 'tanh')
    asinh = _Constructor._func_construct_wrapper(cmath.asinh, 'asinh')
    acosh = _Constructor._func_construct_wrapper(cmath.acosh, 'acosh')
    atanh = _Constructor._func_construct_wrapper(cmath.atanh, 'atanh')

    # random
    rand = _Constructor._func_construct_wrapper(random.randint, 'rand')
    choose = _Constructor._func_construct_wrapper(lambda *args: random.choice(args), 'choose')
    wchoose = _Constructor._func_construct_wrapper(_NewMathFunction.wchoose, 'wchoose')

    # complex
    to_complex = _Constructor._func_construct_wrapper(complex, 'complex')
    real = _Constructor._func_construct_wrapper(lambda x: 0j+x.real, 'real')
    imag = _Constructor._func_construct_wrapper(lambda x: x.imag, 'imag')
    conjugate = _Constructor._func_construct_wrapper(lambda x: x.conjugate(), 'conjugate')
    phase = _Constructor._func_construct_wrapper(cmath.phase, 'phase')
    modulus = _Constructor._func_construct_wrapper(lambda x: cmath.polar(x)[0], 'modulus')
    rect = _Constructor._func_construct_wrapper(cmath.rect, 'rect')

    # logic
    to_bool = _Constructor._func_construct_wrapper(bool, 'bool')
    logicand = _Constructor._func_construct_wrapper(lambda *args: all(map(bool, args)), 'and')
    logicor = _Constructor._func_construct_wrapper(lambda *args: any(map(bool, args)), 'or')
    logicnot = _Constructor._func_construct_wrapper(lambda x: not bool(x), 'not')
    logicxor = _Constructor._func_construct_wrapper(lambda x, y: (not (bool(x) and bool(y))) and (bool(x) or bool(y)), 'xor')
    branch = _Constructor._func_construct_wrapper(_NewMathFunction.branch, 'branch')
