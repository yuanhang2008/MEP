# -*- coding: utf-8 -*-


import math
from .production import *


class Math:

    @classmethod
    def abs(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return abs(x)
        return Production(
            lambda kwargs: abs(x._func(kwargs)), 
            {'x': x._tree, 'S': 'abs'})
    
    @classmethod
    def round(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return round(x)
        return Production(
            lambda kwargs: round(x._func(kwargs)), 
            {'x': x._tree, 'S': 'round'})
    
    @classmethod
    def ceil(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return math.ceil(x)
        return Production(
            lambda kwargs: math.ceil(x._func(kwargs)), 
            {'x': x._tree, 'S': 'ceil'})
    
    @classmethod
    def floor(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return math.floor(x)
        return Production(
            lambda kwargs: math.floor(x._func(kwargs)), 
            {'x': x._tree, 'S': 'floor'})
    
    @classmethod
    def int(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return int(x)
        return Production(
            lambda kwargs: int(x._func(kwargs)), 
            {'x': x._tree, 'S': 'int'})
    
    @classmethod
    def round(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return round(x)
        return Production(
            lambda kwargs: round(x._func(kwargs)), 
            {'x': x._tree, 'S': 'round'})
    
    @classmethod
    def root(cls, x, y):
        unlock(x, y)
        if not (isinstance(x, Production) or isinstance(y, Production)):
            return x ** (1 / y)
        return Production(
            lambda kwargs: (x._func(kwargs) if isinstance(x, Production) else x) ** 
                (1 / (y._func(kwargs) if isinstance(y, Production) else y)), 
            {'x': (x._tree if isinstance(x, Production) else x), 
            'y': (y.tree if isinstance(y, Production) else y), 
            'S': 'root'})
    
    def sqrt(cls, x):
        unlock(x)
        if not isinstance(x, Production):
            return math.sqrt(x)
        return Production(
            lambda kwargs: math.sqrt(x._func(kwargs)), 
            {'x': x._tree, 'S': 'sqrt'})