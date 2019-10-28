from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyStratum-MSSQL',

    version='0.10.2',

    description='A stored procedure and function loader and wrapper generator for SQL Server',
    long_description=long_description,

    url='https://github.com/SetBased/py-stratum-mssql',

    author='Set Based IT Consultancy',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],

    keywords='stored procedure, stored procedures, wrapper, loader, SQL Server',

    packages=find_packages(exclude=['build', 'pystratum_test']),

    install_requires=['pymssql', 'pystratum>=0.10.21'],
)
