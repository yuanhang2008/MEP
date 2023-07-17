# -*- coding:utf-8 -*-


from .production import Production, unlock
from typing import Callable, Any
from.draw import Draw


class Formula:

    def __init__(self, production: Production):
        unlock(production)
        self._func = production._func
        self._tree = production._tree
        self._exp = self._get_exp(self._tree)
    
    def subs(self, **kwargs):
        return Expression(self._func, self._exp, kwargs)
    
    def draw(self, range_: tuple):
        Draw._drawer._add_func(self, range_)
    
    def _get_exp(self, tree: dict | str, level=0):
        if type(tree) == str:
            return tree
        if type(tree) == dict and type(tree.get('S', None)) == str:
            args = []
            for item in tree:
                if item == 'S': continue
                if type(tree[item]) == dict:
                    args.append(self._get_exp(tree[item]))
                else:
                    args.append(str(tree[item]))
            return f'{tree["S"]}({"".join([item + ", " for item in args[:-1]] + [args[-1]])})'
        
        parents = False
        if level > tree['l']:
            parents = True

        if type(tree['L']) != dict:
            left = str(tree['L'])
        else:
            left = self._get_exp(tree['L'], tree['l'])
        
        if type(tree['R']) != dict:
            right = str(tree['R'])
        else:
            right = self._get_exp(tree['R'], tree['l'])
        
        operator = tree['O']
        if parents:
            return ''.join(['(', left, operator, right, ')'])
        return ''.join([left, operator, right])

    def __str__(self):
        return self._exp

class Expression:

    def __init__(self, func: Callable[[dict], Any], exp: str, kwargs: dict):
        self._func = func
        self._exp = exp
        self._kwargs = kwargs

    def value(self):
        return self._func(self._kwargs)

    def __str__(self):
        exp: str = ''
        for item in self._exp:
            for kwarg in self._kwargs:
                if item == kwarg:
                    exp += str(self._kwargs[kwarg])
                    break
            else:
                exp += item
        return exp