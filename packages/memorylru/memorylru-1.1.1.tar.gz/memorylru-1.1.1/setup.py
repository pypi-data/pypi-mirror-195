# -*- coding: utf-8 -*-
from platform import system
from setuptools import Extension, find_packages, setup

README = open("README.md").read()


lru_module = Extension("memorylru.lru", sources=["memorylru/lru.c"])


extensions = []
if system() != "Windows":
    extensions.append(lru_module)


setup(
    name="memorylru",
    version="1.1.1",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/vangheem/memorylru",
    license="BSD",
    setup_requires=[],
    zip_safe=True,
    include_package_data=True,
    ext_modules=extensions,
    packages=find_packages(),
)
