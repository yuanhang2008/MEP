# -*- coding: utf-8 -*-


import unittest
from MEP import *


class MEPTestCase(unittest.TestCase):

    VALUES = (0, 1, 8.3, -4, 3j, 8j-2.1, 3e3, -5.89e2j+1e0)
    CASES = [
        [Formula(X), VALUES], 
        [Formula(X + 8), tuple(map(lambda x: x + 8, VALUES))], 
        [Formula(X - X), tuple(map(lambda x: x - x, VALUES))], 
        [Formula(X - 7 + X), tuple(map(lambda x: x - 7 + x, VALUES))], 
        [Formula(X * 2 - 5), tuple(map(lambda x: x * 2 - 5, VALUES))], 
        [Formula(X + X * 6), tuple(map(lambda x: x + x * 6, VALUES))], 
        [Formula(X * 3 / 3), tuple(map(lambda x: x * 3 / 3, VALUES))], 
        [Formula(X * (X + 1)), tuple(map(lambda x: x * (x + 1), VALUES))], 
        [Formula(X ** (X / (X * 2 + 1))), tuple(map(lambda x: x ** (x / (x * 2 + 1)), VALUES))], 

        # r-mode test
        [Formula(8 + X), tuple(map(lambda x: 8 + x, VALUES))], 
        [Formula(100 * (8 + X)), tuple(map(lambda x: 100 * (8 + x), VALUES))], 
        [Formula(X + (9 / (X - 3)) - X), tuple(map(lambda x: x + (9 / (x - 3)) - x, VALUES))]
    ]

    def test_calculation(self):
        for item in self.CASES:
            for value in enumerate(self.VALUES):
                formula: Formula = item[0]
                exp = formula.substitute(value[1])
                self.assertEqual(exp.value(), item[1][value[0]])


if __name__ == '__main__':
    unittest.main()
    