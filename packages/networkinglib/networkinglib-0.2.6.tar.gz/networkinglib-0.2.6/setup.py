from setuptools import setup
from setuptools import find_packages

from pathlib import Path
long_description = Path('README.md').read_text()

setup(
    name='networkinglib',
    version='0.2.6',
    author='lstuma',
    author_email='g.lstuma@gmail.com',
    url='https://github.com/lstuma/networkinglib/',
    description='Extension providing a basic networking protcol implementations as a Python module using mainly C-Extenstions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'networking-tcp-client',
        'networking-udp-client'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)