from setuptools import setup, find_packages
import sys

__version__ = '5.4.0'


if '--version' in sys.argv:
    print(__version__)
    sys.exit()


setup(
    name='abarorm',
    version=__version__,
    description='abarorm is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite and PostgreSQL databases in Python. It aims to provide a simple and intuitive interface for managing database models and interactions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mahdi Ghasemi',
    author_email='prodbygodfather@gmail.com',
    url='https://github.com/prodbygodfather/abarorm',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'psycopg2-binary>=2.9.0',
    ],
    extras_require={
        'postgresql': ['psycopg2-binary>=2.9.0']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)

