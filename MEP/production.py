# -*- coding: utf-8 -*-


operators = {
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__floordiv__': '//',
    '__truediv__': '/',
    '__mod__': '%',
    '__pow__': '**',
    '__lshift__': '<<',
    '__rshift__': '>>',
    '__and__': '&',
    '__xor__': '^',
    '__or__': '|'
}

def take_function_name(func):
    name = func.__name__
    def wrapper(*args, **kwargs):
        return func(*args, __name__=name, **kwargs)
    return wrapper

class Production:
    
    def __init__(self, func, exp):
        self._func = func
        self._exp = exp

    def product(self, operator, left, right):
        if type(right) == Production: return Production(
            eval(f'lambda x: left._func(x) {operators[operator]} right._func(x)',
                {'operators': operators,
                'left': left,
                'right': right,
                'operator': operator}), 
            '(' + str(left._exp) + operators[operator] + str(right._exp) + ')')
        else: return Production(
            eval(f'lambda x: left._func(x) {operators[operator]} right',
                {'operators': operators,
                'left': left,
                'right': right,
                'operator': operator}),
            '(' + str(left._exp) + operators[operator] + str(right) + ')')

    @take_function_name
    def __add__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __sub__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __mul__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __floordiv__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __truediv__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __mod__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __pow__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __lshift__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __rshift__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __and__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __xor__(self, other, __name__): return self.product(__name__, self, other)

    @take_function_name
    def __or__(self, other, __name__): return self.product(__name__, self, other)

X = Production(lambda x: x, 'x')
