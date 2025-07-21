# -*- coding: utf-8 -*-


import math
from string import ascii_letters as letters, digits
from typing import Callable, NoReturn, TypeAlias, Any
from enum import Enum

from .config import *


NumericValue: TypeAlias = int | float | complex | bool
_allows = ['get_sign']

def _unlock(*args: '_Production | NumericValue') -> None:
    if SAFE_MODE:
        for item in args:
            if isinstance(item, _Production):
                item._locked = False

def _relock(*args: '_Production | NumericValue') -> None:
    if SAFE_MODE:
        for item in args:
            if isinstance(item, _Production):
                item._locked = True

def _get_production_attributes(value: '_Production') -> 'tuple[Callable[[dict], NumericValue], _Tree._ProductionTree, set[str]]':
    _unlock(value)
    func: Callable[[dict], NumericValue] = value._func
    tree: _Tree._ProductionTree = value._tree
    args: set[str] = value._args
    _relock(value)
    return func, tree, args

class _OperatorMode(Enum):
    OPERATOR1E = '1e'
    OPERATOR2E = '2e'
    FUNCTION1E = 'f1e'
    FUNCTION2E = 'f2e'

class _Tree:

    class _ProductionTree:

        def __init__(self, operator: str | None=None, level: int=0) -> None:
            self._operator: str | None = operator
            self._level: int = level

    class _NumericProductionTree(_ProductionTree):

        def __init__(self, value: NumericValue) -> None:
            super().__init__()
            self._value: NumericValue = value

    class _SymbolProductionTree(_ProductionTree):

        def __init__(self, sign: str) -> None:
            super().__init__()
            self._sign: str = sign

    class _FunctionProductionTree(_ProductionTree):

        def __init__(self, operator: str, *args: '_Tree._ProductionTree') -> None:
            super().__init__(operator)
            self._args: tuple[_Tree._ProductionTree] = args

    class _OperatorProductionTree1E(_ProductionTree):

        def __init__(self, operator: str, value: '_Tree._ProductionTree', level: int) -> None:
            super().__init__(operator, level)
            self._value: _Tree._ProductionTree = value

    class _OperatorProductionTree2E(_ProductionTree):

        def __init__(self, operator: str, value1: '_Tree._ProductionTree', value2: '_Tree._ProductionTree', level: int) -> None:
            super().__init__(operator, level)
            self._value1: _Tree._ProductionTree = value1
            self._value2: _Tree._ProductionTree = value2

class _Productor:
    
    @staticmethod
    def _product(operator: str, 
        value1: '_Production | NumericValue', 
        value2: '_Production | NumericValue | None'=None, 
        level: int=0, 
        mode: _OperatorMode='') ->' _Production':

        match mode:
            case _OperatorMode.OPERATOR1E:
                return _Productor._product1e(operator, value1, level)
            case _OperatorMode.OPERATOR2E:
                is_pordutions = [isinstance(value1, _Production), isinstance(value2, _Production)]
                return _Productor._product2e(operator, value1, value2, is_pordutions, level)
            case _OperatorMode.FUNCTION1E:
                return _Productor._productfunc1e(operator, value1)
            case _OperatorMode.FUNCTION2E:
                is_pordutions = [isinstance(value1, _Production), isinstance(value2, _Production)]
                return _Productor._productfunc2e(operator, value1, value2, is_pordutions)
            case modstr: # Never
                raise ValueError(f'bad mod {modstr} was given')
    
    @staticmethod
    def _productfunc1e(func_name: str, value: '_Production') -> '_Production':
        func, tree, args = _get_production_attributes(value)
        if func_name.startswith('math.'):
            short_name: str = func_name.removeprefix('math.')
            wrapper_func: Callable[[dict], NumericValue] = math.__dict__[short_name]
        else:
            short_name: str = func_name
            wrapper_func: Callable[[dict], NumericValue] = __builtins__[short_name]
        production_func: Callable[[dict], NumericValue] = lambda kwargs: wrapper_func(func(kwargs))
        return _Production(production_func,  _Tree._FunctionProductionTree(short_name, tree), args)

    @staticmethod
    def _productfunc2e(func_name: str, value1: '_Production | NumericValue', value2: '_Production | NumericValue', is_productions: list[bool]) -> '_Production':
        short_name: str = func_name.removeprefix('math.')
        if is_productions[0] and is_productions[1]:
            func1, tree1, args1 = _get_production_attributes(value1)
            func2, tree2, args2 = _get_production_attributes(value2)
            if func_name.startswith('math.'):
                short_name: str = func_name.removeprefix('math.')
                wrapper_func: Callable[[dict], NumericValue] = math.__dict__[short_name]
            else:
                short_name: str = func_name
                wrapper_func: Callable[[dict], NumericValue] = __builtins__[short_name]
            production_func: Callable[[dict], NumericValue] = lambda kwargs: wrapper_func(func1(kwargs), func2(kwargs))
            return _Production(production_func, _Tree._FunctionProductionTree(short_name, tree1, tree2), args1 | args2)
        
        if (not is_productions[0]) and is_productions[1]:
            func2, tree2, args2 = _get_production_attributes(value2)
            tree1: _Tree._NumericProductionTree = _Tree._NumericProductionTree(value1)
            if func_name.startswith('math.'):
                short_name: str = func_name.removeprefix('math.')
                wrapper_func: Callable[[dict], NumericValue] = math.__dict__[short_name]
            else:
                short_name: str = func_name
                wrapper_func: Callable[[dict], NumericValue] = __builtins__[short_name]
            production_func: Callable[[dict], NumericValue] = lambda kwargs: wrapper_func(value1, func2(kwargs))
            return _Production(production_func, _Tree._FunctionProductionTree(short_name, tree1, tree2), args2)
        
        else:
            func1, tree1, args1 = _get_production_attributes(value1)
            tree2: _Tree._NumericProductionTree = _Tree._NumericProductionTree(value2)
            if func_name.startswith('math.'):
                short_name: str = func_name.removeprefix('math.')
                wrapper_func: Callable[[dict], NumericValue] = math.__dict__[short_name]
            else:
                short_name: str = func_name
                wrapper_func: Callable[[dict], NumericValue] = __builtins__[short_name]
            production_func: Callable[[dict], NumericValue] = lambda kwargs: wrapper_func(func1(kwargs), value2)
            return _Production(production_func, _Tree._FunctionProductionTree(short_name, tree1, tree2), args1)
    
    @staticmethod
    def _product1e(operator: str, value: '_Production', level: int) -> '_Production':
        func, tree, args = _get_production_attributes(value)
        return _Production(
            eval(f'lambda kwargs: {operator}func(kwargs)', 
                {'func': func}), 
                _Tree._OperatorProductionTree1E(operator, tree, level), 
                args)

    @staticmethod
    def _product2e(operator: str, left: '_Production | NumericValue', right: '_Production | NumericValue', is_productions: list[bool], level: int) -> '_Production':
        if is_productions[0] and is_productions[1]:
            lfunc, ltree, largs = _get_production_attributes(left)
            rfunc, rtree, rargs = _get_production_attributes(right)
            return _Production(
                eval(f'lambda kwargs: lfunc(kwargs) {operator} rfunc(kwargs)',
                    {'lfunc': lfunc,
                    'rfunc': rfunc}), 
                _Tree._OperatorProductionTree2E(operator, ltree, rtree, level), 
                largs | rargs)
        
        if (not is_productions[0]) and is_productions[1]:
            rfunc, rtree, rargs = _get_production_attributes(right)
            ltree: _Tree._NumericProductionTree = _Tree._NumericProductionTree(left)
            return _Production(
                eval(f'lambda kwargs: left {operator} func(kwargs)',
                    {'left': left,
                    'func': rfunc}),
                _Tree._OperatorProductionTree2E(operator, ltree, rtree, level), 
                rargs)

        else:
            lfunc, ltree, largs = _get_production_attributes(left)
            rtree: _Tree._NumericProductionTree = _Tree._NumericProductionTree(right)
            return _Production(
                eval(f'lambda kwargs: func(kwargs) {operator} right',
                    {'func': lfunc,
                    'right': right}),
                _Tree._OperatorProductionTree2E(operator, ltree, rtree, level), 
                largs)

class _Production:
    
    def __init__(self, func: Callable[[dict], NumericValue], tree: _Tree._ProductionTree, args: set[str]) -> None:
        self._locked: bool = False
        self._func: Callable[[dict], NumericValue] = func
        self._tree: _Tree._ProductionTree = tree
        self._args: set[str] = args
        _relock(self)
    
    def __getattribute__(self, __name: str) -> Any | NoReturn:
        if (__name in _allows) or \
        (not super().__getattribute__('_locked')) or \
        (not SAFE_MODE):
            return super().__getattribute__(__name)
        raise AttributeError('cannot access a Production object')
        
    
    # functions with 1 element
    def __abs__(self): return _Productor._product('abs', self, mode=_OperatorMode.FUNCTION1E)
    def __floor__(self): return _Productor._product('math.floor', self, mode=_OperatorMode.FUNCTION1E)
    def __ceil__(self): return _Productor._product('math.ceil', self, mode=_OperatorMode.FUNCTION1E)
    def __trunc__(self): return _Productor._product('math.trunc', self, mode=_OperatorMode.FUNCTION1E)

    # functions with 2 elements
    def __round__(self, arg=0): return _Productor._product('round', self, arg, mode=_OperatorMode.FUNCTION2E)

    # operators with 1 element
    def __pos__(self): return _Productor._product('+', self, level=12, mode=_OperatorMode.OPERATOR1E)
    def __neg__(self): return _Productor._product('-', self, level=12, mode=_OperatorMode.OPERATOR1E)
    def __invert__(self): return _Productor._product('~', self, level=12, mode=_OperatorMode.OPERATOR1E)

    # operators with 2 elements
    def __add__(self, other): return _Productor._product('+', self, other, 10, mode=_OperatorMode.OPERATOR2E)
    def __sub__(self, other): return _Productor._product('-', self, other, 10, mode=_OperatorMode.OPERATOR2E)
    def __mul__(self, other): return _Productor._product('*', self, other, 11, mode=_OperatorMode.OPERATOR2E)
    def __floordiv__(self, other): return _Productor._product('//', self, other, 11, mode=_OperatorMode.OPERATOR2E)
    def __truediv__(self, other): return _Productor._product('/', self, other, 11, mode=_OperatorMode.OPERATOR2E)
    def __mod__(self, other): return _Productor._product('%', self, other, 11, mode=_OperatorMode.OPERATOR2E)
    def __pow__(self, other): return _Productor._product('**', self, other, 13, mode=_OperatorMode.OPERATOR2E)
    def __lshift__(self, other): return _Productor._product('<<', self, other, 9, mode=_OperatorMode.OPERATOR2E)
    def __rshift__(self, other): return _Productor._product('>>', self, other, 9, mode=_OperatorMode.OPERATOR2E)
    def __and__(self, other): return _Productor._product('&', self, other, 8, mode=_OperatorMode.OPERATOR2E)
    def __xor__(self, other): return _Productor._product('^', self, other, 7, mode=_OperatorMode.OPERATOR2E)
    def __or__(self, other): return _Productor._product('|', self, other, 7, mode=_OperatorMode.OPERATOR2E)
    def __eq__(self, other): return _Productor._product('==', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    def __ne__(self, other): return _Productor._product('!=', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    def __lt__(self, other): return _Productor._product('<', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    def __gt__(self, other): return _Productor._product('>', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    def __le__(self, other): return _Productor._product('<=', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    def __ge__(self, other): return _Productor._product('>=', self, other, 5, mode=_OperatorMode.OPERATOR2E)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other): return _Productor._product('+', other, self, 10, mode=_OperatorMode.OPERATOR2E)
    def __rsub__(self, other): return _Productor._product('-', other, self, 10, mode=_OperatorMode.OPERATOR2E)
    def __rmul__(self, other): return _Productor._product('*', other, self, 11, mode=_OperatorMode.OPERATOR2E)
    def __rfloordiv__(self, other): return _Productor._product('//', other, self, 11, mode=_OperatorMode.OPERATOR2E)
    def __rtruediv__(self, other): return _Productor._product('/', other, self, 11, mode=_OperatorMode.OPERATOR2E)
    def __rmod__(self, other): return _Productor._product('%', other, self, 11, mode=_OperatorMode.OPERATOR2E)
    def __rpow__(self, other): return _Productor._product('**', other, self, 13, mode=_OperatorMode.OPERATOR2E)
    def __rlshift__(self, other): return _Productor._product('<<', other, self, 9, mode=_OperatorMode.OPERATOR2E)
    def __rrshift__(self, other): return _Productor._product('>>', other, self, 9, mode=_OperatorMode.OPERATOR2E)
    def __rand__(self, other): return _Productor._product('&', other, self, 8, mode=_OperatorMode.OPERATOR2E)
    def __rxor__(self, other): return _Productor._product('^', other, self, 7, mode=_OperatorMode.OPERATOR2E)
    def __ror__(self, other): return _Productor._product('|', other, self, 7, mode=_OperatorMode.OPERATOR2E)

class Symbol(_Production):
    '''
    Argument of formula.

    Args:
        sign (str): The name of symbol.
    
    Raises:
        ValueError: The symbol sign is out of A-Z and a-z, or it has been occupied.
    '''

    def __init__(self, sign: str) -> None:
        self._locked: bool = False
        self._sign: str = sign
        if not self._check(sign):
            raise ValueError(f'{sign} is an invalid sign')
        tree: _Tree._SymbolProductionTree = _Tree._SymbolProductionTree(sign)
        super().__init__(lambda kwargs: kwargs[sign], tree, {sign})
        _relock(self)
    
    def get_sign(self) -> str:
        '''
        Return the sign of symbol.

        Returns:
            str: The sign of symbol.
        '''
        _unlock(self)
        sign: str = self._sign
        _relock(self)
        return sign
    
    def __getattribute__(self, __name: str) -> Any | NoReturn:
        if (__name in _allows) or \
        (not object.__getattribute__(self, '_locked')) or \
        (not SAFE_MODE):
            return object.__getattribute__(self, __name)
        raise AttributeError('cannot access a Production object')
    
    def _check(self, sign: str) -> bool:
        if len(sign) == 0: return False
        if sign[0] in letters:
            if (len(sign) > 1 and all([ch in digits for ch in sign[1:]])) or \
            len(sign) == 1:
                return True
            return False
        return False
        
