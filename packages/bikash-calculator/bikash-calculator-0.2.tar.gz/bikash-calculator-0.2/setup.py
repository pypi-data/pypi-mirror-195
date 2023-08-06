import setuptools

from pathlib import Path


setuptools.setup(
    name='bikash-calculator',
    version='0.2',
    author='Bikash Chowdhury',
    author_email= 'chowdhurybikash38@gmail.com',
    description='This is very basic calculator',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/bikash829',
    packages=setuptools.find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
)