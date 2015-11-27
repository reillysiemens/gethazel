import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = ['requests']

setup(
    name='gethazel',
    version='0.1.0',
    description='A balanced life is a good life.',
    long_description=README,
    author='Reilly Tucker Siemens',
    author_email='reilly.siemens@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
    ],
    packages=find_packages(),
    keywords='Corgi Hazel Balance',
    py_modules=['gethazel'],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'gethazel=gethazel.__main__:main',
        ]
    },
)
