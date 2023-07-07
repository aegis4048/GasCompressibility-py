import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()


def readme():
    with open('README.md') as f:
        return f.read().strip()


def classifiers():
    with open('classifiers.txt') as f:
        return f.read().strip().split('\n')


setup(
    name='gascompressibility',
    version='0.1.8',
    packages=find_packages(exclude=[
        "tutorials",
        "LICENSE",
        ".gitignore",
        "README.md",
        "misc",
        ".travis.yml",
        "notes.py",
        "testruns.ipynb",
        "papers",
        "docs",
    ]),
    description='GasCompressibility-py is a Python library for calculating the gas compressibility factor, Z, based on real gas law.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=classifiers(),
    license='MIT',
    author='Eric Kim',
    author_email='aegis4048@gmail.com',
    install_requires=[
        'numpy>=1.14',
        'scipy>=1.5',
        'matplotlib>=3.2.1',
    ],
    url='https://github.com/aegis4048/GasCompressibiltiy-py/tree/main',
)


# python setup.py sdist bdist_wheel
# python -m twine upload --skip-existing dist/*

# python -m twine upload --skip-existing --repository testpypi dist/*
# python setup.py install --user
# pip uninstall gascompressibility
# pip install gascompressibility