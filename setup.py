from setuptools import setup, find_packages

setup(
    name='abarorm',
    version='3.1.1',
    description='abarorm is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite & PostgreSQL and MySQL databases in Python. It aims to provide a simple and intuitive interface for managing database models and interactions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mahdi Ghasemi',
    author_email='prodbygodfather@gmail.com',
    url='https://github.com/prodbygodfather/abarorm',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'mysql-connector-python>=8.0.0',
        'psycopg2-binary>=2.9.0',
    ],
    extras_require={
        'mysql': ['mysql-connector-python>=8.0.0'],
        'postgresql': ['psycopg2-binary>=2.9.0']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
    ],
)
