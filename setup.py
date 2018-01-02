# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import os

here = path.abspath(path.dirname(__file__))
long_description = "See website for more info."
dev_tools = ['pytest','python-coveralls','coverage','pytest-cov','pytest-xdist','ipython']
setup(
    name='CoW',
    version='0.0.1',
    description='Copy-On-Write Mixin Base Class.',
    long_description=long_description,
    # The project's main homepage.
    url='https://github.com/bannsec/pyCoW',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='copy-on-write cow',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=dev_tools,
    extras_require={
        'dev': dev_tools,
    },
)

