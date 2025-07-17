# -*- coding: utf-8 -*-


import math
from string import ascii_letters as letters
from typing import Any, Callable, Set


symbols: Set[str] = set()
allows = ['get_sign']

def unlock(*args: 'Production | Any'):
    for item in args:
        if isinstance(item, Production):
            item._locked = False

def relock(*args: 'Production | Any'):
    for item in args:
        if isinstance(item, Production):
            item._locked = True

def get_production_attributes(value: 'Production'):
    unlock(value)
    func = value._func
    tree = value._tree
    args = value._args
    relock(value)
    return func, tree, args

class Productor:
    
    @classmethod
    def product(cls, operator, 
        value1: 'Production | Any', 
        value2: 'Production | None | Any'=None, 
        level: int | None=None, 
        mode: str=''):

        match mode:
            case '1e':
                return cls.product1e(operator, value1, level)
            case '2e':
                is_pordutions = [isinstance(value1, Production), isinstance(value2, Production)]
                return cls.product2e(operator, value1, value2, is_pordutions, level)
            case 'f1e':
                return cls.productfunc1e(operator, value1)
            case 'f2e':
                is_pordutions = [isinstance(value1, Production), isinstance(value2, Production)]
                return cls.productfunc2e(operator, value1, value2, is_pordutions)
            case modstr:
                raise ValueError(f'bad mod {modstr} was given')
    
    @classmethod
    def productfunc1e(cls, func_name, value):
        func, tree, args = get_production_attributes(value)
        if func_name[:5] == 'math.':
            short_name = func_name[5:]
        else:
            short_name = func_name
        return Production(
            eval(f'lambda kwargs: {func_name}(func(kwargs))', 
                {'math': math, 
                'func': func}), 
                {'S': short_name, 'a': tree}, 
                args)

    @classmethod
    def productfunc2e(cls, func_name, value1, value2, is_productions):
        if func_name[:5] == 'math.':
            short_name = func_name[5:]
        else:
            short_name = func_name
        if (not is_productions[0]) and is_productions[1]:
            func, tree, args = get_production_attributes(value2)
            return Production(
                eval(f'lambda kwargs: {func_name}(value1, func(kwargs))',
                    {'math': math, 
                     'value1': value1, 
                    'func': func}), 
                {'S': short_name, 'a': value1, 'b': tree},
                args)

        if is_productions[1]:
            func1, tree1, args1 = get_production_attributes(value1)
            func2, tree2, args2 = get_production_attributes(value2)
            return Production(
                eval(f'lambda kwargs: {func_name}(func1(kwargs), func2(kwargs))',
                    {'math': math, 
                     'func1': func1, 
                     'func2': func2}), 
                {'S': short_name, 'a': tree1, 'b': tree2}, 
                args1 | args2)
        else:
            func, tree, args = get_production_attributes(value1)
            return Production(
                eval(f'lambda kwargs: {func_name}(func(kwargs), value2)',
                    {'math': math, 
                     'value2': value2, 
                     'func': func}),
                {'S': short_name, 'a': tree, 'b': value2}, 
                args)
    
    @classmethod
    def product1e(cls, operator, value, level):
        func, tree, args = get_production_attributes(value)
        return Production(
            eval(f'lambda kwargs: {operator}func(kwargs)', 
                {'func': func}), 
                {'O': operator, 'V': tree, 'l': level}, 
                args)

    @classmethod
    def product2e(cls, operator, left, right, is_productions, level):
        if (not is_productions[0]) and is_productions[1]:
            func, tree, args = get_production_attributes(right)
            return Production(
                eval(f'lambda kwargs: left {operator} func(kwargs)',
                    {'left': left,
                    'func': func}),
                {'L': left, 'O': operator, 'R': tree, 'l': level}, 
                args)

        if is_productions[1]:
            lfunc, ltree, largs = get_production_attributes(left)
            rfunc, rtree, rargs = get_production_attributes(right)
            return Production(
                eval(f'lambda kwargs: lfunc(kwargs) {operator} rfunc(kwargs)',
                    {'lfunc': lfunc,
                    'rfunc': rfunc}), 
                {'L': ltree, 'O': operator, 'R': rtree, 'l': level}, 
                largs | rargs)
        else:
            func, tree, args = get_production_attributes(left)
            return Production(
                eval(f'lambda kwargs: func(kwargs) {operator} right',
                    {'func': func,
                    'right': right}),
                {'L': tree, 'O': operator, 'R': right, 'l': level}, 
                args)

class Production:
    
    def __init__(self, func, tree, args):
        self._locked = True
        self._func: Callable[[dict]] = func
        self._tree: dict | str | Any = tree
        self._args: set = args

    def __getattribute__(self, __name: str):
        if __name in allows or not super().__getattribute__('_locked'):
            return super().__getattribute__(__name)
        raise AttributeError('cannot access a Production object')
        
    
    # functions with 1 element
    def __abs__(self): return Productor.product('abs', self, mode='f1e')
    def __floor__(self): return Productor.product('math.floor', self, mode='f1e')
    def __ceil__(self): return Productor.product('math.ceil', self, mode='f1e')
    def __trunc__(self): return Productor.product('math.trunc', self, mode='f1e')

    # functions with 2 elements
    def __round__(self, arg=None): return Productor.product('round', self, arg, mode='f2e')

    # operators with 1 element
    def __pos__(self): return Productor.product('+', self, level=12, mode='1e')
    def __neg__(self): return Productor.product('-', self, level=12, mode='1e')
    def __invert__(self): return Productor.product('~', self, level=12, mode='1e')

    # operators with 2 elements
    def __add__(self, other): return Productor.product('+', self, other, 10, mode='2e')
    def __sub__(self, other): return Productor.product('-', self, other, 10, mode='2e')
    def __mul__(self, other): return Productor.product('*', self, other, 11, mode='2e')
    def __floordiv__(self, other): return Productor.product('//', self, other, 11, mode='2e')
    def __truediv__(self, other): return Productor.product('/', self, other, 11, mode='2e')
    def __mod__(self, other): return Productor.product('%', self, other, 11, mode='2e')
    def __pow__(self, other): return Productor.product('**', self, other, 13, mode='2e')
    def __lshift__(self, other): return Productor.product('<<', self, other, 9, mode='2e')
    def __rshift__(self, other): return Productor.product('>>', self, other, 9, mode='2e')
    def __and__(self, other): return Productor.product('&', self, other, 8, mode='2e')
    def __xor__(self, other): return Productor.product('^', self, other, 7, mode='2e')
    def __or__(self, other): return Productor.product('|', self, other, 7, mode='2e')
    def __eq__(self, other): return Productor.product('==', self, other, 5, mode='2e')
    def __ne__(self, other): return Productor.product('!=', self, other, 5, mode='2e')
    def __lt__(self, other): return Productor.product('<', self, other, 5, mode='2e')
    def __gt__(self, other): return Productor.product('>', self, other, 5, mode='2e')
    def __le__(self, other): return Productor.product('<=', self, other, 5, mode='2e')
    def __ge__(self, other): return Productor.product('>=', self, other, 5, mode='2e')
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other): return Productor.product('+', other, self, 10, mode='2e')
    def __rsub__(self, other): return Productor.product('-', other, self, 10, mode='2e')
    def __rmul__(self, other): return Productor.product('*', other, self, 11, mode='2e')
    def __rfloordiv__(self, other): return Productor.product('//', other, self, 11, mode='2e')
    def __rtruediv__(self, other): return Productor.product('/', other, self, 11, mode='2e')
    def __rmod__(self, other): return Productor.product('%', other, self, 11, mode='2e')
    def __rpow__(self, other): return Productor.product('**', other, self, 13, mode='2e')
    def __rlshift__(self, other): return Productor.product('<<', other, self, 9, mode='2e')
    def __rrshift__(self, other): return Productor.product('>>', other, self, 9, mode='2e')
    def __rand__(self, other): return Productor.product('&', other, self, 8, mode='2e')
    def __rxor__(self, other): return Productor.product('^', other, self, 7, mode='2e')
    def __ror__(self, other): return Productor.product('|', other, self, 7, mode='2e')

class Symbol(Production):
    '''
    Argument of formula.

    Args:
        sign (str): The name of symbol.

    Attributes:
        _locked (bool): The lock that blocks access after new symbols are defined.
        _sign (str): The name of symbol.
    
    Raises:
        ValueError: The symbol sign is out of A-Z and a-z, or it has been occupied.
    '''

    def __init__(self, sign: str):
        self._locked: bool = True
        self._sign: str = sign
        unlock(self)
        if not self._check(sign):
            raise ValueError(f'{sign} is an invalid sign')
        if sign in symbols:
            raise ValueError(f'Sign {sign} has been defined')
        super().__init__(lambda kwargs: kwargs[sign], sign, {sign})
        symbols.add(sign)
        relock(self)
    
    def get_sign(self) -> str:
        '''
        Return the sign of symbol.

        Returns:
            str: The sign of symbol.
        '''
        unlock(self)
        sign = self._sign
        relock(self)
        return sign
    
    def __getattribute__(self, __name: str):
        if __name in allows or not object.__getattribute__(self, '_locked'):
            return object.__getattribute__(self, __name)
        raise AttributeError('cannot access a Production object')
    
    def _check(self, sign: str):
        if len(sign) == 1 and (sign in letters):
            return True