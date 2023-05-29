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
    version='0.0.3',
    packages=find_packages(exclude=[
        "tutorials",
        "LICENSE",
        ".gitignore",
        "README.md",
        "misc",
        ".travis.yml",
        "notes.py",
    ]),
    description='GasCompressibility-py is a Python library for calculating the gas compressibility factor, Z, based on real gas law.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=classifiers(),
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


# python setup.py sdist bdist_wheel
# python -m twine upload --skip-existing --repository testpypi dist/*
