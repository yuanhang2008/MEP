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
((2*x)-1)

>>>str(f)
'((2*x)-1)'
```

```draw_func(range_, config=DEFAULT_CONFIG)``` is used to prepare a function plot in matplotlib, then show by ```showall()```

About Config object,it includes arguments that generating the plot and can be overwrited yourself.
if config argument is not given, it' s a default config.

```python
>>>range_ = (-100, 100)
>>>config = Config(line_color='#ff0000')

>>>f1 = Formula(2 * MEP.X + 1)
>>>f2 = Formula(MEP.X ** 2)

>>>f1.draw_func(range_)
>>>f2.draw_func(range_, config)

>>>showall()
```

Besides, if there are too many lines in a plot, ```set_max(value)``` is a way to solve.
The default max is None, i.e. no max.

```python
>>>set_max(2)

>>>f3 = Formula(MEP.X * 0.2)
# ValueError: 3 (more than 2) items to draw
```

### expression

Substitute a value to build a new expression.

```python
>>>exp = f.subs(2) # an Expression object
>>>exp.value()
3

>>>print(exp)
((2*2)-1)
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/yuanhang2008/MEP/issues).

## License

Copyright yuanhang, 2023.

Distributed under the terms of the  [MIT License](https://github.com/yuanhang2008/MEP/blob/master/LICENSE).