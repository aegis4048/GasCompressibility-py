
'''
from setuptools import setup, find_packages


with open('readme', 'r') as f:
    long_description = f.read()

setup(
    name='gascompressibility',
    version='0.0.1',
    packages=find_packages(exclude=[
        "tutorials",
        "LICENSE",
        ".gitignore",
        "README.md",
        "misc"
    ]),
    description='GasCompressibility-py is a Python library for calculating the gas compressibility factor, Z, based on real gas law.',
    long_description=long_description,
    license='MIT',
    author='Eric Kim',
    author_email='aegis4048@gmail.com',
    install_requires=[
        'numpy>=1.21.5',
        'scipy>=1.9.1',
        'matplotlib>=3.5.1',
    ],
    url='https://github.com/aegis4048/GasCompressibiltiy-py/tree/main',
)
'''