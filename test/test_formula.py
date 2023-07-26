# -*- coding: utf-8 -*-


import unittest
from MEP import *


class TestFormula(unittest.TestCase):
    pass


if __name__ == '__main__':
    #unittest.main()
    #breakpoint()
    f = Formula(Math.logicand(2<=X, 2<= Y))
    print(f)
    exp = f.subs(x=12, y=1)
    print(exp, exp.value())