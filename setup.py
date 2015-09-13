from setuptools import setup

setup(
    name='gethazel',
    version='0.1.0',
    description='A balanced life is a good life.',
    author='Reilly Tucker Siemens',
    author_email='reilly.siemens@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='Corgi Hazel Balance',
    py_modules=['gethazel'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gethazel=gethazel:main',
        ]
    },
)
