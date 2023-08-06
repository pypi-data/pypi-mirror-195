from setuptools import setup

with open('/home/sdoxl/programming/projects/networkinglib/README.md') as f:
    long_description = f.read()

setup(
    name='networkinglib',
    version='0.2.1',
    author='lstuma',
    author_email='g.lstuma@gmail.com',
    url='https://github.com/lstuma/networkinglib/',
    description='Extension providing a basic networking protcol implementations as a Python module using mainly C-Extenstions.',
    long_description=long_description,
    packages=['networkinglib']
)