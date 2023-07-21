# MEP

## install

Run ```auto_install1.bat``` to install MEP, if it doesn't work, try ```auto_install1.bat```, please.

## usage

### formula

Use ```MEP.Formula``` and ```MEP.X``` to product a formula.

```python
>>>import MEP
>>>f = MEP.Formula(2 * MEP.X - 1)
```

Formula objects are printable and ```__str__``` method is defined.

```python
>>>print(f)
2*x-1

>>>str(f)
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

```setmax``` is a way to set the maximum number of functions display on the plot.
The default max is None, i.e. infinity.

```python
>>>Draw.setmax(2)

>>>f3 = Formula(MEP.X * 0.2)
>>>f3.draw(range_)
# ValueError: 3 (more than 2) items to draw
```

more functions, such as ```clear```: clear all the formulas in Draw object.

```python
>>>Draw.clear()
>>>Draw.display()
# Nothing to show
```

However, drawing a formula contains multiple symbols is invalid.

### expression

Substitute a value to build a new expression.The substituted values should correspond to the symbols by using keyword arguments, the key names are symbols's signs.

```python
>>>f = MEP.Formula(2 * MEP.X - 1)
>>>exp = f.subs(x=2) # an Expression object
>>>exp.value()
3

>>>print(exp)
2*2-1
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