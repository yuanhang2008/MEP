# -*- coding:utf-8 -*-


from .production import Production, unlock
from typing import Tuple
from.draw import Draw


class Formula:

    def __init__(self, production: Production):
        unlock(production)
        self._func = production._func
        self._tree = production._tree
        self._exp = self._get_exp(self._tree)
    
    def subs(self, arg):
        return Expression(self._func, self._exp, arg)
    
    def draw(self, range_: Tuple):
        Draw._drawer._add_func(self, range_)
    
    def _get_exp(self, tree, level=0):
        if tree == 'x':
            return tree
        
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

    def __init__(self, func, exp, arg):
        self._func = func
        self._exp = exp
        self._arg = arg

    def value(self):
        return self._func(self._arg)

    def __str__(self):
        exp = ''
        for item in self._exp:
            exp += str(self._arg) if item == 'x' else item
        return exp