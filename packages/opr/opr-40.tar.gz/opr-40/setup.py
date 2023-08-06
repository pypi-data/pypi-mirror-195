# This file is placed in the Public Domain.


"object programming runtime"


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opr",
    version="40",
    author="B.H.J. Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opr",
    description="object programming runtime",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["opr", "opr.modules"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
