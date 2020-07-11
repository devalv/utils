# -*- coding: utf-8 -*-
"""Python package config.

build example: python3 setup.py sdist bdist_wheel
"""
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dav_utils',
    version='0.2.5',
    author='Aleksey Devyatkin',
    author_email='devyatkin.av@ya.ru',
    description='Set of tools that often have to reproduce in Python scripts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devalv/utils',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
