# -*- coding: utf-8 -*-


import unittest
from MEP import *


class TestFormula(unittest.TestCase):
    pass


if __name__ == '__main__':
    #unittest.main()
    #breakpoint()
    f = Formula(X+Y >= 10)
    print(f)
    exp = f.subs(x=12, y=2)
    print(exp, exp.value())