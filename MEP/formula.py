# -*- coding:utf-8 -*-


import math
from typing import Callable, NoReturn

from .config import *
from .production import _Production, _relock, _unlock, NumericValue, _TreeType

# from.draw import Draw


_named_formulas: 'dict[str, Formula]' = {}

def _name_check(name: str) -> 'Formula | NoReturn':
    formula: Formula | None = _named_formulas.get(name, None)
    if formula is None:
        raise ValueError(f'No such a formula named {name}')
    return formula

def call(name: str, **kwargs) -> 'Expression | NoReturn':
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
    
    def subs(self, **kwargs: dict[str, NumericValue]) -> 'Expression':
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

    def curry(self, **kwargs: dict[str, NumericValue]) -> 'Formula':
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
    def __round__(self, arg): return self._formula.__round__(arg)

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
        func (Callable): Function for calculating value.
        exp (str): Mathematical text.
        kwargs (dict): arguments that substituting.
        args (set): argument set of corresponding formula.
        tree: The tree structure of formula operations.

    Attributes:
        _expression (_Expression): The corresponding unencapsulated object of expression.
    '''

    def __init__(self, func: Callable[[dict], NumericValue], exp: str, kwargs: dict, args: set, tree: dict | str | NumericValue) -> None:
        self._expression = _Expression(func, exp, kwargs, args, tree)

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
    def __round__(self, arg): return self._expression.__round__(arg)

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

class _Formula:

    def __init__(self, production: _Production | NumericValue) -> None:
        self._production: _Production | NumericValue = production
        _unlock(self._production)
        if not isinstance(self._production, _Production):
            if isinstance(self._production, int) or \
            isinstance(self._production, float) or \
            isinstance(self._production, complex) or \
            isinstance(self._production, bool):
                self._func: Callable[[dict], NumericValue] = lambda _: self._production
                self._tree: NumericValue = self._production
                self._args: set[str] = set()
                self._tree_type: _TreeType = _TreeType.NUMERICVALUE
            else:
                raise TypeError(f'Formula() argument must be a Production or NumericValue, not \'{type(production)}\'')
        else:
            self._func: Callable[[dict], NumericValue] = self._production._func
            self._tree: dict | str| NumericValue = self._production._tree
            self._args: set[str] = self._production._args
            self._tree_type: _TreeType = self._production._tree_type
        self._tree_str: str = self._get_tree_str(self._tree)
        _relock(self._production)
    
    def _subs(self, **kwargs: dict[str, NumericValue]) -> Expression:
        args: set[str] = set(kwargs)
        if args != self._args:
            raise ValueError(f'arguments do not match')
        return Expression(self._func, self._tree_str, kwargs, self._args, self._tree, self._tree_type)

    # def _draw(self, range_: tuple):
    #     Draw._drawer._add_func(self, range_)
    
    def _get_tree_str(self, tree: dict | str | NumericValue, level: int=0) -> str:
        match self._tree_type:
            case _TreeType.NUMERICVALUE:
                return str(tree)
            case _TreeType.SYMBOL:
                return SIGN_CH + tree
            case _TreeType.FUNCTIONTREE:
                return self._get_func_tree_str(tree)
            case _TreeType.OPERATOR1ETREE:
                return self._get_ovl_tree_str(tree)
            case _TreeType.OPERATOR2ETREE:
                return self._get_lor_tree_str(tree, level)

    def _get_func_tree_str(self, tree: dict[str, dict | str | NumericValue]) -> str:
        args: list[str] = []
        for item in tree:
            subtree: NumericValue | dict | str = tree[item]
            arg: str = self._get_tree_str(subtree)
            if item != 'S':
                args.append(arg)
        func_text: str = tree["S"]
        args_text: str = ''.join((''.join((item, ', ')) for item in args if item)).removesuffix(', ')
        return f'{func_text}({args_text})'
    
    def _get_ovl_tree_str(self, tree: dict[str, dict | str | NumericValue]) -> str:
        subtree_str = self._get_tree_str(tree['V'])
        return ''.join(('(', tree['O'], subtree_str, ')'))

    def _get_lor_tree_str(self, tree: dict[str, dict | str | NumericValue], level: int) -> str:
        use_brackets: bool = True if level > tree['l'] else False
        l_subtree_str = self._get_tree_str(tree['L'])
        r_subtree_str = self._get_tree_str(tree['R'])
        l_filler, r_filler = ('(', ')') if use_brackets else ('', '')
        return ''.join((l_filler, l_subtree_str, tree['O'], r_subtree_str, r_filler))

    def _curry(self, **kwargs: dict[str, NumericValue]) -> Formula:
        args: set[str] = self._args.copy()
        tree: dict | str | NumericValue = self._tree_curry(self._tree, kwargs)
        for key in kwargs:
            if key not in args:
                raise ValueError(f'arguments do not match')
            args.remove(key)

        def wapper(kwargs_: dict[str, NumericValue]) -> NumericValue:
            for key in kwargs:
                kwargs_[key] = kwargs[key]
            return self._func(kwargs_)
        
        return Formula(_Production(wapper, tree, args))
    
    def _tree_curry(self, tree: dict | str, kwargs: dict[str, NumericValue]) -> dict | str | NumericValue:
        if isinstance(tree, str):
            if tree in kwargs.keys():
                return kwargs[tree]
            return tree
        
        if 'S' in tree.keys():
            for key in tree:
                if key != 'S' and isinstance(tree[key], str | dict):
                    tree[key] = self._tree_curry(tree[key], kwargs)
            return tree
        
        if isinstance(tree['L'], str | dict):
            tree['L'] = self._tree_curry(tree['L'], kwargs)
        if isinstance(tree['R'], str | dict):
            tree['R'] = self._tree_curry(tree['R'], kwargs)
        return tree
    
    def _text(self) -> str:
        tree_text: str = self._tree_str.replace(SIGN_CH, '')
        return tree_text

    def __str__(self) -> str:
        formula_text = self._text()
        fargs = [f'{arg}, 'for arg in self._args]
        args_text = ''.join(fargs).removesuffix(', ')
        return f'<Formula f({args_text})={formula_text}>'
    
    # functions with 1 element
    def __abs__(self): p = abs(self._production);return Formula(p)
    def __floor__(self): p = math.floor(self._production);return Formula(p)
    def __ceil__(self): p = math.ceil(self._production);return Formula(p)
    def __trunc__(self): p = math.trunc(self._production);return Formula(p)

    # functions with 2 elements
    def __round__(self, arg=None): p = round(self._production, arg);return Formula(p)

    # operators with 1 element
    def __pos__(self): p = +self._production;return Formula(p)
    def __neg__(self): p = -self._production;return Formula(p)
    def __invert__(self): p = ~self._production;return Formula(p)

    # operators with 2 elements
    def __add__(self, other: 'Formula'): p = self._production + other._formula._production;return Formula(p)
    def __sub__(self, other: 'Formula'): p = self._production - other._formula._production;return Formula(p)
    def __mul__(self, other: 'Formula'): p = self._production * other._formula._production;return Formula(p)
    def __floordiv__(self, other: 'Formula'): p = self._production // other._formula._production;return Formula(p)
    def __truediv__(self, other: 'Formula'): p = self._production / other._formula._production;return Formula(p)
    def __mod__(self, other: 'Formula'): p = self._production % other._formula._production;return Formula(p)
    def __pow__(self, other: 'Formula'): p = self._production ** other._formula._production;return Formula(p)
    def __lshift__(self, other: 'Formula'): p = self._production << other._formula._production;return Formula(p)
    def __rshift__(self, other: 'Formula'): p = self._production >> other._formula._production;return Formula(p)
    def __and__(self, other: 'Formula'): p = self._production & other._formula._production;return Formula(p)
    def __xor__(self, other: 'Formula'): p = self._production ^ other._formula._production;return Formula(p)
    def __or__(self, other: 'Formula'): p = self._production | other._formula._production;return Formula(p)
    def __eq__(self, other: 'Formula'): p = self._production == other._formula._production;return Formula(p)
    def __ne__(self, other: 'Formula'): p = self._production != other._formula._production;return Formula(p)
    def __lt__(self, other: 'Formula'): p = self._production < other._formula._production;return Formula(p)
    def __gt__(self, other: 'Formula'): p = self._production > other._formula._production;return Formula(p)
    def __le__(self, other: 'Formula'): p = self._production <= other._formula._production;return Formula(p)
    def __ge__(self, other: 'Formula'): p = self._production >= other._formula._production;return Formula(p)
    
    # operator with 2 elements(r-mod)
    def __radd__(self, other: 'Formula'): p = other._formula._production + self._production;return Formula(p)
    def __rsub__(self, other: 'Formula'): p = other._formula._production - self._production;return Formula(p)
    def __rmul__(self, other: 'Formula'): p = other._formula._production * self._production;return Formula(p)
    def __rfloordiv__(self, other: 'Formula'): p = other._formula._production // self._production;return Formula(p)
    def __rtruediv__(self, other: 'Formula'): p = other._formula._production / self._production;return Formula(p)
    def __rmod__(self, other: 'Formula'): p = other._formula._production % self._production;return Formula(p)
    def __rpow__(self, other: 'Formula'): p = other._formula._production ** self._production;return Formula(p)
    def __rlshift__(self, other: 'Formula'): p = other._formula._production << self._production;return Formula(p)
    def __rrshift__(self, other: 'Formula'): p = other._formula._production >> self._production;return Formula(p)
    def __rand__(self, other: 'Formula'): p = other._formula._production & self._production;return Formula(p)
    def __rxor__(self, other: 'Formula'): p = other._formula._production ^ self._production;return Formula(p)
    def __ror__(self, other: 'Formula'): p = other._formula._production | self._production;return Formula(p)

class _Expression:

    def __init__(self, func: Callable[[dict], NumericValue], exp: str, kwargs: dict[str, NumericValue], args: set[str], tree: dict | str | NumericValue, tree_type: _TreeType) -> None:
        self._expression_text_with_signs: str = exp
        self._kwargs: dict[str, NumericValue] = kwargs
        self._func: Callable[[dict], NumericValue] = func
        self._args: set[str] = args
        self._tree: dict | NumericValue = self._tree_subs(tree, kwargs)
        self._tree_type: _TreeType = tree_type

    def _value(self) -> NumericValue:
        return self._func(self._kwargs)
    
    def _tree_subs(self, tree: dict | str | NumericValue, kwargs: dict[str, NumericValue]) -> dict | NumericValue:
        match self._tree_type:
            case _TreeType.NUMERICVALUE:
                return str(tree)
            case _TreeType.SYMBOL:
                return kwargs.get(tree)
            case _TreeType.FUNCTIONTREE:
                for item in tree:
                    if item != 'S':
                        tree[item] = self._tree_subs(tree[item], kwargs)
                return tree
            case _TreeType.OPERATOR1ETREE:
                tree['V'] = self._tree_subs(tree['V'], kwargs)
                return tree
            case _TreeType.OPERATOR2ETREE:
                tree['L'] = self._tree_subs(tree['L'], kwargs)
                tree['R'] = self._tree_subs(tree['R'], kwargs)
                return tree

    def _text(self) -> str:
        match_arg_sign: bool = False
        expression_text: str = ''
        for ch in self._expression_text_with_signs:
            if match_arg_sign:
                arg_value: NumericValue = self._kwargs[ch]
                value_str: str = str(arg_value)
                is_negative: bool = (not isinstance(arg_value, complex)) and arg_value < 0
                if is_negative:
                    value_str = f'({value_str})'
                expression_text += value_str
                match_arg_sign = False; continue
            if ch == SIGN_CH:
                match_arg_sign = True; continue
            expression_text += ch
        return expression_text
    
    def _text(self) -> str:
        expression_text: str = ''
        pos = 0
        while pos < len(self._expression_text_with_signs):
            char = self._expression_text_with_signs[pos]
            if char != SIGN_CH:
                expression_text += char
            else:
                pos += 1
                char = self._expression_text_with_signs[pos]
                arg_value: NumericValue = self._kwargs[char]
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
    def __round__(self, arg=None): return self._expression.__round__(arg)

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
