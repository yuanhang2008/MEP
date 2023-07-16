# -*- coding: utf-8 -*-


from typing import Callable


def unlock(*args):
    production: Production
    for production in args:
        if isinstance(production, Production):
            production._locked = False

def product(operator, left, right, level):
    unlock(left, right)
    if isinstance(right, Production) and (not isinstance(left, Production)):
        return Production(
        eval(f'lambda kwargs: left {operator} right._func(kwargs)',
            {'left': left,
            'right': right}),
        {'L': left, 'O': operator, 'R': right._tree, 'l': level})

    if isinstance(right, Production):
        return Production(
        eval(f'lambda kwargs: left._func(kwargs) {operator} right._func(kwargs)',
            {'left': left,
            'right': right}), 
        {'L': left._tree, 'O': operator, 'R': right._tree, 'l': level})
    else:
        return Production(
        eval(f'lambda kwargs: left._func(kwargs) {operator} right',
            {'left': left,
            'right': right}),
        {'L': left._tree, 'O': operator, 'R': right, 'l': level})

class Production:
    
    def __init__(self, func, tree):
        self._locked = True
        self._func: Callable[[dict]] = func
        self._tree: dict | str = tree

    def __getattribute__(self, __name: str):
        if super().__getattribute__('_locked'):
            raise AttributeError('cannot access a Production object')
        return super().__getattribute__(__name)

    def __add__(self, other): return product('+', self, other, 4)
    def __sub__(self, other): return product('-', self, other, 4)
    def __mul__(self, other): return product('*', self, other, 5)
    def __floordiv__(self, other): return product('//', self, other, 5)
    def __truediv__(self, other): return product('/', self, other, 5)
    def __mod__(self, other): return product('%', self, other, 5)
    def __pow__(self, other): return product('**', self, other, 6)
    def __lshift__(self, other): return product('<<', self, other, 3)
    def __rshift__(self, other): return product('>>', self, other, 3)
    def __and__(self, other): return product('&', self, other, 2)
    def __xor__(self, other): return product('^', self, other, 1)
    def __or__(self, other): return product('|', self, other, 1)
    
    def __radd__(self, other): return product('+', other, self, 4)
    def __rsub__(self, other): return product('-', other, self, 4)
    def __rmul__(self, other): return product('*', other, self, 5)
    def __rfloordiv__(self, other): return product('//', other, self, 5)
    def __rtruediv__(self, other): return product('/', other, self, 5)
    def __rmod__(self, other): return product('%', other, self, 5)
    def __rpow__(self, other): return product('**', other, self, 6)
    def __rlshift__(self, other): return product('<<', other, self, 3)
    def __rrshift__(self, other): return product('>>', other, self, 3)
    def __rand__(self, other): return product('&', other, self, 2)
    def __rxor__(self, other): return product('^', other, self, 1)
    def __ror__(self, other): return product('|', other, self, 1)

class Symbol(Production):

    def __init__(self, sign):
        super().__init__(lambda kwargs: kwargs[sign], sign)