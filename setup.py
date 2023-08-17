# -*- coding: utf-8 -*-

"""
Python Map Generation
=====================
Simple python world generation
"""

from setuptools import setup, find_packages

setup(
    name="py-map-generation",
    version="0.1.1",
    license="Unlicensed",
    author="Michał Gdula (Fluffy-Bean)",
    author_email="<michal-gdula@protonmail.com>",
    description="Simple python world generation",
    packages=find_packages(),
    py_modules=["py_map_generation"],
    python_requires=">=3.7, <4",
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Unlicensed",
    ],
    zip_safe=False,
)
