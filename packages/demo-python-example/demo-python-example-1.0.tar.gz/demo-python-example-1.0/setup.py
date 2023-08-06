#!/usr/bin/env python
 
from setuptools import setup
 
setup(
    name='demo-python-example',
    version='1.0',
    description='Project example for building Python project with JFrog products',
    author='JFrog',
    author_email='jfrog@jfrog.com',
    packages=['helloworld'],
    install_requires=['PyYAML>3.11', 'nltk'],
)