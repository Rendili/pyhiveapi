#import os
from setuptools import setup, find_packages
from codecs import open
from os import path

#try:
#    from setuptools import setup, find_packages
#    packages = find_packages(exclude=['tests'])
#except ImportError:
#    from distutils.core import setup
#    packages = ["pyhiveapi"]


setup(
    name='pyhiveapi',
    version='0.0.10',
    description='A Python library to interface with the Hive API',
    long_description="A Python library to interface with the Hive API",
	#    url='https://github.com/pypa/sampleproject',

    author='Rendili',
    author_email='rendili@outlook.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
#        'Topic :: Software Development :: API',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    keywords='Hive API Library',
#    py_modules = ['pyhiveapi'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
#    packages=packages,
#    packages=["pyhiveapi"],
#    install_requires=[],

    # To provide executable scripts, use entry points in preference to the

    # "scripts" keyword. Entry points provide cross-platform support and allow

    # pip to create the appropriate form of executable for the target platform.

    entry_points={
        'console_scripts': [
            'pyhiveapi=pyhiveapi.pyhiveapi:Pyhiveapi',
        ],
    },
)