from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'test pkg'
LONG_DESCRIPTION = 'my first test pkg'

setup(
    name='haczechpkg',
    version=VERSION,
    author='me',
    author_email='me@me.me',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'test_pkg'],
    classifiers=[
        "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
    ]
)