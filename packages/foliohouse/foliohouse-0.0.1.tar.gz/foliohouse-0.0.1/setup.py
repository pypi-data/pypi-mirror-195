from setuptools import setup

setup(
    name='foliohouse',
    version='0.0.1',
    description='A Python package for accessing datasets from Foliohouse',
    author='Your name',
    author_email='bashybaranaba@gmail.com',
    packages=['foliohouse'],
    install_requires=[
        'pandas',
        'pycryptodome',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)