import os
from setuptools import setup

def read(fname):
    with open("README.md") as f:
        return f.read()

setup(
    name = "multipro",
    version = "0.0.1",
    author = "David Johnnes",
    author_email = "david.johnnes@gmail.com",
    description = ("A generic module that enables multiprocessing execution on any given function"),
    license = "BSD",
    keywords = "multiprocessing, parallel execution, fast execution, speed processing",
    url = "",
    packages=['multiprocessor'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)