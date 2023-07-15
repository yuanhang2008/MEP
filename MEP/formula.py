# -*- coding:utf-8 -*-


from .production import Production, unlock
from typing import Tuple
from.draw import Drawer, Config, DEFAULT_CONFIG


drawer = Drawer()

def showall():
    drawer.show()

def set_max(value):
    drawer.max = value

class Formula:

    def __init__(self, production: Production):
        unlock(production)
        self._func = production._func
        self._exp = production._exp
    
    def subs(self, arg):
        return Expression(self._func, self._exp, arg)
    
    def draw_func(self, range_: Tuple, config: Config=DEFAULT_CONFIG):
        drawer.add_func(self._func, range_, config)

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