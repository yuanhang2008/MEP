# MEP

## install

Run ```auto_install.bat``` to install MEP.

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

### Draw

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

### expression

Substitute a value to build a new expression.

```python
>>>exp = f.subs(2) # an Expression object
>>>exp.value()
3

>>>print(exp)
2*2-1
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/yuanhang2008/MEP/issues).

## License

Copyright yuanhang, 2023.

Distributed under the terms of the  [MIT License](https://github.com/yuanhang2008/MEP/blob/master/LICENSE).