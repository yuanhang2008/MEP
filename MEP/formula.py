# -*- coding:utf-8 -*-


import math
from typing import Callable, NoReturn, overload

from .config import *
from .production import _Production, _relock, _unlock, NumericValue, _Tree

# from.draw import Draw


_named_formulas: 'dict[str, Formula]' = {}

def _name_check(name: str) -> 'Formula | NoReturn':
    formula: Formula | None = _named_formulas.get(name, None)
    if formula is None:
        raise ValueError(f'No such a formula named {name}')
    return formula

def _to_production(v: 'Formula | NumericValue') -> _Production | NumericValue:
    if isinstance(v, Formula):
        return v._formula._production
    return v

def call(name: str, **kwargs: NumericValue) -> 'Expression | NoReturn':
    '''
    Call a named formula with arguments.

    Args:
        name (str): The name of formula to be call.
        **kwargs: The arguments to call the formula.
    
    Returns:
        Expression: Expression after substituting into the formula.
    
    Raises:
        ValueError: No such a formula named...
    '''
    formula = _name_check(name)
    return formula.subs(**kwargs)

def find(name: str) -> 'Formula | NoReturn':
    '''
    Get a formula matches the name.

    Args:
        name (str): The name of formula to be match.
    
    Returns:
        Formula: Formula that matches the name.
    
    Raises:
        ValueError: No such a formula named...
    '''
    formula = _name_check(name)
    return formula

class Formula:
    '''
    Math expression with arguments.

    Args:
        production (_Production): The expression with arguments.
        name (str): Name of a formula.

    Attributes:
        _formula (_Formula): The corresponding unencapsulated object of formula.
    '''

    def __init__(self, production: _Production, name: str | None=None) -> None:
        self._formula = _Formula(production)
        if name is not None:
            _named_formulas[name] = self
    
    def subs(self, **kwargs: NumericValue) -> 'Expression':
        '''
        Substituting arguments into formula.

        Args:
            **kwargs: The value of each arguments.
        
        Returns:
            Expression: Math expression after substituting.
        
        Raises:
            ValueError: 
                The given arguments does not match formula's argument set, 
                or non-numeric type is given.
        '''
        return self._formula._subs(**kwargs)
    
    #def draw(self, range_: tuple) -> None:
    #    '''
    #    Store formula in the cache to show.
    #
    #    Args:
    #        range_ (tuple[int]): The start point and end point that formula shows.
    #    '''
    #    self._formula._draw(range_)

    def curry(self, **kwargs: NumericValue) -> 'Formula':
        '''
        Substituting partial arguments and currying the formula.

        Args:
            **kwargs: The value of arguments that substituting.
        
        Returns:
            Formula: Formula with unsubstituted arguments after currying.
        
        Raises:
            ValueError:
                The given arguments does not match formula's argument set, 
                or non-numeric type is given.
        '''
        return self._formula._curry(**kwargs)

    def text(self) -> str:
        '''
        Represent formula mathematically.

        Returns:
            str: Mathematical text of formula.
        '''
        return self._formula._text()

    def __str__(self) -> str:
        '''
        Literal of formula.

        Returns:
            str: a literal value of formula with its arguments and mathematical text.
        '''
        return self._formula.__str__()
    
    # functions with 1 element
    def __abs__(self): return self._formula.__abs__()
    def __floor__(self): return self._formula.__floor__()
    def __ceil__(self): return self._formula.__ceil__()
    def __trunc__(self): return self._formula.__trunc__()

    # functions with 2 elements
    def __round__(self, arg=0): return self._formula.__round__(arg)

    # operators with 1 element
    def __pos__(self): return self._formula.__pos__()
    def __neg__(self): return self._formula.__neg__()
    def __invert__(self): return self._formula.__invert__()

    # operators with 2 elements
    def __add__(self, other): return self._formula.__add__(other)
    def __sub__(self, other): return self._formula.__sub__(other)
    def __mul__(self, other): return self._formula.__mul__(other)
    def __floordiv__(self, other): return self._formula.__floordiv__(other)
    def __truediv__(self, other): return self._formula.__truediv__(other)
    def __mod__(self, other): return self._formula.__mod__(other)
    def __pow__(self, other): return self._formula.__pow__(other)
    def __lshift__(self, other): return self._formula.__lshift__(other)
    def __rshift__(self, other): return self._formula.__rshift__(other)
    def __and__(self, other): return self._formula.__and__(other)
    def __xor__(self, other): return self._formula.__xor__(other)
    def __or__(self, other): return self._formula.__or__(other)
    def __eq__(self, other): return self._formula.__eq__(other)
    def __ne__(self, other): return self._formula.__ne__(other)
    def __lt__(self, other): return self._formula.__lt__(other)
    def __gt__(self, other): return self._formula.__gt__(other)
    def __le__(self, other): return self._formula.__le__(other)
    def __ge__(self, other): return self._formula.__ge__(other)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other): return self._formula.__radd__(other)
    def __rsub__(self, other): return self._formula.__rsub__(other)
    def __rmul__(self, other): return self._formula.__rmul__(other)
    def __rfloordiv__(self, other): return self._formula.__rfloordiv__(other)
    def __rtruediv__(self, other): return self._formula.__rtruediv__(other)
    def __rmod__(self, other): return self._formula.__rmod__(other)
    def __rpow__(self, other): return self._formula.__rpow__(other)
    def __rlshift__(self, other): return self._formula.__rlshift__(other)
    def __rrshift__(self, other): return self._formula.__rrshift__(other)
    def __rand__(self, other): return self._formula.__rand__(other)
    def __rxor__(self, other): return self._formula.__rxor__(other)
    def __ror__(self, other): return self._formula.__ror__(other)

class Expression:
    '''
    Mathematical expression for pure numbers.

    Args:
        production (_Production): The production of expression.

    Attributes:
        _expression (_Expression): The corresponding unencapsulated object of expression.
    '''

    @overload
    def __init__(self, production: _Production) -> None: ...
    
    @overload
    def __init__(self, _func: Callable[[dict], NumericValue], _exp: str, _kwargs: dict[str, NumericValue]) -> None: ...
    
    def __init__(self, production: _Production=None, _func: Callable[[dict], NumericValue]=None, _exp: str=None, _kwargs: dict[str, NumericValue]=None) -> None:
        if production is None and \
        _func is not None and \
        _exp is not None and \
        _kwargs is not None:
            self._expression: _Expression = _Expression(_func, _exp, _kwargs)
        
        elif production is not None and \
        _func is None and \
        _exp is None and \
        _kwargs is None:
            _unlock(production)
            if production._args == set():
                self._production: _Production = production
                _func: Callable[[dict], NumericValue] = self._production._func
                _exp: str = _TreeParser._get_tree_str(self._production._tree)
                _kwargs: dict[str, NumericValue] = {}
                self._expression: _Expression = _Expression(_func, _exp, _kwargs)
            else:
                raise ValueError('Arguments cannot be carried in expression production.')
        
        else:
            raise ValueError('Unexpected argument(s) in Expression object.')

    def value(self) -> NumericValue:
        '''
        Return the value of expression.

        Returns:
            NumericValue: The value of expression after calculating.
        '''
        return self._expression._value()
    
    def text(self) -> str:
        '''
        Represent expression mathematically.

        Returns:
            str: Mathematical text of expression.
        '''
        return self._expression._text()
    
    def __str__(self) -> str:
        '''
        Literal of expression.

        Returns:
            str: a literal value of expression with its arguments of formula and mathematical text.
        '''
        return self._expression.__str__()

    # functions with 1 element
    def __abs__(self): return self._expression.__abs__()
    def __floor__(self): return self._expression.__floor__()
    def __ceil__(self): return self._expression.__ceil__()
    def __trunc__(self): return self._expression.__trunc__()

    # functions with 2 elements
    def __round__(self, arg=0): return self._expression.__round__(arg)

    # operators with 1 element
    def __pos__(self): return self._expression.__pos__()
    def __neg__(self): return self._expression.__neg__()
    def __invert__(self): return self._expression.__invert__()

    # operators with 2 elements
    def __add__(self, other): return self._expression.__add__(other)
    def __sub__(self, other): return self._expression.__sub__(other)
    def __mul__(self, other): return self._expression.__mul__(other)
    def __floordiv__(self, other): return self._expression.__floordiv__(other)
    def __truediv__(self, other): return self._expression.__truediv__(other)
    def __mod__(self, other): return self._expression.__mod__(other)
    def __pow__(self, other): return self._expression.__pow__(other)
    def __lshift__(self, other): return self._expression.__lshift__(other)
    def __rshift__(self, other): return self._expression.__rshift__(other)
    def __and__(self, other): return self._expression.__and__(other)
    def __xor__(self, other): return self._expression.__xor__(other)
    def __or__(self, other): return self._expression.__or__(other)
    def __eq__(self, other): return self._expression.__eq__(other)
    def __ne__(self, other): return self._expression.__ne__(other)
    def __lt__(self, other): return self._expression.__lt__(other)
    def __gt__(self, other): return self._expression.__gt__(other)
    def __le__(self, other): return self._expression.__le__(other)
    def __ge__(self, other): return self._expression.__ge__(other)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other): return self._expression.__radd__(other)
    def __rsub__(self, other): return self._expression.__rsub__(other)
    def __rmul__(self, other): return self._expression.__rmul__(other)
    def __rfloordiv__(self, other): return self._expression.__rfloordiv__(other)
    def __rtruediv__(self, other): return self._expression.__rtruediv__(other)
    def __rmod__(self, other): return self._expression.__rmod__(other)
    def __rpow__(self, other): return self._expression.__rpow__(other)
    def __rlshift__(self, other): return self._expression.__rlshift__(other)
    def __rrshift__(self, other): return self._expression.__rrshift__(other)
    def __rand__(self, other): return self._expression.__rand__(other)
    def __rxor__(self, other): return self._expression.__rxor__(other)
    def __ror__(self, other): return self._expression.__ror__(other)

class _TreeParser:

    @staticmethod
    def _get_tree_str(tree: _Tree._ProductionTree, parent_level: int=0) -> str:
        if isinstance(tree, _Tree._NumericProductionTree):
            return str(tree._value)
        if isinstance(tree, _Tree._SymbolProductionTree):
            return f'{SIGN_CH_L}{tree._sign}{SIGN_CH_R}'
        if isinstance(tree, _Tree._FunctionProductionTree):
            return _TreeParser._get_func_tree_str(tree)
        if isinstance(tree, _Tree._OperatorProductionTree1E):
            return _TreeParser._get_ovl_tree_str(tree)
        if isinstance(tree, _Tree._OperatorProductionTree2E):
            return _TreeParser._get_lor_tree_str(tree, parent_level)
        raise ValueError(f'Bad tree was given')

    @staticmethod
    def _get_func_tree_str(tree: _Tree._FunctionProductionTree) -> str:
        args: list[str] = []
        for subtree in tree._args:
            arg: str = _TreeParser._get_tree_str(subtree, tree._level)
            args.append(arg)
        func_text: str = tree._operator
        args_text: str = ''.join((f'{item}, ' for item in args if item)).removesuffix(', ')
        return f'{func_text}({args_text})'

    @staticmethod
    def _get_ovl_tree_str(tree: _Tree._OperatorProductionTree1E) -> str:
        value_str: str = _TreeParser._get_tree_str(tree._value, tree._level)
        return f'({tree._operator}{value_str})'

    @staticmethod
    def _get_lor_tree_str(tree: _Tree._OperatorProductionTree2E, parent_level: int) -> str:
        l_subtree_str: str = _TreeParser._get_tree_str(tree._value1, tree._level)
        r_subtree_str: str = _TreeParser._get_tree_str(tree._value2, tree._level)
        l_filler, r_filler = ('(', ')') if parent_level > tree._level else ('', '')
        return f'{l_filler}{l_subtree_str}{tree._operator}{r_subtree_str}{r_filler}'

class _Formula:

    def __init__(self, production: _Production | NumericValue) -> None:
        self._production: _Production | NumericValue = production
        _unlock(self._production)
        if not isinstance(self._production, _Production):
            if isinstance(self._production, NumericValue):
                self._func: Callable[[dict], NumericValue] = lambda _: self._production
                self._tree: _Tree._NumericProductionTree = _Tree._NumericProductionTree(self._production)
                self._args: set[str] = set()
            else:
                raise TypeError(f'Formula() argument must be a Production or NumericValue, not \'{type(production)}\'')
        else:
            self._func: Callable[[dict], NumericValue] = self._production._func
            self._tree: _Tree._ProductionTree = self._production._tree
            self._args: set[str] = self._production._args
        self._tree_str: str = _TreeParser._get_tree_str(self._tree)
        _relock(self._production)
    
    def _subs(self, **kwargs: NumericValue) -> Expression:
        args: set[str] = set(kwargs)
        if args != self._args:
            raise ValueError(f'arguments do not match')
        return Expression(None, self._func, self._tree_str, kwargs)

    # def _draw(self, range_: tuple):
    #     Draw._drawer._add_func(self, range_)

    def _curry(self, **kwargs: dict[str, NumericValue]) -> Formula:
        args: set[str] = self._args.copy()
        tree: _Tree._ProductionTree = self._tree_curry(self._tree, kwargs)
        for key in kwargs:
            if key not in args:
                raise ValueError(f'arguments do not match')
            args.remove(key)

        def wapper(kwargs_: dict[str, NumericValue]) -> NumericValue:
            for key in kwargs:
                kwargs_[key] = kwargs[key]
            return self._func(kwargs_)
        
        return Formula(_Production(wapper, tree, args))
    
    def _tree_curry(self, tree: _Tree._ProductionTree, kwargs: dict[str, NumericValue]) -> _Tree._ProductionTree:
        if isinstance(tree, _Tree._SymbolProductionTree):
            if tree._sign in kwargs.keys():
                return _Tree._NumericProductionTree(kwargs[tree._sign])
            return _Tree._SymbolProductionTree(tree._sign)
        
        if isinstance(tree, _Tree._FunctionProductionTree):
            args: list[_Tree._ProductionTree] = []
            for arg in tree._args:
                args.append(self._tree_curry(arg, kwargs))
            return _Tree._FunctionProductionTree(tree._operator, args)
        
        if isinstance(tree, _Tree._OperatorProductionTree1E):
            return _Tree._OperatorProductionTree1E(tree._operator, self._tree_curry(tree._value), tree._level)
        if isinstance(tree, _Tree._OperatorProductionTree2E):
            return _Tree._OperatorProductionTree2E(tree._operator, self._tree_curry(tree._value1), self._tree_curry(tree._value2), tree._level)
        if isinstance(tree, _Tree._NumericProductionTree):
            return _Tree._NumericProductionTree(tree._value)
        raise ValueError('Bad tree was given.')
    
    def _text(self) -> str:
        tree_text: str = self._tree_str.replace(SIGN_CH_L, '').replace(SIGN_CH_R, '')
        return tree_text

    def __str__(self) -> str:
        formula_text: str = self._text()
        args: list[str] = [f'{arg}, 'for arg in self._args]

        args_text = ''.join(args).removesuffix(', ')
        return f'<Formula f({args_text})={formula_text}>'
    
    # functions with 1 element
    def __abs__(self): p = abs(self._production);return Formula(p)
    def __floor__(self): p = math.floor(self._production);return Formula(p)
    def __ceil__(self): p = math.ceil(self._production);return Formula(p)
    def __trunc__(self): p = math.trunc(self._production);return Formula(p)

    # functions with 2 elements
    def __round__(self, arg: 'Formula | NumericValue'=0): p = round(self._production, _to_production(arg));return Formula(p)

    # operators with 1 element
    def __pos__(self): p = +self._production;return Formula(p)
    def __neg__(self): p = -self._production;return Formula(p)
    def __invert__(self): p = ~self._production;return Formula(p)

    # operators with 2 elements
    def __add__(self, other: 'Formula | NumericValue'): p = self._production + _to_production(other);return Formula(p)
    def __sub__(self, other: 'Formula | NumericValue'): p = self._production - _to_production(other);return Formula(p)
    def __mul__(self, other: 'Formula | NumericValue'): p = self._production * _to_production(other);return Formula(p)
    def __floordiv__(self, other: 'Formula | NumericValue'): p = self._production // _to_production(other);return Formula(p)
    def __truediv__(self, other: 'Formula | NumericValue'): p = self._production / _to_production(other);return Formula(p)
    def __mod__(self, other: 'Formula | NumericValue'): p = self._production % _to_production(other);return Formula(p)
    def __pow__(self, other: 'Formula | NumericValue'): p = self._production ** _to_production(other);return Formula(p)
    def __lshift__(self, other: 'Formula | NumericValue'): p = self._production << _to_production(other);return Formula(p)
    def __rshift__(self, other: 'Formula | NumericValue'): p = self._production >> _to_production(other);return Formula(p)
    def __and__(self, other: 'Formula | NumericValue'): p = self._production & _to_production(other);return Formula(p)
    def __xor__(self, other: 'Formula | NumericValue'): p = self._production ^ _to_production(other);return Formula(p)
    def __or__(self, other: 'Formula | NumericValue'): p = self._production | _to_production(other);return Formula(p)
    def __eq__(self, other: 'Formula | NumericValue'): p = self._production == _to_production(other);return Formula(p)
    def __ne__(self, other: 'Formula | NumericValue'): p = self._production != _to_production(other);return Formula(p)
    def __lt__(self, other: 'Formula | NumericValue'): p = self._production < _to_production(other);return Formula(p)
    def __gt__(self, other: 'Formula | NumericValue'): p = self._production > _to_production(other);return Formula(p)
    def __le__(self, other: 'Formula | NumericValue'): p = self._production <= _to_production(other);return Formula(p)
    def __ge__(self, other: 'Formula | NumericValue'): p = self._production >= _to_production(other);return Formula(p)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other: 'Formula | NumericValue'): p = _to_production(other) + self._production;return Formula(p)
    def __rsub__(self, other: 'Formula | NumericValue'): p = _to_production(other) - self._production;return Formula(p)
    def __rmul__(self, other: 'Formula | NumericValue'): p = _to_production(other) * self._production;return Formula(p)
    def __rfloordiv__(self, other: 'Formula | NumericValue'): p = _to_production(other) // self._production;return Formula(p)
    def __rtruediv__(self, other: 'Formula | NumericValue'): p = _to_production(other) / self._production;return Formula(p)
    def __rmod__(self, other: 'Formula | NumericValue'): p = _to_production(other) % self._production;return Formula(p)
    def __rpow__(self, other: 'Formula | NumericValue'): p = _to_production(other) ** self._production;return Formula(p)
    def __rlshift__(self, other: 'Formula | NumericValue'): p = _to_production(other) << self._production;return Formula(p)
    def __rrshift__(self, other: 'Formula | NumericValue'): p = _to_production(other) >> self._production;return Formula(p)
    def __rand__(self, other: 'Formula | NumericValue'): p = _to_production(other) & self._production;return Formula(p)
    def __rxor__(self, other: 'Formula | NumericValue'): p = _to_production(other) ^ self._production;return Formula(p)
    def __ror__(self, other: 'Formula | NumericValue'): p = _to_production(other) | self._production;return Formula(p)

class _Expression:

    def __init__(self, func: Callable[[dict], NumericValue], exp: str, kwargs: dict[str, NumericValue]) -> None:
        self._expression_text_with_signs: str = exp
        self._kwargs: dict[str, NumericValue] = kwargs
        self._func: Callable[[dict], NumericValue] = func
        # self._tree: _Tree._ProductionTree = self._tree_subs(tree, kwargs)

    def _value(self) -> NumericValue:
        return self._func(self._kwargs)
    
    # def _tree_subs(self, tree: dict | str | NumericValue, kwargs: dict[str, NumericValue]) -> dict | NumericValue:
    #     match self._tree_type:
    #         case _TreeType.NUMERICVALUE:
    #             return str(tree)
    #         case _TreeType.SYMBOL:
    #             return kwargs.get(tree)
    #         case _TreeType.FUNCTIONTREE:
    #             for item in tree:
    #                 if item != 'S':
    #                     tree[item] = self._tree_subs(tree[item], kwargs)
    #             return tree
    #         case _TreeType.OPERATOR1ETREE:
    #             tree['V'] = self._tree_subs(tree['V'], kwargs)
    #             return tree
    #         case _TreeType.OPERATOR2ETREE:
    #             tree['L'] = self._tree_subs(tree['L'], kwargs)
    #             tree['R'] = self._tree_subs(tree['R'], kwargs)
    #             return tree
    
    def _text(self) -> str:
        expression_text: str = ''
        pos: int = 0
        while pos < len(self._expression_text_with_signs):
            char = self._expression_text_with_signs[pos]
            if char != SIGN_CH_L:
                expression_text += char
            else:
                left: int = pos + 1
                while self._expression_text_with_signs[pos] != SIGN_CH_R:
                    pos += 1
                right: int = pos
                symbol: str = self._expression_text_with_signs[left:right]
                arg_value: NumericValue = self._kwargs[symbol]
                value_str: str = str(arg_value)
                is_negative: bool = (not isinstance(arg_value, complex)) and arg_value < 0
                if is_negative:
                    value_str = f'({value_str})'
                expression_text += value_str
            pos += 1
        return expression_text

    def __str__(self) -> str:
        fargs = [f'{key}={self._kwargs[key]}, ' for key in self._kwargs]
        args_text = ''.join(fargs).removesuffix(', ')
        return f'<Expression f({args_text})={self._text()}>'
    
    # unfinished
    # functions with 1 element
    def __abs__(self): return self._expression.__abs__()
    def __floor__(self): return self._expression.__floor__()
    def __ceil__(self): return self._expression.__ceil__()
    def __trunc__(self): return self._expression.__trunc__()

    # functions with 2 elements
    def __round__(self, arg=0): return self._expression.__round__(arg)

    # operators with 1 element
    def __pos__(self): return self._expression.__pos__()
    def __neg__(self): return self._expression.__neg__()
    def __invert__(self): return self._expression.__invert__()

    # operators with 2 elements
    def __add__(self, other): return self._expression.__add__(other)
    def __sub__(self, other): return self._expression.__sub__(other)
    def __mul__(self, other): return self._expression.__mul__(other)
    def __floordiv__(self, other): return self._expression.__floordiv__(other)
    def __truediv__(self, other): return self._expression.__truediv__(other)
    def __mod__(self, other): return self._expression.__mod__(other)
    def __pow__(self, other): return self._expression.__pow__(other)
    def __lshift__(self, other): return self._expression.__lshift__(other)
    def __rshift__(self, other): return self._expression.__rshift__(other)
    def __and__(self, other): return self._expression.__and__(other)
    def __xor__(self, other): return self._expression.__xor__(other)
    def __or__(self, other): return self._expression.__or__(other)
    def __eq__(self, other): return self._expression.__eq__(other)
    def __ne__(self, other): return self._expression.__ne__(other)
    def __lt__(self, other): return self._expression.__lt__(other)
    def __gt__(self, other): return self._expression.__gt__(other)
    def __le__(self, other): return self._expression.__le__(other)
    def __ge__(self, other): return self._expression.__ge__(other)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other): return self._expression.__radd__(other)
    def __rsub__(self, other): return self._expression.__rsub__(other)
    def __rmul__(self, other): return self._expression.__rmul__(other)
    def __rfloordiv__(self, other): return self._expression.__rfloordiv__(other)
    def __rtruediv__(self, other): return self._expression.__rtruediv__(other)
    def __rmod__(self, other): return self._expression.__rmod__(other)
    def __rpow__(self, other): return self._expression.__rpow__(other)
    def __rlshift__(self, other): return self._expression.__rlshift__(other)
    def __rrshift__(self, other): return self._expression.__rrshift__(other)
    def __rand__(self, other): return self._expression.__rand__(other)
    def __rxor__(self, other): return self._expression.__rxor__(other)
    def __ror__(self, other): return self._expression.__ror__(other)
