# -*- coding: utf-8 -*-


import cmath
import math
import random
from string import ascii_lowercase as letters
from typing import Callable, TypeAlias
from enum import Enum

from .production import _Production, _relock, _unlock, NumericValue, _Tree

from .formula import Formula


Calculable: TypeAlias = _Production | Formula | NumericValue

class _ArgsType(Enum):
    ALLNUM = 'allnum'
    PRODUCTION = 'production'
    FORMULA = 'formula'

class _Constructor:

    @staticmethod
    def _args_type_check(args: tuple[Calculable]) -> _ArgsType:
        num_count = formula_count = production_count = 0
        for arg in args:
            if isinstance(arg, Formula):
                formula_count += 1
            elif isinstance(arg, _Production):
                production_count += 1
            else:
                num_count += 1

        if num_count == len(args):
            return _ArgsType.ALLNUM
        elif production_count:
            return _ArgsType.PRODUCTION
        elif formula_count:
            return _ArgsType.FORMULA
        raise TypeError('unsupported operand types for this math functions: Formula and Production')

    @staticmethod
    def _construct_production(func: Callable[[NumericValue], NumericValue], args: tuple[_Production | NumericValue], func_name: str) -> _Production:
        args_: set[str] = set()
        _unlock(*args)
        consructed_func: Callable[[NumericValue], NumericValue] = lambda kwargs: func(
            *[arg._func(kwargs) if isinstance(arg, _Production) else arg
            for arg in args])

        func_tree: _Tree._FunctionProductionTree = _Tree._FunctionProductionTree(func_name, 
            *[arg._tree if isinstance(arg, _Production) else _Tree._NumericProductionTree(arg) 
            for arg in args])
        
        for arg in args:
            if isinstance(arg, _Production):
                args_ |= arg._args
        _relock(*args)

        return _Production(consructed_func, func_tree, args_)

    @staticmethod
    def _construct_formula(args: tuple[Calculable], wrapper: Callable[[Calculable], Calculable]) -> Formula:
        productions: dict[int, NumericValue | _Production] = {}
        _unlock(*args)
        for index, arg in enumerate(args):
            if isinstance(arg, Formula):
                productions[index] = arg._formula._production
        _relock(*args)

        funcs: list[NumericValue | _Production] = [productions[index] if isinstance(arg, Formula) else arg
            for index, arg in enumerate(args)]
        production: _Production = wrapper(*funcs)
        return Formula(production)

    @staticmethod
    def _func_construct_wrapper(func: Callable[[NumericValue], NumericValue], func_name: str) -> Callable[[Calculable], Calculable]:
        def wrapper(*args: Calculable) -> Calculable:
            match _Constructor._args_type_check(args):
                case _ArgsType.ALLNUM:
                    return func(*args)
                case _ArgsType.PRODUCTION:
                    return _Constructor._construct_production(func, args, func_name)
                case _ArgsType.FORMULA:
                    return _Constructor._construct_formula(args, wrapper)
        return wrapper

class _NewMathFunction:

    @staticmethod
    def factorial(x: NumericValue) -> NumericValue:
        result = 1
        if x == 1:
            return result
        for i in range(2, x + 1):
            result *= i
        return result

    @staticmethod
    def dist(*args: NumericValue) -> NumericValue:
        if len(*args) % 2 != 0:
            raise ValueError('bad value was given')
        mid = len(args) // 2
        p = zip(args[:mid], args[mid:])
        return (sum((abs(x - y) ** 2 for x, y in p))) ** 0.5
    
    @staticmethod
    def wchoose(*args: NumericValue) -> NumericValue:
        if len(*args) % 2 != 0:
            raise ValueError('bad value was given')
        values, weights = [], []
        for k, v in enumerate(args):
            if k % 2 == 0:
                values.append(v)
            else:
                weights.append(v)
        return random.choices(values, weights)[0]
    
    @staticmethod
    def branch(*args: NumericValue) -> NumericValue:
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

    @staticmethod
    def define(func: Callable[[NumericValue], NumericValue], name: str) -> None:
        '''
        Define a new math function.

        Args:
            func (Callable): the core of new function.
            name (str): the name of new function.
        '''
        exec(f'Math.{name} = newfunc(func, name)', {
            'newfunc': _Constructor._func_construct_wrapper, 
            'func': func, 
            'name': name})

    # basic
    toint = _Constructor._func_construct_wrapper(int, 'int')
    tofloat = _Constructor._func_construct_wrapper(float, 'float')
    root = _Constructor._func_construct_wrapper(lambda x, y: x ** (1 / y), 'root')
    sqrt = _Constructor._func_construct_wrapper(cmath.sqrt, 'sqrt')
    cbrt = _Constructor._func_construct_wrapper(lambda x: x ** (1 / 3), 'cbrt')
    log = _Constructor._func_construct_wrapper(cmath.log, 'log')
    fact = _Constructor._func_construct_wrapper(_NewMathFunction.factorial, 'fact')

    # permutation & combination
    comb = _Constructor._func_construct_wrapper(math.comb, 'comb')
    perm = _Constructor._func_construct_wrapper(math.perm, 'perm')

    # lcg & gcd
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
    gradtodeg = _Constructor._func_construct_wrapper(lambda x: x * (400 / 360), 'gtd')
    degtorad = _Constructor._func_construct_wrapper(lambda x: 180 / cmath.pi * x, 'dtr')
    gradtorad = _Constructor._func_construct_wrapper(lambda x: 240 / cmath.pi * x, 'gtr')
    degtograd = _Constructor._func_construct_wrapper(lambda x: x * (360 / 400), 'dtg')
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
