# -*- coding:utf-8 -*-


import math
from typing import Any, Callable, NoReturn

from .config import *
from .production import Production, relock, unlock

# from.draw import Draw


named_formulas: dict = {}

def _get_tree_type(tree):
        if type(tree) == int or type(tree) == float or \
        type(tree) == complex or type(tree) == bool: return 'n||b'

        if type(tree) == str: return 'str'
        if tree is None: return 'None'

        if type(tree) == dict:
            if tree.get('S', None) is not None: return 'S*'
            if tree.get('V', None) is not None: return 'OVl'
            if tree.get('L', None) is not None: return 'LORl'
        raise ValueError(f'bad tree was given')

def _name_check(name: str) -> 'Formula' | NoReturn:
    formula: Formula | None = named_formulas.get(name, None)
    if formula is None:
        raise ValueError(f'No such a formula named {name}')
    return formula

def call(name: str, **kwargs) -> 'Expression' | NoReturn:
    '''
    Call a named formula with arguments.

    Args:
        name (str): The name of formula to be call.
        **kwargs: The arguments to call the formula.
    
    Returns:
        Expression: Expression after substituting into the formula.
    
    Raises:
        ValueError: There is no formula that matches the name.
    '''
    formula = _name_check(name)
    return formula.subs(**kwargs)

def get(name: str) -> 'Formula' | NoReturn:
    '''
    Get a formula matches the name.

    Args:
        name (str): The name of formula to be match.
    
    Returns:
        Formula: Formula that matches the name.
    
    Raises:
        ValueError: There is no formula that matches the name.
    '''
    formula = _name_check(name)
    return formula

class Formula:
    '''
    Math expression with arguments.

    Args:
        production (Production): The expression with arguments.
        name (str): Name of a formula.

    Attributes:
        _formula (_Formula): The corresponding unencapsulated object of formula.
    '''

    def __init__(self, production: Production, name: str =...) -> None:
        self._formula = _Formula(production)
        if name is not ...:
            named_formulas[name] = self
    
    def subs(self, **kwargs) -> 'Expression':
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

    def curry(self, **kwargs) -> 'Formula':
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

    def __str__(self):
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
    def __round__(self, arg=None): return self._formula.__round__(arg)

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
        _fexpression (_Expression): The corresponding unencapsulated object of expression.
    '''

    def __init__(self, func: Callable[[dict], Any], exp: str, kwargs: dict, args: set, tree) -> None:
        self._expression = _Expression(func, exp, kwargs, args, tree)

    def value(self) -> int | float | complex | bool:
        '''
        Return the value of expression.

        Returns:
            int | float | complex | bool: The value of expression after calculating.
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

class _Formula:

    def __init__(self, production: Production):
        self._production = production
        unlock(self._production)
        if not isinstance(self._production, Production):
            self._func = lambda kwargs: self._production
            self._tree = self._production
            self._args = set()
        else:
            self._func = self._production._func
            self._tree = self._production._tree
            self._args = set(sorted(list(self._production._args)))
        self._exp = self._get_exp(self._tree)
        relock(self._production)
    
    def _subs(self, **kwargs):
        args = {key for key in kwargs}
        if args != self._args:
            raise ValueError(f'arguments do not match')
        return Expression(self._func, self._exp, kwargs, self._args, self._tree)

    # def _draw(self, range_: tuple):
    #     Draw._drawer._add_func(self, range_)
    
    def _get_exp(self, tree: dict | str | Any, level=0):
        tree_type = _get_tree_type(tree)
        match tree_type:
            case 'n||b':
                return str(tree)
            case 'str':
                return '$' + tree
            case 'S*':
                return self._get_func_tree(tree)
            case 'OVl':
                self._get_ovl_tree(tree)
            case 'LORl':
                return self._get_lor_tree(tree, level)
            case 'None':
                return None

    def _get_func_tree(self, tree):
        args = []
        for item in tree:
            if item == 'S': continue
            args.append(self._get_exp(tree[item]))
        return f'{tree["S"]}({"".join([item + ", " for item in args if item is not None])[:-2]})'
    
    def _get_ovl_tree(self, tree):
        if tree['V'] is None:
            raise ValueError('Nonetype was given to an OVL tree')
        return '(' + tree['O'] + self._get_exp(tree['V']) + ')'

    def _get_lor_tree(self, tree, level):
        parents = True if level > tree['l'] else False
        lr_result = {}
        for item in ['L', 'R']:
            if tree[item] is None:
                raise ValueError('Nonetype was given to a LOR tree')
            lr_result[item] = self._get_exp(tree[item])
        l_bracket, r_bracket = ('(', ')') if parents else ('', '')
        return ''.join([l_bracket, lr_result['L'], tree['O'], lr_result['R'], r_bracket])

    def _curry(self, **kwargs):
        args = set(tuple(self._args))
        tree = self._tree_curry(self._tree, kwargs)
        for key in kwargs:
            if key not in args:
                raise ValueError(f'arguments do not match')
            args.remove(key)

        def wapper(kwargs_):
            for key in kwargs:
                kwargs_[key] = kwargs[key]
            return self._func(kwargs_)
        
        return Formula(Production(wapper, tree, args))
    
    def _tree_curry(self, tree: dict | str, kwargs: dict):
        if type(tree) == str:
            if kwargs.get(tree, None) is not None:
                return kwargs[tree]
            return tree

        if type(tree.get('S', None)) == str:
            for key, value in tree.items():
                if key == 'S': continue
                if type(value) == str or type(value) == dict:
                    tree[key] = self._tree_curry(tree[key], kwargs)
            return tree
        
        if type(tree['L']) == str or type(tree['L']) == dict:
            tree['L'] = self._tree_curry(tree['L'], kwargs)
        if type(tree['R']) == str or type(tree['R']) == dict:
            tree['R'] = self._tree_curry(tree['R'], kwargs)
        return tree
    
    def _text(self):
        exp: str = ''
        for item in self._exp:
            if item != '$':
                exp += item
        return exp

    def __str__(self):
        return f'<Formula f({"".join([arg + ", " for arg in self._args])[:-2]})={self._text()}>'
    
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

    def __init__(self, func: Callable[[dict], Any], exp: str, kwargs: dict, args: set, tree):
        self._exp = exp
        self._kwargs = kwargs
        self._func = func
        self._args = args
        self._tree = self._get_tree(tree, kwargs)

    def _value(self):     
        return self._func(self._kwargs)
    
    def _get_tree(self, tree: dict | str | Any, kwargs: dict):
        tree_type = _get_tree_type(tree)
        match tree_type:
            case 'n||b' | 'None':
                return tree
            case 'str':
                return kwargs.get(tree)
            case 'S*':
                for item in tree:
                    if item == 'S': continue
                    tree[item] = self._get_tree(tree[item], kwargs)
                return tree
            case 'OVl':
                tree['V'] = self._get_tree(tree['V'], kwargs)
                return tree
            case 'LORl':
                tree['L'] = self._get_tree(tree['L'], kwargs)
                tree['R'] = self._get_tree(tree['R'], kwargs)
                return tree

    def _text(self):
        flag = False
        exp: str = ''
        for item in self._exp:
            if flag:
                k = type(self._kwargs[item]) != complex and self._kwargs[item] < 0
                exp += ('(' + str(self._kwargs[item]) + ')') if k else str(self._kwargs[item])
                flag = False
                continue
            if item == '$':
                flag = True
                continue
            exp += item
        return exp

    def __str__(self):
        fargs = [f'{key}={self._kwargs[key]}, ' for key in self._kwargs]
        return f'<Expression f({"".join(fargs)[:-2]})={self._text()}>'
    
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
