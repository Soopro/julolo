# coding=utf-8

from setuptools import setup, find_packages
import alimmodity

setup(
    name='alimmodity',
    version=alimmodity.__version__,
    packages=find_packages(),
    install_requires=[
        'xlrd==1.1.0',
    ],
    author='Redy',
    author_email='redy.ru@gmail.com',
    description='Alimmodity is a tool to convert alimama csv to json.',
    license='MIT',
    keywords='alimama commodity',
    url='',
    entry_points={
        'console_scripts': [
            'alimmodity = alimmodity:run',
        ]
    }
)
