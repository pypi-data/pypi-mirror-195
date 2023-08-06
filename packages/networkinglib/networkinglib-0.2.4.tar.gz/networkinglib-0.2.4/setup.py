from setuptools import setup

from pathlib import Path
long_description = Path('/home/sdoxl/programming/projects/networkinglib/README.md').read_text()

setup(
    name='networkinglib',
    version='0.2.4',
    author='lstuma',
    author_email='g.lstuma@gmail.com',
    url='https://github.com/lstuma/networkinglib/',
    description='Extension providing a basic networking protcol implementations as a Python module using mainly C-Extenstions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['networkinglib'],
    install_requires=[
        'networking-tcp-client',
        'networking-udp-client'
    ]
)