# -*- coding:utf-8 -*-


from .production import Production, X


class Formula:

    def __init__(self, expression: Production):
        self._func = expression._func
        self._exp = expression._exp
    
    def substitute(self, arg):
        return Expression(self._func, self._exp, arg)

    def get_exp(self):
        return self._exp

class Expression:

    def __init__(self, func, exp, arg):
        self._func = func
        self._exp = exp
        self._arg = arg

    def value(self):
        return self._func(self._arg)

    def get_exp(self):
        exp = ''
        for item in self._exp:
            exp += str(self._arg) if item == 'x' else item
        return exp


if __name__ == '__main__':
    f = Formula(X*2+3)
    print(f.get_exp())
    exp = f.substitute(4j+1.44e2)
    print(exp.get_exp())
    print(exp.value())
