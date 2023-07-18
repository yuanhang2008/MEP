# -*- coding:utf-8 -*-


from typing import Any, Callable

from .production import Production, relock, unlock

from.draw import Draw


class Formula:

    def __init__(self, production: Production):
        unlock(production)
        if not isinstance(production, Production):
            self._func = lambda kwargs: production
            self._tree = production
            self._args = set()
        else:
            self._func = production._func
            self._tree = production._tree
            self._args = production._args
        self._exp = self._get_exp(self._tree)
        relock(production)
    
    def subs(self, **kwargs):
        args = {key for key in kwargs}
        if args != self._args:
            raise ValueError(f'substitution takes {len(self._args)} arguments, not {args}')
        return Expression(self._func, self._exp, kwargs, self._args)
    
    def draw(self, range_: tuple):
        Draw._drawer._add_func(self, range_)

    def _get_exp(self, tree: dict | str, level=0):
        if type(tree) != dict and type(tree) != str:
            print('qwe')
            return str(tree)
        if type(tree) == str:
            return '$' + tree
        if type(tree) == dict and type(tree.get('S', None)) == str:
            args = []
            for item in tree:
                if item == 'S': continue
                if type(tree[item]) == dict:
                    args.append(self._get_exp(tree[item]))
                else:
                    args.append(('$' + tree[item]) if type(tree[item]) == str else str(tree[item]))
            return f'{tree["S"]}({"".join([item + ", " for item in args[:-1]] + [args[-1]])})'
        
        parents = False
        if level > tree['l']:
            parents = True

        if type(tree['L']) != dict:
            if type(tree['L']) == str:
                left = '$' + tree['L']
            else:
                left = str(tree['L']) if tree['L'] >= 0 else ('(' + str(tree['L']) + ')')
        else:
            left = self._get_exp(tree['L'], tree['l'])
        
        if type(tree['R']) != dict:
            if type(tree['R']) == str:
                right = '$' + tree['R']
            else:
                right = str(tree['R']) if tree['R'] >= 0 else ('(' + str(tree['R']) + ')')
        else:
            right = self._get_exp(tree['R'], tree['l'])
        
        operator = tree['O']
        if parents:
            return ''.join(['(', left, operator, right, ')'])
        return ''.join([left, operator, right])
    
    def curry(self, **kwargs):
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

    def __str__(self):
        exp: str = ''
        for item in self._exp:
            if item != '$':
                exp += item
        return exp

class Expression:

    def __init__(self, func: Callable[[dict], Any], exp: str, kwargs: dict, args: set):
        self._exp = exp
        self._kwargs = kwargs
        self._func = func
        self._args = args

    def value(self):
        return self._func(self._kwargs)

    def __str__(self):
        flag = False
        exp: str = ''
        for item in self._exp:
            if flag:
                exp += str(self._kwargs[item]) if self._kwargs[item] >= 0 else ('(' + str(self._kwargs[item]) + ')')
                flag = False
                continue
            if item == '$':
                flag = True
                continue
            exp += item
        return exp
