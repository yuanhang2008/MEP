# -*- encoding: utf-8 -*-


from setuptools import setup


with open('README.md', 'r', encoding='utf-8') as md:
    long_description = md.read()

with open('./MEP/__init__.py', 'r', encoding='utf-8') as init:
    for line in init.readlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setup(
    name='MEP', 
    version=version, 
    description='Mathematical expression processing.', 
    long_description=long_description, 
    author='yuanhang', 
    author_email='minecraft_mo_ye@qq.com', 
    url='https://github.com/yuanhang/MEP', 
    packages=['MEP']
)