# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import random as rd


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

    def __init__(self, max: int | None=None):
        self.max = max
        self.funcs = []
    
    def setmax(self, value):
        self.max = value
        self._check_flow(self.max, len(self.funcs))

    def _add_func(self, formula, range_):
        self._check_flow(self.max, len(self.funcs) + 1)
        self.funcs.append((formula, range_))

    def _check_flow(self, max, funcs_length) -> None:
        if max is None:
            return
        if funcs_length > max:
            raise ValueError(f'{funcs_length} (more than {max}) items to draw')

    def show(self):
        colors = color(len(self.funcs))
        counter = 0
        for func in self.funcs:
            formula = func[0]
            range_ = func[1]

            x = [item for item in range(*range_)]
            y = [formula._func(arg) for arg in x]
            
            plt.plot(x, y, color=colors[counter], label=formula._exp)
            counter += 1
        plt.legend(loc='best')
        plt.show()

drawer = Drawer()