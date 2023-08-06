from setuptools import setup
from setuptools import find_packages
from os import path
from Cython.Build import cythonize

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'minepython',      
    version = '0.0.4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'QinBingFeng',        
    author_email = '114479602@qq.com',
    url = 'http://www.minepython.com',
    description = '在Minecraft游戏环境中学习编程，使用编程的方式来玩Minecraft',
    packages=find_packages()
    )