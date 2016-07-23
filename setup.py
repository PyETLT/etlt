from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ETLT',

    version='0.0.30',

    description='Extract Transform Load - but not in that strict order',
    long_description=long_description,

    url='https://github.com/SetBased/py-etlt',

    author='Paul Water',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Topic :: Database'
    ],

    keywords='ETLT, ETL, ELT, Extract, Transform, Load, DWH, Data, Warehouse',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=[]
)
