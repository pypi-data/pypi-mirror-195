from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = "Find what you're looking for in a flash with Huntela - the ultimate search tool for Python."
LONG_DESCRIPTION = """
# Huntela

Huntela makes searching in Python very simple.

```python
>>> import huntela
>>> huntela.simple_search("app", ["app", "apple", "hello", "world"])
[{'index': 0, 'value': 'app', 'confidence': 1},
{'index': 1, 'value': 'apple', 'confidence': 0.6}]
```
With a variety of powerful algorithms to choose from, finding what you're looking for has never been easier.

From binary search to linear search and more, Huntela has everything you need to 
quickly and efficiently search through your data. With a simple, intuitive interface
and lightning-fast performance, Huntela is the go-to package for anyone who needs to search through data.

Whether you're a data scientist, engineer, or  developer, Huntela will help you find what you need.

## Installation
> Huntela officially supports Python 3.9 upwards. 

Request is available on PyPi and it can be installed using `pip`

```batch
python -m pip install huntela
```
"""

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="huntela", 
    version=VERSION,
    author="Tomisin Abiodun",
    author_email="decave.12357@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
