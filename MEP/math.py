# -*- coding: utf-8 -*-


import math
from .production import *


class Math:

    @classmethod
    def abs(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)

        if not isinstance(x, Production):
            return abs(x)
        return Production(
            lambda kwargs: abs(x_func(kwargs)), 
            {'x': x_tree, 'S': 'abs'}, 
            x_args)
    
    @classmethod
    def round(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return round(x)
        return Production(
            lambda kwargs: round(x_func(kwargs)), 
            {'x': x_tree, 'S': 'round'}, 
            x_args)
    
    @classmethod
    def ceil(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return math.ceil(x)
        return Production(
            lambda kwargs: math.ceil(x_func(kwargs)), 
            {'x': x_tree, 'S': 'ceil'}, 
            x_args)
    
    @classmethod
    def floor(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return math.floor(x)
        return Production(
            lambda kwargs: math.floor(x_func(kwargs)), 
            {'x': x_tree, 'S': 'floor'}, 
            x_args)
    
    @classmethod
    def int(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return int(x)
        return Production(
            lambda kwargs: int(x_func(kwargs)), 
            {'x': x_tree, 'S': 'int'}, 
            x_args)
    
    @classmethod
    def round(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return round(x)
        return Production(
            lambda kwargs: round(x_func(kwargs)), 
            {'x': x_tree, 'S': 'round'}, 
            x_args)
    
    @classmethod
    def root(cls, x, y):
        unlock(x, y)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        if isinstance(y, Production):
            y_func = y._func
            y_tree = y._tree
            y_args = y._args
        relock(x, y)

        if not (isinstance(x, Production) or isinstance(y, Production)):
            return x ** (1 / y)
        return Production(
            lambda kwargs: (x_func(kwargs) if isinstance(x, Production) else x) ** 
                (1 / (y_func(kwargs) if isinstance(y, Production) else y)), 
            {'x': (x_tree if isinstance(x, Production) else x), 
            'y': (y_tree if isinstance(y, Production) else y), 
            'S': 'root'}, 
            x_args | y_args)
    
    def sqrt(cls, x):
        unlock(x)
        if isinstance(x, Production):
            x_func = x._func
            x_tree = x._tree
            x_args = x._args
        relock(x)
        
        if not isinstance(x, Production):
            return math.sqrt(x)
        return Production(
            lambda kwargs: math.sqrt(x_func(kwargs)), 
            {'x': x_tree, 'S': 'sqrt'}, 
            x_args)