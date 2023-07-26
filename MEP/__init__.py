# -*- coding:utf-8 -*-


'''
MEP: Mathematical expression processing.

A tool to product, show or operate formulas.
'''

__version__ = '1.0.2'


from .formula import Formula

from.draw import Draw
from .math import Math
from .production import Symbol, symbols


X = Symbol('x')
Y = Symbol('y')
Z = Symbol('z')


__all__ = [
    'X', 'Y', 'Z', 
    'Formula', 
    'Draw', 
    'Math', 
    'Symbol', 
    'symbols'
]