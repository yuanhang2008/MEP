# -*- coding: utf-8 -*-


import random as rd

import matplotlib.pyplot as plt

COLOR = {
    '#000000', '#000088','#0000ff', '#008800', '#008888', '#0088ff', '#00ff00', '#00ff88', '#00ffff', 
    '#880000', '#880088','#8800ff', '#888800', '#888888', '#8888ff', '#88ff00', '#88ff88', '#88ffff', 
    '#ff0000', '#ff0088','#ff00ff', '#ff8800', '#ff8888', '#ff88ff', '#ffff00', '#ffff88', '#ffffff'
}

def strcolor(color: tuple):
    strc = '#'
    for item in color:
        strc += hex(item)[2:]
    return strc

def color(num: int):
    if type(num) != int:
        raise TypeError(f'argument num must be an int, not {type(num)}')
    result = []
    if num <= len(COLOR):
        colors = set(tuple(COLOR))
        for _ in range(num):
            c = rd.choice(list(colors))
            colors.remove(c)
            result.append(c)
        return result
    while num: 
        c = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        if (c := strcolor(c)) in COLOR:
            continue
        result.append(c)
        num -= 1
    return result

class Drawer:

    def __init__(self):
        self._precision = 640
        self._funcs = []
    
    def _setprec(self, value):
        if type(value) != int:
            raise ValueError(f'precision must be int, not {type(value).__name__}')
        self._precision = value

    def _add_func(self, formula, range_):
        self._funcs.append((formula, range_))
    
    def _range_check(self, range_):
        if range_[0] > range_[1]:
            raise ValueError(f'{range_} cant be a useable range')
    
    def _get(self, func, arg, range_):
        self._range_check(range_)
        d = (range_[1] - range_[0]) / self._precision
        x = range_[0]
        xlst, ylst = [], []
        while x <= range_[1]:
            try:
                ylst.append(func({arg: x}))
                xlst.append(x)
            except ZeroDivisionError:
                pass
            x += d

        return xlst, ylst

    def _show(self):
        colors = color(len(self._funcs))
        counter = 0
        for func in self._funcs:
            formula = func[0]
            range_ = func[1]

            if len(formula._args) > 1:
                raise ValueError('cannot display a formula with more than 1 symbol')
            arg = list(formula._args)[0]
            x, y = self._get(formula._func, arg, range_)

            plt.plot(x, y, color=colors[counter], label=formula._text())
            counter += 1
        self._funcs.clear()
        plt.legend(loc='best')
        plt.show()

class Draw:

    _drawer = Drawer()

    @classmethod
    def display(cls):
        cls._drawer._show()
    
    @classmethod
    def setprec(cls, value):
        cls._drawer._setprec(value)
    
    @classmethod
    def clear(cls):
        cls._drawer._funcs.clear()