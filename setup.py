#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='OverTheWire',
    version='0.0.3',
    license='Apache License 2.0',
    url='https://github.com/tommilligan/OverTheWire/',
    author='Tom Milligan',
    author_email='code@tommilligan.net',
    description="Connection and password helper for playing OverTheWire wargames",
    keywords='OverTheWire over the wire otw ctf capture the flag wargame wargames',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'PyYAML == 3.12'
    ],
    tests_require=['nose2 == 0.6.5'],
    test_suite='nose2.collector.collector',
    extras_require={
        'dev': [
            'coverage == 4.4.1',
            'cov-core == 1.15.0',
            'nose2 == 0.6.5',
            'six == 1.10.0'
        ]
    }
)
