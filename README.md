# MEP

***Mathematical Expression Parsing***

![License](https://img.shields.io/badge/license-MIT-green) ![Language](https://img.shields.io/badge/language-Py3.11-blue) ![Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fyuanhang2008%2FMEP%2Freleases%2Flatest&query=name&label=version&color=red)  ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fyuanhang2008%2FMEP&query=stargazers_count&label=stars&color=yellow)

## Stargazers over time

[![Stargazers over time](https://starchart.cc/yuanhang2008/MEP.svg)](https://starchart.cc/yuanhang2008/MEP)

## install

In the directory of MEP:

```
pip install .
```

or use ```setup.py``` to install:

```
python setup.py install
```

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

#### curry

```curry``` method can curry a formula and return the curried formula.

```python
>>>f1 = MEP.Formula(X + Y)
>>>f2 = f1.curry(x=2)
>>>print(f2.text())
2+y
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

## Features in Development

- [ ] Show functions images with tkinter.
- [ ] Code for test (too lazy to write.
- [ ] Analyze formulas, such as calculating definition domains.
- [ ] Optimize the code.
- [ ] Consider removing "draw" or verifying whether it is still required.
...

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/yuanhang2008/MEP/issues).

## About Author

Bilbili: [航sail654](https://space.bilibili.com/3546938777537032)
Github: [yuanhang2008](https://github.com/yuanhang2008)
QQ: [远航](https://user.qzone.qq.com/3467359137)

## License

Copyright yuanhang2008, 2023.

Distributed under the terms of the [MIT License](https://github.com/yuanhang2008/MEP/blob/master/LICENSE).

## Change Log

[ChangeLog](https://github.com/yuanhang2008/MEP/blob/master/CHANGELOG.md)