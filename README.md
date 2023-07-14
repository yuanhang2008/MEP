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