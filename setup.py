# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mbtools",
    version="0.1.1",
    author="Misael Barreto de Queiroz",
    author_email="misaelbarreto@gmail.com",
    description="Project that offer utility functions to treat strings, numbers, files etc.",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/misaelbarreto/mbtools",
    packages=setuptools.find_packages(),
    license='BSD License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)