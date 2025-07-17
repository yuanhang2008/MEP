# MEP

***数学表达式解析（Mathematical Expression Parsing）***

![许可证](https://img.shields.io/badge/许可证-MIT-green) ![语言](https://img.shields.io/badge/语言-Py3.11-blue) ![版本](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fyuanhang2008%2FMEP%2Freleases%2Flatest&query=name&label=版本&color=red)  ![Stars](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fyuanhang2008%2FMEP&query=stargazers_count&label=Stars&color=yellow)

## Stars增长图

[![Stars增长图](https://starchart.cc/yuanhang2008/MEP.svg)](https://starchart.cc/yuanhang2008/MEP)

## 安装

在MEP目录下输入:

```
pip install .
```

或使用 ```setup.py``` 安装:

```
python setup.py install
```

## 功能

### formula

使用 ```MEP.Formula``` 以及 ```MEP.X``` 产生一个```Formula```公式对象。

```python
>>>import MEP
>>>f = MEP.Formula(2 * MEP.X - 1)
```

```Formula``` 对象是可打印的，支持 ```__str__``` 方法，但推荐以 ```text``` 方法获取字面量。

```python
>>>print(f)
<Formula f(x)=2*x-1>
>>>str(f)
'<Formula f(x)=2*x-1>'
>>>f.text()
'2*x-1'
```

#### curry

```curry``` 方法可以将一个公式以任意变量柯里化并得到柯里化后的新公式。

```python
>>>f1 = MEP.Formula(X + Y)
>>>f2 = f1.curry(x=2)
>>>print(f2.text())
2+y
```

### symbol

 ```Symbol``` 对象可以被用户自定义，但必须是单个字母。

```python
A = MEP.Symbol('a')
f = Formula(A * 2)
```

一个 ```Formula``` 可以包含多个 ```Symbol``` ，“x”、“y”、“z”是内置的默认符号。

使用 ```symbols``` 变量来获取所有已定义的符号，每个 ```Symbol``` 也可以用 ```sign``` 属性访问对应的字母。

```python
>>>MEP.symbols
{'x', 'y', 'z', 'a'}

>>>A.sign
'a'
```

### expression

代入数值来构造一个表达式对象 ```Expressio``` ，被替换的值应该通过使用关键字参数与符号对应，键名是符号对应的字母。

```python
>>>f = MEP.Formula(2 * MEP.X - 1)
>>>exp = f.subs(x=2) # 一个 Expression 对象
>>>exp.value()
3

>>>print(exp)
<Expression f(x=2)=2*2-1>
>>>exp.text()
'2*2-1'
```

### math

 ```Math``` 类提供了一些特殊的函数，可以参与公式的构造。

```python
>>>f = Formula(Math.abs(9 - MEP.X)) # 等于 |9-x|
>>>exp = f.subs(x=12)
>>>exp.value()
3
```

## 开发中的功能

- [ ] 用tkinter显示函数图像。
- [ ] 测试 (懒得写。
- [ ] 公式的分析，如计算定义域。
- [ ] 优化代码。
- [ ] 考虑删除“draw”或保留。
...

## 漏洞/申请

请通过 [github issue tracker](https://github.com/yuanhang2008/MEP/issues) 发送错误报告和功能申请。

## 关于作者

Bilbili: [航sail654](https://space.bilibili.com/3546938777537032)
Github: [yuanhang2008](https://github.com/yuanhang2008)
QQ: [远航](https://user.qzone.qq.com/3467359137)

## 许可证

Copyright yuanhang2008, 2023.

根据 [MIT License](https://github.com/yuanhang2008/MEP/blob/master/LICENSE) 条款分发。

## 更新日志

[更新日志](https://github.com/yuanhang2008/MEP/blob/master/CHANGELOG.md)