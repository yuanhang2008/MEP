# -*- coding:utf-8 -*-


'''
MEP: Mathematical expression processing.

A tool to product, show or operate formulas.

Features include:
    Formula: The basic feature of MEP, it products a formula similar to a function.
    Expression: It is producted after substituting into formula.
    Symbol: It is captured as a production, like an argument of function.
    Draw: Mainly used for display formulas.
    Math: Provide extra functinos.

    etc.
'''

__version__ = '1.1.3'


from .formula import Formula, call, get

# from.draw import Draw
from .math import Math
from .production import Symbol, symbols


X = Symbol('x')
Y = Symbol('y')
Z = Symbol('z')

__all__ = [
    'X', 'Y', 'Z', 
    'Formula', 
    'call', 
    'get', 
    'Math', 
    'Symbol', 
    'symbols' # removed class Draw
]