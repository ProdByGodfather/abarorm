from setuptools import setup, find_packages

setup(
    name='abarorm',
    version='0.8.0',
    description='A simple ORM library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mahdi Ghasemi',
    author_email='prodbygodfather@gmail.com',
    url='https://github.com/prodbygodfather/abarorm',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'mysql-connector-python', 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
    ],
)
