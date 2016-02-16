# -*- coding: utf-8 -*-

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='qeXml',
    version='0.1',
    description='A quantum espresso xml generator',
    url='https://github.com/lmpizarro/espresso-xml',
    author='Luis María Pizarro',
    author_email='lpizarro@cnea.gov.ar',
    license='GNU',
    packages=['qeXml'],
    long_description=read("README.md"),
    classifiers =[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: Free For Educational Use",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Physics",
        ],
    install_requires=[
        'lxml'],
    zip_safe=False)


''' References:

    http://python-packaging.readthedocs.org/en/latest/minimal.html
    https://pythonhosted.org/an_example_pypi_project/setuptools.html
'''
