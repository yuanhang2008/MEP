# -*- coding: utf-8 -*-


class Production:
    
    def __init__(self, func, exp):
        self._func = func
        self._exp = exp

    def product(self, operator, left, right):
        if right is self and left is not self:
            return Production(
            eval(f'lambda x: left {operator} right._func(x)',
                {'left': left,
                'right': right}),
            '(' + str(left) + operator + str(right._exp) + ')')

        if type(right) == Production: return Production(
            eval(f'lambda x: left._func(x) {operator} right._func(x)',
                {'left': left,
                'right': right}), 
            '(' + str(left._exp) + operator + str(right._exp) + ')')
        else: return Production(
            eval(f'lambda x: left._func(x) {operator} right',
                {'left': left,
                'right': right}),
            '(' + str(left._exp) + operator + str(right) + ')')       

    def __add__(self, other): return self.product('+', self, other)
    def __sub__(self, other): return self.product('-', self, other)
    def __mul__(self, other): return self.product('*', self, other)
    def __floordiv__(self, other): return self.product('//', self, other)
    def __truediv__(self, other): return self.product('/', self, other)
    def __mod__(self, other): return self.product('%', self, other)
    def __pow__(self, other): return self.product('**', self, other)
    def __lshift__(self, other): return self.product('<<', self, other)
    def __rshift__(self, other): return self.product('>>', self, other)
    def __and__(self, other): return self.product('&', self, other)
    def __xor__(self, other): return self.product('^', self, other)

    def __or__(self, other): return self.product('|', self, other)
    def __radd__(self, other): return self.product('+', other, self)
    def __rsub__(self, other): return self.product('-', other, self)
    def __rmul__(self, other): return self.product('*', other, self)
    def __rfloordiv__(self, other): return self.product('//', other, self)
    def __rtruediv__(self, other): return self.product('/', other, self)
    def __rmod__(self, other): return self.product('%', other, self)
    def __rpow__(self, other): return self.product('**', other, self)
    def __rlshift__(self, other): return self.product('<<', other, self)
    def __rrshift__(self, other): return self.product('>>', other, self)
    def __rand__(self, other): return self.product('&', other, self)
    def __rxor__(self, other): return self.product('^', other, self)
    def __ror__(self, other): return self.product('|', other, self)

X = Production(lambda x: x, 'x')