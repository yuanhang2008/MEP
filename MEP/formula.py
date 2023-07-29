# -*- coding:utf-8 -*-


from typing import Any, Callable, List

from .production import Production, relock, unlock

from.draw import Draw


def get_tree_type(tree):
        if type(tree) == int or type(tree) == float or \
        type(tree) == complex or type(tree) == bool: return 'n||b'

        if type(tree) == str: return 'str'
        if tree is None: return 'None'

        if type(tree) == dict:
            if tree.get('S', None) is not None: return 'S*'
            if tree.get('V', None) is not None: return 'OVl'
            if tree.get('L', None) is not None: return 'LORl'
        
        raise ValueError(f'bad tree was given')

class Formula:

    def __init__(self, production: Production) -> None:
        self._formula = _Formula(production)
    
    def subs(self, **kwargs) -> 'Expression':
        return self._formula._subs(**kwargs)
    
    def draw(self, range_: tuple):
        self._formula._draw(range_)

    def curry(self, **kwargs) -> 'Formula':
        return self._formula._curry(**kwargs)

    def text(self) -> str:
        return self._formula._text()

    def __str__(self):
        return self._formula.__str__()

class Expression:

    def __init__(self, func: Callable[[dict], Any], exp: str,kwargs: dict, args: set, tree) -> None:
        self._expression = _Expression(func, exp, kwargs, args, tree)

    def value(self) -> int | float | complex | bool:
        return self._expression._value()
    
    def text(self) -> str:
        return self._expression._text()
    
    def __str__(self) -> str:
        return self._expression.__str__()

class _Formula:

    def __init__(self, production: Production):
        unlock(production)
        if not isinstance(production, Production):
            self._func = lambda kwargs: production
            self._tree = production
            self._args = set()
        else:
            self._func = production._func
            self._tree = production._tree
            self._args = set(sorted(list(production._args)))
        self._exp = self._get_exp(self._tree)
        relock(production)
    
    def _subs(self, **kwargs):
        args = {key for key in kwargs}
        if args != self._args:
            raise ValueError(f'substitution takes {len(self._args)} arguments, be {len(args)} was given')
        return Expression(self._func, self._exp, kwargs, self._args, self._tree)

    def _draw(self, range_: tuple):
        Draw._drawer._add_func(self, range_)
    
    def _get_exp(self, tree: dict | str | Any, level=0):
        tree_type = get_tree_type(tree)
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

class _Expression:

    _cache: List = []

    def __init__(self, func: Callable[[dict], Any], exp: str, kwargs: dict, args: set, tree):
        self._exp = exp
        self._kwargs = kwargs
        self._func = func
        self._args = args
        self._tree = self._get_tree(tree, kwargs)
        self._result = self._func(self._kwargs)

    def _value(self):
        item: tuple
        flag = False
        for item in self._cache:
            if item[0] != self._exp: continue
            for arg in self._kwargs:
                if self._kwargs.get(arg, None) != item[1][arg]: 
                    flag = True
                    break
            if flag: continue
            return item[2]
        
        self._cache.append((self._exp, self._kwargs, self._result))    
        return self._result
    
    def _get_tree(self, tree: dict | str | Any, kwargs: dict):
        tree_type = get_tree_type(tree)
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