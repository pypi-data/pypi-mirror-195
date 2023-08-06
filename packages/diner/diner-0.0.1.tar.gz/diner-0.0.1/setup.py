#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='diner',
    version='0.0.1',
    description='Diner: A Diverse Named Entity Recognition Tool',
    url='',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords='NER',
    packages=find_packages(),
    install_requires=[
          'transformers',
    ],
    entry_points={
          'console_scripts': [
              'diner = diner.diner:main'
          ]
    },
)