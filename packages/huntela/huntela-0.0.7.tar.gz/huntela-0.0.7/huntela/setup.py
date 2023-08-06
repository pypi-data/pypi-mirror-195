import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
readme_path = os.path.join(parent_dir, "README.md")

with open(readme_path, "rt") as f:
    readme = f.read()

VERSION = '0.0.7' 
DESCRIPTION = "Find what you're looking for in a flash with Huntela - the ultimate search tool for Python."
LONG_DESCRIPTION = readme

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
