# MEP

## install

Run ```auto_install_1.bat``` to install MEP, if it doesn't work, try enter ```pip install setuptools``` and ```pip install wheel``` to install the two necessary libraries, please. 
```auto_install_2.bat``` can install MEP as a temporary modules, you can use it if you are just here to test the library or try some features, not at work or important occasions.

## usage

### formula

Use ```MEP.Formula``` and ```MEP.X``` to product a formula.

```python
>>>import MEP
>>>f = MEP.Formula(2 * MEP.X - 1)
```

Formula objects are printable and ```__str__``` method is defined, but ```text``` method is recommended.

```python
>>>print(f)
<Formula f(x)=2*x-1>
>>>str(f)
'<Formula f(x)=2*x-1>'
>>>f.text()
'2*x-1'
```

### symbol

A ```Symbol``` object can be defined by users, a symbol's name must be a letter. 

```python
A = MEP.Symbol('a')
f = Formula(A * 2)
```

A formula can contain multiple symbols, and 'x', 'y', 'z' are built-in, they are default symbols in MEP.

Use variable ```symbols``` to get all defined symbols's sign, you can also visit ```sign``` to get the sign of a symbol.

```python
>>>MEP.symbols
{'x', 'y', 'z', 'a'}

>>>A.sign
'a'
```

### draw

```Draw``` is used to draw a function plot in matplotlib

```python
>>>range_ = (-100, 100)

>>>f1 = Formula(2 * MEP.X + 1)
>>>f2 = Formula(MEP.X ** 2)

>>>f1.draw(range_)
>>>f2.draw(range_)

>>>Draw.display()
```

more functions, such as ```clear```: clear all the formulas in Draw object.

```python
>>>Draw.clear()
>>>Draw.display()
# Nothing to show
```

```setprec```: set the precision of the plot. the larger the precision, the more detailed the plot, but the slower the program runs.

However, drawing a formula contains multiple symbols is invalid.

### expression

Substitute a value to build a new expression.The substituted values should correspond to the symbols by using keyword arguments, the key names are symbols's signs.

```python
>>>f = MEP.Formula(2 * MEP.X - 1)
>>>exp = f.subs(x=2) # an Expression object
>>>exp.value()
3

>>>print(exp)
<Expression f(x=2)=2*2-1>
>>>exp.text()
'2*2-1'
```

### math

Class ```Math``` provides with some special functions, which can participate in formula generations.

```python
>>>f = Formula(Math.abs(9 - MEP.X)) # equal to |9-x|
>>>exp = f.subs(x=12)
>>>exp.value()
3
```

### curry

```curry``` method can curry a formula and return the curried formula.

```python
>>>f1 = MEP.Formula(X + Y)
>>>f2 = f1.curry(x=2)
>>>exp = f2.subs(y=3)

>>>exp.value
5
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/yuanhang2008/MEP/issues).

## License

Copyright yuanhang, 2023.

Distributed under the terms of the  [MIT License](https://github.com/yuanhang2008/MEP/blob/master/LICENSE).