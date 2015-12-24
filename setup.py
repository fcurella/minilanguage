from setuptools import find_packages, setup


VERSION = '1.0.3'

setup(
    name='minilanguage',
    version=VERSION,
    url='https://github.com/fcurella/minilanguage/',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    description='A minimal DSL for Python',
    license='MIT',
    packages=find_packages(exclude=['*.tests', 'lextab.py', 'parsetab.py']),
    platforms=["any"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        "ply>=3",
    ],
    test_suite='minilanguage.tests',
)
