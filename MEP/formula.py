# -*- coding:utf-8 -*-


from .production import Production


class Formula:

    def __init__(self, expression: Production):
        self._func = expression._func
        self._exp = expression._exp
    
    def substitute(self, arg):
        return Expression(self._func, self._exp, arg)

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