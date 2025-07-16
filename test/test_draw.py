# -*- coding: utf-8 -*-


import unittest

from MEP import *


class TestDraw(unittest.TestCase):
    pass


if __name__ == '__main__':
    # unittest.main()
    e1 = Formula(X+Y).subs(x=3, y=7)
    print(e1)
    e2 = Formula(X * Y - Z).subs(x=2, y=8.2, z=10)
    print(e2)
    e3 = e1 + e2
    print(e3)